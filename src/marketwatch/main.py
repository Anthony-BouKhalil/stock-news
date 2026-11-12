from __future__ import annotations

from dotenv import load_dotenv

from marketwatch.analysis.market_analysis import analyze_exchange_rate, analyze_market_data
from marketwatch.analysis.news_analysis import analyze_news
from marketwatch.config import load_settings
from marketwatch.reporting.email_sender import send_email
from marketwatch.reporting.email_template import build_email
from marketwatch.sources.bank_of_canada import fetch_usd_cad
from marketwatch.sources.fred import fetch_market_data
from marketwatch.sources.gdelt import fetch_news
from marketwatch.utils.dates import report_date


def main() -> None:
    load_dotenv()
    settings = load_settings()
    print("Starting MarketWatch AI...")

    print("Fetching FRED data...")
    market_data = fetch_market_data(settings.fred_api_key)

    print("Fetching USD/CAD data...")
    exchange_data = fetch_usd_cad()

    print("Fetching financial news...")
    news_data = fetch_news()

    markets = analyze_market_data(market_data)
    exchange_rate = analyze_exchange_rate(exchange_data)
    articles = analyze_news(news_data, limit=10)

    market_names = {"S&P 500", "Nasdaq Composite", "Dow Jones", "VIX", "WTI Oil"}
    economic_indicators = [
        item for item in markets if item["name"] not in market_names
    ]

    html = build_email(
        markets=markets,
        economics=economic_indicators,
        exchange_rate=exchange_rate,
        articles=articles,
    )

    subject = f"MarketWatch AI Report - {report_date()}"
    send_email(
        smtp_host=settings.smtp_host,
        smtp_port=settings.smtp_port,
        smtp_username=settings.smtp_username,
        smtp_password=settings.smtp_password,
        email_to=settings.email_to,
        email_from=settings.email_from,
        subject=subject,
        html=html,
    )


if __name__ == "__main__":
    main()
