# European Startups Lead Scraper

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Requests](https://img.shields.io/badge/Requests-2C2D72?style=for-the-badge)
![BeautifulSoup](https://img.shields.io/badge/BeautifulSoup4-4B8BBE?style=for-the-badge)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Logging](https://img.shields.io/badge/Logging-4D4D4D?style=for-the-badge)

Turns a startup directory into a ready-to-use B2B lead list — company name, location,
founding year, funding stage, description, and website — exported straight to Excel.

## The problem

Building a lead list by hand from an online directory means opening dozens (or hundreds) of
pages one by one, copying fields into a spreadsheet, and re-checking for duplicates — hours of
manual work for something that has to be redone every time you target a new market or country.

This scraper automates that entire process for the [EU-Startups
Directory](https://www.eu-startups.com/directory/): pick a country and how many leads you
need, and it collects the data, cleans it, and hands you back a spreadsheet ready for outreach.

## What it does

- **Two-level collection** — pulls the basics from the country listing, then visits each
  company's own page to fetch funding and description, so no field is left half-filled
- **Ask, don't hardcode** — country and lead count are chosen at runtime, no need to touch the
  code to target a different market
- **No duplicate leads** — companies are deduplicated on a normalized version of their link,
  so the same business never appears twice even if listed under slightly different URLs
- **Doesn't give up on the first network hiccup** — failed requests are retried automatically
  before a page is skipped
- **Safe to interrupt** — progress is saved to Excel every 10 companies, so a long run doesn't
  lose data if it's stopped partway through
- **Won't crash if you're checking the file mid-run** — if the output Excel is open elsewhere
  when the script tries to save, it logs it and keeps going instead of crashing
- **Full audit trail** — every missing field and failed request is logged with a timestamp

## Sample output

| Name          | Based in | Foundation year | Funding      | Tags              |
|---------------|----------|------------------|--------------|-------------------|
| Acme Robotics | Berlin   | 2021             | €2M raised   | Robotics, AI      |
| GreenLoop     | Paris    | 2019             | Seed         | Sustainability    |

*(illustrative example — no real scraped data is included in this repo, see Disclaimer)*

## Tech stack

Python · Requests · BeautifulSoup4 · pandas · `logging`

## Installation

```bash
git clone https://github.com/leonangheluta-cyber/eu-startups-lead-scraper.git
cd eu-startups-lead-scraper
pip install -r requirements.txt
```

## Usage

```bash
python european_companies.py
```

You'll be asked for a country and how many leads to collect. The script walks the directory
listing, visits each company's page for the remaining details, and writes the result to
`Lead_{country}_companies.xlsx`.

## Available as a standalone .exe — no Python required

```bash
python -m PyInstaller --onefile european_companies.py
```

The resulting executable runs the same country/quantity prompts in a console window — no
Python installation needed on the machine that runs it.

## Project structure

```
.
├── european_companies.py       # main script
├── config_europe_lead.py       # site-specific config (headers, CSS selectors, countries, timeouts)
├── requirements.txt
└── script_european_companies.log   # created on first run
```

`config_europe_lead.py` keeps everything specific to the target site — headers, CSS
selectors for each field, the 30-country URL slug lookup, timeout, and delay between
requests — separate from the scraping logic itself.

## Scraping etiquette

Requests are spaced out with a configurable delay and sent through a shared session with
descriptive headers, not fired anonymously. The target site's `robots.txt` was checked
before building this and does not disallow the directory pages used here.

## Roadmap

- Retry logic currently covers listing-page requests; detail-page requests log and skip on
  failure rather than retrying
- Description text isn't normalized for extra whitespace beyond quote removal

## Disclaimer

This repository is shared for portfolio/demonstration purposes and contains the scraper's
source code only — no real data collected with it. If you use this code, make sure your use
of the target site complies with its terms of use and `robots.txt` at the time you run it.