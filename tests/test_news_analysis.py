from marketwatch.analysis.news_analysis import analyze_news


def test_relevant_news_ranks_higher():
    articles = [
        {"title": "New movie releases this week", "published": "20261110"},
        {"title": "Federal Reserve announces interest rate decision", "published": "20261110"},
        {"title": "Local sports update", "published": "20261110"},
    ]
    results = analyze_news(articles)
    assert "Federal Reserve" in results[0]["title"]


def test_empty_news():
    results = analyze_news([])
    assert results == []
