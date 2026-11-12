from __future__ import annotations

from typing import Any

DAILY_MARKET_SERIES = {
    "S&P 500",
    "Nasdaq Composite",
    "Dow Jones",
    "VIX",
    "WTI Oil",
}


def percentage_change(current: float, previous: float) -> float | None:
    if previous in (None, 0):
        return None
    try:
        current_value = float(current)
        previous_value = float(previous)
    except (TypeError, ValueError):
        return None
    if previous_value == 0:
        return None
    return ((current_value - previous_value) / previous_value) * 100


def analyze_series(name: str, series: dict[str, Any]) -> dict[str, Any]:
    observations = series.get("observations", [])
    if not observations:
        return {
            "name": name,
            "latest": None,
            "date": None,
            "daily_change": None,
            "weekly_change": None,
            "error": "No observations available",
        }

    latest = observations[0]
    daily_change = None
    weekly_change = None
    if name in DAILY_MARKET_SERIES:
        if len(observations) >= 2:
            daily_change = percentage_change(
                latest["value"],
                observations[1]["value"],
            )
        if len(observations) >= 6:
            weekly_change = percentage_change(
                latest["value"],
                observations[5]["value"],
            )

    return {
        "name": name,
        "latest": latest["value"],
        "date": latest["date"],
        "daily_change": daily_change,
        "weekly_change": weekly_change,
        "error": None,
    }


def analyze_market_data(market_data: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    results = []
    for name, series in market_data.items():
        results.append(analyze_series(name, series))
    return results


def analyze_exchange_rate(exchange_data: dict[str, Any]) -> dict[str, Any]:
    return analyze_series("USD/CAD", exchange_data)
