import httpx

from marketwatch.sources import gdelt


def test_fetch_news_retries_rate_limit_and_fetches_one_combined_query(monkeypatch):
    request = httpx.Request("GET", gdelt.BASE_URL)
    rate_limited = httpx.Response(429, request=request)
    successful = httpx.Response(
        200,
        json={
            "articles": [
                {
                    "title": "Markets respond to inflation data",
                    "url": "https://example.com/markets",
                    "domain": "example.com",
                    "seendate": "20261112T010000Z",
                    "language": "English",
                }
            ]
        },
        request=request,
    )

    class FakeClient:
        def __init__(self, **_kwargs):
            self.responses = iter([rate_limited, successful])
            self.calls = []

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return False

        def get(self, url, params):
            self.calls.append((url, params))
            return next(self.responses)

    fake_client = FakeClient()
    monkeypatch.setattr(gdelt.httpx, "Client", lambda **kwargs: fake_client)
    sleeps = []
    monkeypatch.setattr(gdelt.time, "sleep", sleeps.append)

    articles = gdelt.fetch_news()

    assert len(fake_client.calls) == 2
    assert fake_client.calls[0][1]["maxrecords"] == 50
    assert "sourcelang:English" in fake_client.calls[0][1]["query"]
    assert len(articles) == 1
    assert articles[0]["title"] == "Markets respond to inflation data"
    assert sleeps == [5]
