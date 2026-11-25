"""Collect daily mandi prices for several commodities over a date range.
Resumable: any day that already has a file is skipped."""

import os
import time
from datetime import date, timedelta
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# --- Setup -------------------------------------------------------------
load_dotenv()
API_KEY = os.getenv("DATA_GOV_API")
if not API_KEY:
    raise SystemExit("API key not found. Check your .env file.")

URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"
COMMODITIES = ["Tomato", "Onion"]
START_DATE = date(2026, 10, 1)  # test with a SHORT range first (one week)
END_DATE = date(2026, 10, 7)
PAGE_SIZE = 1000
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
    "Accept": "application/json",
}
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"


# --- Functions -----------------------------------------------------------
def get_page(commodity, date_str, offset, retries=3):
    """Return one page of results, or None if every retry fails."""
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": PAGE_SIZE,
        "offset": offset,
        "filters[Commodity]": commodity,
        "filters[Arrival_Date]": date_str,
    }
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(URL, params=params, headers=HEADERS, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            print(f"    Attempt {attempt} failed: HTTP {error.response.status_code}")
        except requests.exceptions.RequestException as error:
            print(f"    Attempt {attempt} failed: {type(error).__name__}")
        time.sleep(5 * attempt)
    return None  # Rule 2: report the failure, but don't stop the whole script


def fetch_day(commodity, date_str):
    """Return all records for one commodity on one day, or None if it failed."""
    all_records = []
    offset = 0
    while True:
        data = get_page(commodity, date_str, offset)
        if data is None:
            return None
        records = data["records"]
        all_records.extend(records)
        if len(records) < PAGE_SIZE:
            return all_records
        offset += PAGE_SIZE
        time.sleep(1)


# --- Main loop -------------------------------------------------------------
failed = []
current = START_DATE

while current <= END_DATE:
    date_str = current.strftime("%d-%m-%Y")  # the API wants dd-MM-yyyy

    for commodity in COMMODITIES:
        out_file = (
            RAW_DIR
            / commodity.lower()
            / f"{commodity.lower()}_{current.isoformat()}.csv"
        )  # ← GAP 1

        if out_file.exists():  # ← GAP 2
            print(f"{commodity} {date_str}: already done, skipping")
            continue

        records = fetch_day(commodity, date_str)

        if records is None:
            failed.append((commodity, date_str))  # ← GAP 3
            print(f"{commodity} {date_str}: FAILED, will retry on next run")
            continue

        # Rule 3: save even when empty (an empty file means "checked, no data")
        df = pd.DataFrame(records)
        out_file.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(out_file, index=False)
        print(f"{commodity} {date_str}: saved {len(df)} rows")
        time.sleep(1)

    current = current + timedelta(days=1)  # ← GAP 4

print(f"\nDone. Failed: {len(failed)}")
for item in failed:
    print("  ", item)
