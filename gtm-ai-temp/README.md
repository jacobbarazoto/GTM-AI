# dd_gtm_ai_eng_exercise

Generate personalized, draft outreach emails to DCW speakers to invite them to Booth #42 for a DroneDeploy demo and gift.

## What this does
1. Scrapes the **All Speakers** page from Digital Construction Week.
2. Parses **Speaker Name / Title / Company**.
3. Classifies the **Company Category** as one of: `Builder`, `Owner`, `Partner`, `Competitor`, `Other` (filters out Partner/Competitor).
4. Uses an LLM (OpenAI) to generate a subject + short, role‑aware email body.
5. Writes `out/email_list.csv` with the required columns.

## Tech
- Python 3.10+
- `asyncio` + `aiohttp` for non‑blocking scraping and concurrent LLM calls
- OpenAI Chat Completions (configurable model)
- BeautifulSoup for HTML parsing
- `python-dotenv` for `.env` handling

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate   # on Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env_sample .env
# edit .env and set OPENAI_API_KEY=...
```

## Run
The inputs/inputs.py file defines the number of speakers to process (`limit`) as well as the number of concurrent jobs to run (`concurrent`). Update that file as desired (defaults to all speakers with 8 threads).

```bash
python main.py
```

Output appears at `out/email_list.csv`.

## Requirements

Create `requirements.txt` with:
```
aiohttp
beautifulsoup4
python-dotenv
openai>=1.0.0
certifi
```
