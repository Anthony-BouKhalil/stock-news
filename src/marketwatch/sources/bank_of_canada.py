from __future__ import annotations

from typing import Any

import httpx

BASE_URL = "https://www.bankofcanada.ca/valet/observations"


def fetch_usd_cad() -> dict[str, Any]:
    url = f"{BASE_URL}/FXUSDCAD/json"
    try:
        with httpx.Client(timeout=30) as client:
            response = client.get(url, params={"recent": 5})
            response.raise_for_status()
            data = response.json()
    except (httpx.HTTPError, ValueError):
        return {"observations": []}

    observations: list[dict[str, Any]] = []
    for item in data.get("observations", []):
        value = item.get("FXUSDCAD", {}).get("v")
        if value is None:
            continue
        try:
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue
        observations.append({
            "date": item.get("d"),
            "value": numeric_value,
        })
    return {"observations": observations}
