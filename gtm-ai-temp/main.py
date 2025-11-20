import os, csv, asyncio, importlib
import argparse
from dotenv import load_dotenv
from utils.scrape import scrape_speakers
from utils.classify import classify_company
from utils.llm import draft_email
from inputs.inputs import limit, concurrent

OUT_CSV = os.path.join('out','email_list.csv')

async def main():
    load_dotenv()
    # scrape speakers and if limit is set, only process that many
    speakers = await scrape_speakers()
    if limit:
        speakers = speakers[:int(limit) + 1]
    rows = []
    # limit running threads to 8
    sem = asyncio.Semaphore(max(1, int(concurrent)))
    # co-routine for processing speaker data
    async def process(sp):
        company_category = classify_company(sp.get('company',''), sp.get('title',''))
        print(f"Processing {sp['name']}-{sp['company']}-{sp['title']} ({company_category})")
        if company_category in ('Partner','Competitor'):
            print(f"Skipping {sp['name']}")
            return None
        # Make call to LLM for each speaker (doing this because a giant list of speakers in a single call is crazy)
        def run_llm():
            return draft_email({
                'name': sp.get('name',''),
                'title': sp.get('title',''),
                'company': sp.get('company','')
            })
        loop = asyncio.get_running_loop()
        # OpenAI is synchronous, so needs to be threaded
        async with sem:
            data = await loop.run_in_executor(None, run_llm)
            print (f"Processed {sp['name']}")
            print(data)
        # If LLM responded with SKIP logic, ignore
        if not data.get('subject') and not data.get('body'):
            return None
        return {
            'Speaker Name': sp.get('name',''),
            'Speaker Title': sp.get('title',''),
            'Speaker Company': sp.get('company',''),
            'Company Category': company_category,
            'Email Subject': data.get('subject',''),
            'Email Body': data.get('body',''),
        }
    # run each speaker data through co-routine
    tasks = [process(sp) for sp in speakers]
    # when a task is completed, add to CSV
    for coro in asyncio.as_completed(tasks):
        row = await coro
        if row:
            rows.append(row)
    os.makedirs('out', exist_ok=True)
    with open(OUT_CSV, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'Speaker Name','Speaker Title','Speaker Company','Company Category','Email Subject','Email Body'
        ])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {OUT_CSV}")

if __name__ == '__main__':
    asyncio.run(main())
