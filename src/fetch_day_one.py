"""Fetch one day of mandi prices for one commodity, page by page, and save it as a CSV."""

import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

# 1. Read the API key from .env
load_dotenv()
API_KEY = os.getenv("DATA_GOV_API")
if not API_KEY:
    raise SystemExit("API key not found. Check your .env file.")

# 2. Settings: change these to fetch something else
URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"
COMMODITY = "Tomato"
DATE = "24-10-2026"  # dd-MM-yyyy
PAGE_SIZE = 100  # rows per request (small = easier for the server)


def get_page(offset, retries=3):
    """Request one page of results. Retry if the server fails."""
    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": PAGE_SIZE,
        "offset": offset,
        "filters[Commodity]": COMMODITY,
        "filters[Arrival_Date]": DATE,
    }
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(URL, params=params, timeout=120)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as error:
            # Show the status code and the start of the server's reply (no URL, so no key)
            status = error.response.status_code
            print(
                f"  Attempt {attempt} failed: HTTP {status}: {error.response.text[:150]}"
            )
            time.sleep(5 * attempt)
        except requests.exceptions.RequestException as error:
            print(f"  Attempt {attempt} failed: {type(error).__name__}")
            time.sleep(5 * attempt)
    raise SystemExit("All retries failed. The server may be down; try again later.")


# 3. Fetch every page until there are no more records
all_records = []
offset = 0
while True:
    data = get_page(offset)
    records = data["records"]
    all_records.extend(records)
    print(
        f"Offset {offset}: got {len(records)} records (total available: {data['total']})"
    )

    if len(records) < PAGE_SIZE:  # a short page means it was the last one
        break
    offset += PAGE_SIZE
    time.sleep(1)  # pause between requests to be polite to the server

# 4. Save as CSV (the file name follows the settings automatically)
df = pd.DataFrame(all_records)
print(f"\nCollected {len(df)} rows in total")
print(df.head())

out_dir = Path("data/raw")
out_dir.mkdir(parents=True, exist_ok=True)
out_file = out_dir / f"{COMMODITY.lower()}_{DATE}.csv"
df.to_csv(out_file, index=False)
print("Saved to", out_file)
