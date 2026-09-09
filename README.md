# European Startups Lead Scraper

A Python scraper that collects business leads (name, location, foundation year, funding, description, tags, and website link) from the [EU-Startups Directory](https://www.eu-startups.com/directory/), exports them to a clean Excel file, and lets you pick the target country and how many companies to collect at runtime.

Built as a portfolio project to demonstrate a realistic two-level scraping pipeline: a search page → detail page workflow with retry logic, deduplication, structured logging, and incremental saving.

> **Note:** this repository contains only the scraper code. No real scraped data is included — see [Disclaimer](#disclaimer) below.

## Features

- **Two-level scraping**: collects basic info from the country directory listing, then visits each company's page to fetch its funding and description.
- **Parametrized search**: choose the country (validated against a fixed list) and how many companies to collect via simple CLI prompts.
- **Deduplication**: companies are deduplicated on a normalized version of their link (lowercased, stripped of `http(s)://`/`www.`/trailing slash), stored in a set for fast lookups.
- **Retry logic with backoff**: failed requests to the listing pages are retried up to 3 times before the scraper moves on to the next page, instead of giving up on a single network hiccup.
- **Resilient parsing**: every field extraction goes through a shared helper that catches missing elements (`AttributeError`) and logs a warning instead of crashing.
- **Incremental saving**: results are saved to Excel every 10 companies during the detail-page pass, plus a final save at the end — so a long run doesn't lose progress if interrupted. Since every save rewrites the full dataset collected so far (not just the newest batch), a single failed save is always caught up by the next one.
- **Safe against a locked output file**: if the Excel file is open elsewhere (e.g. you opened it in Excel mid-run) a save attempt raises `PermissionError`; this is caught, logged, and shown on screen, and the run keeps going instead of crashing — the data isn't lost, it's just written on the next successful save.
- **Shared session**: reuses a single `requests.Session()` (with custom headers) across all requests for the whole run, closed cleanly at the end.
- **Logging**: all warnings (missing fields) and errors (failed requests) are written to a log file with timestamps, so a run can be audited afterwards.

## Tech stack

- [Requests](https://docs.python-requests.org/) — HTTP requests
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) — HTML parsing
- [pandas](https://pandas.pydata.org/) — data structuring and Excel export
- Python's built-in `logging` module

## Project structure

```
.
├── european_companies.py       # main script
├── config_europe_lead.py       # site-specific config (headers, CSS selectors, countries, timeouts)
├── requirements.txt
└── script_european_companies.log   # created on first run
```

`config_europe_lead.py` keeps everything that depends on the target site separate from the scraping logic itself:

- `HEADERS` — a browser-like `User-Agent`, `Accept-Encoding`, and `Accept-Language`, sent with every request.
- `SELECTORS_FIRST_PAGE` — the HTML tag/class pairs used to locate each field: `name`, `location`, `tag`, `year` on the listing page, and `funding`/`description` on each company's own page, plus two shared entries: `second_tag`, the `div.value` element every field block uses to hold its actual value, and `link`/`link_second`, used to reach the nested `<a href>` inside the company name block.
- `COUNTRIES` — a dictionary mapping 30 European countries to their EU-Startups directory URL slugs. Most follow a `<country>-startups` pattern, but a few are irregular (e.g. Slovakia's slug has no `-startups` suffix) — kept as an explicit lookup instead of generating the slug from the country name.
- `TIMEOUT = (3, 10)` — connect/read timeout tuple for every request.
- `SLEEP_TIME = 2` — seconds to wait between requests.

## Installation

```bash
git clone <this-repo-url>
cd <this-repo-folder>
pip install -r requirements.txt
```

## Usage

```bash
python european_companies.py
```

You'll be prompted for:

1. **Country** — must match one of the countries defined in `config_europe_lead.py`.
2. **Number of companies** — how many leads to collect (positive integer).

The script will:

1. Walk the paginated directory listing for the chosen country, collecting name, location, foundation year, tags, and link for each company until it has enough (or runs out of pages).
2. Visit each company's own page to fetch its funding and description, saving progress to Excel every 10 companies.
3. Write the final result to `Lead_{country}_companies.xlsx`.

## Building a standalone executable

The script is plain CLI Python (no GUI), so it can be packaged into a standalone executable with [PyInstaller](https://pyinstaller.org/):

```bash
python -m PyInstaller --onefile european_companies.py
```

Running the resulting executable opens a console window and behaves exactly like running the script directly — the country/quantity prompts still read from that console.

This creates a `build/` and `dist/` folder plus a `.spec` file — these are PyInstaller artifacts and shouldn't be committed to the repo.

## Output

An Excel file (`Lead_{country}_companies.xlsx`) with one row per company and the following columns:

| Name | Based in | Foundation year | Funding | Description | Tags | Direct link |
|------|----------|------------------|---------|--------------|------|-------------|

## Scraping etiquette

- Requests are spaced out with a configurable delay (`SLEEP_TIME`) between calls.
- A shared session with descriptive headers is used instead of firing anonymous one-off requests.
- The target site's `robots.txt` was checked before building this: it does not disallow the directory pages used here.

## Known limitations / possible improvements

- Retry logic currently covers the listing-page requests only; the detail-page requests (funding and description lookup) log an error and skip the company on failure rather than retrying.
- Pagination stop condition relies on an empty results list rather than a fixed page count, which keeps it adaptable to different countries with different numbers of listed companies.
- Description text isn't normalized for extra whitespace beyond quote removal.

## Disclaimer

This repository is shared for portfolio/demonstration purposes. It contains the scraper's source code only — not any real data collected with it. If you use this code, make sure your use of the target site complies with its terms of use and `robots.txt` at the time you run it.
