# MarketWatch AI

Automated daily market report generator that pulls FRED data, Bank of Canada FX rates, and GDELT financial news, analyzes the trends, and emails a formatted HTML summary.

## Features

- Python 3.12
- Scheduled GitHub Actions workflow for weekdays at 7:30 AM Toronto time
- FRED API for market and economic indicators
- Bank of Canada Valet API for USD/CAD data
- GDELT for finance-related news
- SMTP email delivery via Gmail or another SMTP provider
- Pytest coverage for the market and news analysis logic

## Setup

1. Create a virtual environment and install dependencies:
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
2. Copy `.env.example` to `.env` and fill in the required values.
3. Run the app locally:
   PYTHONPATH=src python -m marketwatch.main

## Testing

pytest -q
