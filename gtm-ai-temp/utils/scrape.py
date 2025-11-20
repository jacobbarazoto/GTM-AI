import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import List, Dict, Tuple
import re
import os
import ssl
import certifi

SPEAKERS_URL = "https://www.digitalconstructionweek.com/all-speakers/"

# had to add SSL context for avoid SSL error: "certificate verify failed: unable to get local issuer certificate"
def _ssl_context():
    # Use certifi’s CA bundle for robust verification
    ctx = ssl.create_default_context(cafile=certifi.where())
    return ctx

def _norm_space(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").strip())

def _split_title_company(text: str) -> Tuple[str, str]:
    """
    Expect formats like:
      - "Head of Reality Capture at BigCo"
      - "Head of Reality Capture – BigCo"
      - "Head of Reality Capture — BigCo"
      - "Head of Reality Capture @ BigCo"
    Falls back to whole string as title if no company found.
    """
    txt = _norm_space(text)
    # Preferred split
    if " at " in txt:
        t, c = txt.split(" at ", 1)
        return _norm_space(t.strip("–—- ,")), _norm_space(c.strip("–—- ,"))
    # # Fallback separators
    # for sep in [" @ ", " – ", " — ", " - "]:
    #     if sep in txt:
    #         t, c = txt.split(sep, 1)
    #         return _norm_space(t.strip("–—- ,")), _norm_space(c.strip("–—- ,"))
    return txt, ""

# get text from url async so that we don't have to stay connected to site for the whole run
async def fetch_text(session: aiohttp.ClientSession, url: str) -> str:
    async with session.get(url, timeout=aiohttp.ClientTimeout(total=60)) as resp:
        resp.raise_for_status()
        return await resp.text()

def parse_speakers(html: str) -> List[Dict[str, str]]:
    """
    Parse cards with structure:
      .speaker-grid-item
        a
          .speaker-grid-details
            h3           -> name
            .speaker-job -> title + [separator] + company
    """
    soup = BeautifulSoup(html, "html.parser")
    out: List[Dict[str, str]] = []

    cards = soup.select(".speaker-grid-item")
    for card in cards:
        details = card.select_one(".speaker-grid-details")
        if not details:
            continue

        name_el = details.select_one("h3")
        job_el  = details.select_one(".speaker-job")

        name = _norm_space(name_el.get_text()) if name_el else ""
        meta = _norm_space(job_el.get_text(" ", strip=True)) if job_el else ""

        if not name and not meta:
            continue

        title, company = _split_title_company(meta)
        out.append({
            "name": name,
            "title": title,
            "company": company
        })

    # Deduplicate by (name, company) in case of repeated cards
    seen, uniq = set(), []
    for sp in out:
        key = (sp["name"].lower(), sp["company"].lower())
        if key not in seen:
            seen.add(key)
            uniq.append(sp)
    return uniq

async def scrape_speakers() -> List[Dict[str, str]]:
    # define insecure SSL in environment or create SSL context for secure connection
    allow_insecure = os.getenv("ALLOW_INSECURE_SSL", "false").lower() == "true"
    connector = aiohttp.TCPConnector(ssl=False if allow_insecure else _ssl_context())
    async with aiohttp.ClientSession(
        connector=connector,
        headers={"User-Agent": "dd-gtm-scraper/1.0"}
    ) as session:
        html = await fetch_text(session, SPEAKERS_URL)
        return parse_speakers(html)
