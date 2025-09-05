
#!/usr/bin/env python3
"""
Price Tracker Bot — main.py
Reads config.yaml, scrapes product pages for prices, appends results to prices.csv.
"""

import os
import csv
import sys
import time
import yaml
import requests
from datetime import datetime
from bs4 import BeautifulSoup

# Browser-like header to reduce chance of immediate blocking
DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/122.0.0.0 Safari/537.36"
    )
}

def load_config(path="config.yaml"):
    if not os.path.exists(path):
        print(f"[ERROR] Config file not found: {path}")
        sys.exit(1)
    with open(path, "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f) or {}
    products = cfg.get("products", [])
    if not products:
        print("[ERROR] No products defined in config.yaml")
        sys.exit(1)
    for p in products:
        if not all(k in p for k in ("name", "url", "price_selector")):
            raise ValueError("Each product must include: name, url, price_selector")
    return cfg

def fetch_html(url, timeout=15, retries=2, backoff=2):
    last_exc = None
    for attempt in range(retries + 1):
        try:
            resp = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            last_exc = e
            if attempt < retries:
                time.sleep(backoff * (attempt + 1))
    raise last_exc

def extract_price(html, selector):
    soup = BeautifulSoup(html, "html.parser")
    el = soup.select_one(selector)
    if not el:
        return None
    return el.get_text(strip=True)

def ensure_output(output_path):
    if not os.path.exists(output_path):
        # Create file and write header
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["timestamp", "product", "price", "url"])

def append_row(output_path, row):
    with open(output_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(row)

def main():
    cfg = load_config()
    output_path = cfg.get("output_csv", "prices.csv")
    ensure_output(output_path)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    for p in cfg["products"]:
        name = p["name"]
        url = p["url"]
        selector = p["price_selector"]
        try:
            html = fetch_html(url)
            price = extract_price(html, selector)
            price_display = price if price is not None else "N/A"
            print(f"{name}: {price_display}")
            append_row(output_path, [timestamp, name, price_display, url])
        except Exception as e:
            err_text = f"ERROR: {e}"
            print(f"{name}: {err_text}")
            append_row(output_path, [timestamp, name, err_text, url])

    print(f"✅ Saved results to: {output_path}")

if __name__ == "__main__":
    main()
