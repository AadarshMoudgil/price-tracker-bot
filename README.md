# 🛒 Price Tracker Bot

## Description
A Python automation script that tracks product prices from e-commerce websites and saves them in a CSV file with timestamps.  
This project demonstrates **web scraping + automation** with a clean, GitHub-ready structure.

## Client's Need
Manually checking competitor prices is time-consuming and error-prone.  
Clients often want **automated price monitoring** to help with pricing strategy and market analysis.

## Solution
- Config-driven scraper (`config.yaml`) for product URLs and CSS selectors.
- Fetches web pages, extracts product prices, and appends them to a CSV.
- Run manually when needed.

## Outcome / Impact
- Saves hours of manual monitoring.
- Creates a historical CSV for analysis.
- Can be extended for alerts, dashboards, or competitor analytics.

## Files
- `main.py`: Main script to scrape prices.
- `config.yaml`: Config file for product list and selectors.
- `requirements.txt`: Dependencies.
- `prices.csv`: Generated CSV with historical data.

