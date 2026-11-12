from __future__ import annotations

import time
from typing import Any

import httpx

BASE_URL = "https://api.gdeltproject.org/api/v2/doc/doc"
NEWS_QUERY = (
    'sourcelang:English ("stock market" OR "Federal Reserve" OR "Bank of Canada" OR inflation '
    'OR "interest rates" OR oil OR tariffs OR earnings OR recession)'
)


def fetch_news() -> list[dict[str, Any]]:
    articles: list[dict[str, Any]] = []
    seen_urls: set[str] = set()

    try:
        with httpx.Client(timeout=45) as client:
            for attempt in range(3):
                try:
                    response = client.get(
                        BASE_URL,
                        params={
                            "query": NEWS_QUERY,
                            "mode": "ArtList",
                            "format": "json",
                            "sort": "HybridRel",
                            "maxrecords": 50,
                            "timespan": "24h",
                        },
                    )
                    response.raise_for_status()
                    data = response.json()
                    break
                except httpx.HTTPStatusError as exc:
                    if exc.response.status_code == 429 and attempt < 2:
                        time.sleep(5 * (attempt + 1))
                        continue
                    raise

            for item in data.get("articles", []):
                url = item.get("url")
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                articles.append({
                    "title": item.get("title", ""),
                    "url": url,
                    "domain": item.get("domain", ""),
                    "published": item.get("seendate", ""),
                    "language": item.get("language", ""),
                })
    except (httpx.HTTPError, ValueError) as exc:
        print(f"News collection error: {exc}")
    return articles
