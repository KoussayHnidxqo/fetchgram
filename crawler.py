import argparse
import csv
import hashlib
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

CACHE = Path(".cache/pages")
CACHE.mkdir(parents=True, exist_ok=True)


def fetch(url, delay=1.0, tries=3):
    # polite fetch with on-disk cache and backoff retries
    key = hashlib.sha1(url.encode()).hexdigest()
    hit = CACHE / (key + ".html")
    if hit.exists():
        return hit.read_text(encoding="utf-8", errors="ignore")
    for attempt in range(tries):
        try:
            r = requests.get(url, timeout=15,
                             headers={"User-Agent": "crawl-study/0.2"})
            r.raise_for_status()
            hit.write_text(r.text, encoding="utf-8")
            time.sleep(delay)
            return r.text
        except requests.RequestException:
            time.sleep(2 ** attempt)
    return ""


def parse_listing(html, base):
    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for a in soup.select("h2 a, h3 a, article a"):
        title = a.get_text(strip=True)
        href = urljoin(base, a.get("href", ""))
        if title and urlparse(href).scheme in ("http", "https"):
            rows.append({"title": title, "url": href})
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("start")
    ap.add_argument("--pages", type=int, default=3)
    ap.add_argument("--out", default="out.csv")
    args = ap.parse_args()

    urls = [args.start] + ["%s?page=%d" % (args.start, i)
                           for i in range(2, args.pages + 1)]
    rows = []
    with ThreadPoolExecutor(max_workers=4) as pool:
        for html in pool.map(fetch, urls):
            if html:
                rows.extend(parse_listing(html, args.start))
    with open(args.out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["title", "url"])
        w.writeheader()
        w.writerows(rows)
    print("wrote %d rows -> %s" % (len(rows), args.out))


if __name__ == "__main__":
    main()
