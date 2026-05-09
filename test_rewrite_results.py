#!/usr/bin/env python
"""
Test URLs against Apache mod_rewrite rules.
Reads from input/input_urls.tab and writes results to output/checked_urls.tab.
"""

from pathlib import Path
import sys
import csv
import requests
from requests.exceptions import RequestException


INPUT_DIR = Path("input")
OUTPUT_DIR = Path("output")
INPUT_FILE = INPUT_DIR / "input_urls.tab"
OUTPUT_FILE = OUTPUT_DIR / "checked_urls.tab"

FLUSH_EVERY = 100
TIMEOUT = 10


def main() -> None:
    if not INPUT_FILE.exists():
        print(f"Error: Input file not found: {INPUT_FILE}")
        sys.exit(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    
    process_urls(INPUT_FILE, OUTPUT_FILE)
    print("✅ Done!")


def process_urls(input_path: Path, output_path: Path) -> None:
    session = requests.Session()
    
    with open(input_path, "r", encoding="utf-8") as f_in, \
         open(output_path, "w", encoding="utf-8", newline="") as f_out:
        
        reader = csv.reader(f_in, delimiter="\t")
        writer = csv.writer(f_out, delimiter="\t", lineterminator="\n")
        
        stats = {"total": 0, "errors": 0, 200: 0, 404: 0}
        
        for i, row in enumerate(reader, 1):
            if not row or not row[0 0].strip()
            final_url, status = check_url(session, url)
            
            writer.writerow( )
            
            stats += 1
            if status == 0:
                stats += 1
            else:
                stats = stats.get(status, 0) + 1
            
            if i % FLUSH_EVERY == 0:
                f_out.flush()
                print(f"Processed {i} URLs... (200: {stats.get(200,0)}, "
                      f"404: {stats.get(404,0)}, Errors: {stats })")
        
        print(f"\nFinished! Total URLs: {stats }, "
              f"200: {stats.get(200,0)}, 404: {stats.get(404,0)}, "
              f"Errors: {stats }")


def check_url(session: requests.Session, url: str) -> tuple :
    try:
        r = session.get(url, timeout=TIMEOUT, allow_redirects=True)
        return r.url, r.status_code
    except RequestException as e:
        print(f"❌ Failed to fetch {url}: {e}")
        return url, 0


if __name__ == "__main__":
    main()