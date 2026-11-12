from __future__ import annotations

from html import escape
from typing import Any


def _format_change(value: float | None) -> str:
    if value is None:
        return "N/A"
    return f"{value:+.2f}%"


def _render_table(rows: list[str], title: str) -> str:
    return (
        "<div style=\"margin: 0 0 24px;\">"
        f"<h2 style=\"margin: 0 0 12px; font-size: 18px;\">{title}</h2>"
        "<table style=\"border-collapse: collapse; width: 100%; font-family: Arial, sans-serif; font-size: 14px;\">"
        + "\n".join(rows)
        + "</table></div>"
    )


def build_market_table(market_items: list[dict[str, Any]]) -> str:
    header = (
        "<thead><tr style=\"background: #f3f6fb;\">"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: left;\">Market</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">Latest</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">Daily</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">Weekly</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: left;\">Date</th>"
        "</tr></thead><tbody>"
    )
    body_rows = []
    for item in market_items:
        body_rows.append(
            "<tr>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee;\">{escape(str(item.get('name', '')))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">{escape(str(item.get('latest', 'N/A')))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">{_format_change(item.get('daily_change'))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">{_format_change(item.get('weekly_change'))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee;\">{escape(str(item.get('date', 'N/A')))}</td>"
            "</tr>"
        )
    return _render_table([header + "\n".join(body_rows) + "</tbody>"], "Market Snapshot")


def build_economic_table(economic_items: list[dict[str, Any]]) -> str:
    header = (
        "<thead><tr style=\"background: #f3f6fb;\">"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: left;\">Indicator</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">Latest</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">Daily</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">Weekly</th>"
        "<th style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: left;\">Date</th>"
        "</tr></thead><tbody>"
    )
    body_rows = []
    for item in economic_items:
        body_rows.append(
            "<tr>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee;\">{escape(str(item.get('name', '')))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">{escape(str(item.get('latest', 'N/A')))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">{_format_change(item.get('daily_change'))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee; text-align: right;\">{_format_change(item.get('weekly_change'))}</td>"
            f"<td style=\"padding: 10px; border: 1px solid #d8e1ee;\">{escape(str(item.get('date', 'N/A')))}</td>"
            "</tr>"
        )
    return _render_table([header + "\n".join(body_rows) + "</tbody>"], "Economic Indicators")


def build_news_section(articles: list[dict[str, Any]]) -> str:
    if not articles:
        return "<p style=\"color: #555;\">No recent financial news available at the moment.</p>"

    items: list[str] = []
    for index, article in enumerate(articles[:10], start=1):
        title = escape(str(article.get("title", "Untitled")))
        url = article.get("url") or "#"
        domain = escape(str(article.get("domain", "")))
        items.append(
            f"<li style=\"margin-bottom: 8px;\"><strong>{index}.</strong> "
            f"<a href=\"{escape(url, quote=True)}\" style=\"color: #0b5ed7; text-decoration: none;\">{title}</a>"
            f" <span style=\"color: #666;\">({domain})</span></li>"
        )
    return "<ul style=\"margin: 0; padding-left: 20px;\">" + "\n".join(items) + "</ul>"


def build_email(
    markets: list[dict[str, Any]],
    economics: list[dict[str, Any]],
    exchange_rate: dict[str, Any],
    articles: list[dict[str, Any]],
) -> str:
    return """
    <html>
      <body style="margin: 0; background: #f6f8fb; font-family: Arial, sans-serif; color: #1c2430;">
        <div style="max-width: 900px; margin: 24px auto; background: white; padding: 32px; border-radius: 10px; box-shadow: 0 2px 12px rgba(0,0,0,0.06);">
          <h1 style="margin-top: 0; font-size: 28px; color: #1c2430;">MarketWatch AI Report</h1>
          <p style="margin: 0 0 16px; color: #4a5568;">Generated for the latest market snapshot.</p>
          {market_table}
          {economic_table}
          <h2 style="margin: 0 0 12px; font-size: 18px;">Currency</h2>
          <table style="border-collapse: collapse; width: 100%; max-width: 360px; font-family: Arial, sans-serif; font-size: 14px; margin-bottom: 24px;">
            <tr>
              <th style="padding: 10px; border: 1px solid #d8e1ee; background: #f3f6fb; text-align: left;">Exchange Rate</th>
              <th style="padding: 10px; border: 1px solid #d8e1ee; background: #f3f6fb; text-align: right;">Latest Value</th>
              <th style="padding: 10px; border: 1px solid #d8e1ee; background: #f3f6fb; text-align: left;">Observation Date</th>
            </tr>
            <tr>
              <td style="padding: 10px; border: 1px solid #d8e1ee;">USD/CAD</td>
              <td style="padding: 10px; border: 1px solid #d8e1ee; text-align: right;">{latest_value}</td>
              <td style="padding: 10px; border: 1px solid #d8e1ee;">{observation_date}</td>
            </tr>
          </table>
          <h2 style="margin: 0 0 12px; font-size: 18px;">Financial News</h2>
          {news_section}
          <div style="margin-top: 28px; padding-top: 16px; border-top: 1px solid #e5eaf2; color: #5b6475; font-size: 13px;">
            <p style="margin: 0 0 8px;">This report is for informational and educational purposes only. It is not investment advice.</p>
            <p style="margin: 0;">Market data may be delayed. Economic indicators reflect their latest published observation dates.</p>
          </div>
        </div>
      </body>
    </html>
    """.format(
        market_table=build_market_table(markets),
        economic_table=build_economic_table(economics),
        latest_value=escape(str(exchange_rate.get("latest", "N/A"))),
        observation_date=escape(str(exchange_rate.get("date", "N/A"))),
        news_section=build_news_section(articles),
    )
