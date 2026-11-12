import pytest

from marketwatch.analysis.market_analysis import analyze_series, percentage_change


def test_positive_percentage_change():
    assert percentage_change(110, 100) == 10


def test_negative_percentage_change():
    assert percentage_change(90, 100) == -10


def test_zero_previous_value():
    assert percentage_change(100, 0) is None


def test_analyze_daily_series():
    series = {
        "observations": [
            {"date": "2026-11-10", "value": 110},
            {"date": "2026-11-09", "value": 100},
            {"date": "2026-11-06", "value": 98},
            {"date": "2026-11-05", "value": 97},
            {"date": "2026-11-04", "value": 96},
            {"date": "2026-11-03", "value": 90},
        ]
    }
    result = analyze_series("S&P 500", series)
    assert result["latest"] == 110
    assert result["daily_change"] == 10
    assert result["weekly_change"] == pytest.approx(22.2222, rel=1e-3)


def test_empty_series():
    result = analyze_series("S&P 500", {"observations": []})
    assert result["latest"] is None
    assert result["error"] is not None
