import os
from typing import Dict
from textwrap import dedent
# from openai import OpenAI
from openai import AsyncOpenAI

MODEL = os.getenv('OPENAI_MODEL','gpt-4o-mini')

def make_email_prompt(speaker: Dict[str,str]) -> str:
    return dedent(f'''
    You are a B2B copywriter for DroneDeploy (drone mapping & reality capture for construction).
    Write a concise, friendly cold email inviting the speaker to visit our booth #42 for a live demo and a small gift.
    Personalize to their role and company. 3-5 sentences total. Avoid exclamation overuse.
    Do NOT suggest partnerships. If they are a partner or competitor, return the single word: SKIP.
    Check if the company has 500+ employees first. If so, or if close, generate the email, otherwise return SKIP.

    SPEAKER:
    Name: {speaker.get('name','')}
    Title: {speaker.get('title','')}
    Company: {speaker.get('company','')}

    Output JSON with keys: subject, body.
    ''').strip()

async def draft_email(speaker: Dict[str,str]) -> Dict[str,str]:
    # client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
    # prompt = make_email_prompt(speaker)

    research_prompt = f"""
    Research the company: {speaker.get('company','')}

    Please search for information about this company and provide details about:
    - What industry they operate in
    - What products or services they offer
    - Their main business activities
    - Their target market or customers
    - Any recent news or developments

    Focus on information that would help classify them in relation to DroneDeploy (construction, real estate, technology, etc.).
    """
    response = await client.responses.create(
        model="gpt-4o-mini",
        tools=[{"type": "web_search"}],
        input=research_prompt,
    )

    company_info = response.output_text.strip()
    print(f"Company info: {company_info}")
    return company_info

    # resp = client.chat.completions.create(
    #     model=MODEL,
    #     messages=[{"role":"system","content":"You write concise B2B emails."},
    #               {"role":"user","content":prompt}],
    #     temperature=0.7,
    # )
    # text = resp.choices[0].message.content.strip()
    # Very simple JSON extraction
    # import json, re
    # try:
    #     data = json.loads(re.search(r"\{[\s\S]*\}", company_info).group(0))
    #     # if competitor, skip adding to csv
    #     if isinstance(data, str) and data.strip().upper() == 'SKIP':
    #         return {"subject":"","body":""}
    # except Exception:
    #     if text.strip().upper() == 'SKIP':
    #         return {"subject":"","body":""}
    #     data = {"subject": "Let's connect at DCW", "body": text}
    # return data

# async def _research_company(self, company_name: str) -> str:
#         """Research a company using web search and return information about it."""
#         try:
#             research_prompt = f"""
#             Research the company: {company_name}

#             Please search for information about this company and provide details about:
#             - What industry they operate in
#             - What products or services they offer
#             - Their main business activities
#             - Their target market or customers
#             - Any recent news or developments

#             Focus on information that would help classify them in relation to DroneDeploy (construction, real estate, technology, etc.).
#             """

#             response = await self.client.responses.create(
#                 model="gpt-5-nano",
#                 tools=[{"type": "web_search"}],
#                 input=research_prompt,
#             )

#             company_info = response.output_text.strip()
#             logger.info(f"Researched company '{company_name}' - found information")
#             return company_info

#         except Exception as e:
#             logger.error(f"Research failed for {company_name}: {e}")
#             return f"Limited information available for {company_name}"
        

# self.client = (
#             openai.AsyncOpenAI(api_key=Config.OPENAI_API_KEY)
#             if Config.OPENAI_API_KEY
#             else None
#         )