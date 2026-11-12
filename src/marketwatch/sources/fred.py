from __future__ import annotations

from datetime import date, timedelta
from typing import Any

import httpx

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"

SERIES = {
    "S&P 500": "SP500",
    "Nasdaq Composite": "NASDAQCOM",
    "Dow Jones": "DJIA",
    "VIX": "VIXCLS",
    "10-Year Treasury Yield": "DGS10",
    "US CPI": "CPIAUCSL",
    "US Unemployment": "UNRATE",
    "WTI Oil": "DCOILWTICO",
}


def fetch_series(
    client: httpx.Client,
    api_key: str,
    series_id: str,
) -> list[dict[str, Any]]:
    start_date = date.today() - timedelta(days=400)
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": "json",
        "observation_start": start_date.isoformat(),
        "sort_order": "desc",
        "limit": 20,
    }
    response = client.get(BASE_URL, params=params)
    response.raise_for_status()
    data = response.json()

    observations: list[dict[str, Any]] = []
    for item in data.get("observations", []):
        value = item.get("value")
        if value in (None, "") or value == "NA":
            continue
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue
        observations.append({
            "date": item.get("date"),
            "value": numeric_value,
        })
    return observations


def fetch_market_data(
    api_key: str,
    client: httpx.Client | None = None,
) -> dict[str, dict[str, Any]]:
    if client is None:
        with httpx.Client(timeout=30) as active_client:
            return fetch_market_data(api_key, client=active_client)

    market_data: dict[str, dict[str, Any]] = {}
    for name, series_id in SERIES.items():
        market_data[name] = {"observations": fetch_series(client, api_key, series_id)}
    return market_data
