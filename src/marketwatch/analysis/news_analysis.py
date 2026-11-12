from __future__ import annotations

from typing import Any

KEYWORDS: dict[str, int] = {
    "federal reserve": 5,
    "interest rate": 5,
    "inflation": 5,
    "recession": 5,
    "employment": 4,
    "unemployment": 4,
    "earnings": 4,
    "stock market": 3,
    "economy": 3,
    "bank of canada": 5,
    "oil": 2,
    "tariff": 3,
    "trade": 2,
}


def calculate_relevance(article: dict[str, Any]) -> int:
    title = article.get("title", "").lower()
    score = 0
    for keyword, weight in KEYWORDS.items():
        if keyword in title:
            score += weight
    return score


def analyze_news(articles: list[dict[str, Any]], limit: int = 10) -> list[dict[str, Any]]:
    scored_articles = []
    for article in articles:
        scored = article.copy()
        scored["relevance_score"] = calculate_relevance(article)
        scored_articles.append(scored)
    scored_articles.sort(
        key=lambda item: (
            item["relevance_score"],
            item.get("published", ""),
        ),
        reverse=True,
    )
    return scored_articles[:limit]
