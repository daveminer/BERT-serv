import json
import numpy
import pytest
from .tasks import run_sentiment, send_webhook

@pytest.mark.django_db
def test_run_sentiment(mocker):
    mock_finbert = mocker.patch('sentiment.tasks.finbert')

    fake_finbert_return = numpy.array(
        [[ 3.6286101, -4.290355, -2.529494 ], [ -1.0189443, 4.5508056, -5.3832393]]
    )
    mock_finbert().__getitem__().detach().numpy.return_value = fake_finbert_return

    mock_results = run_sentiment.s(
        [
            (100, ["tag one", "tag two"], "Stonks go up."),
            (101, ["tag three", "tag four"], "For great justice.")
        ]
    ).apply().get()

    assert mock_results == [
            {"article_id": 100, "sentiment": {"label": "Neutral", "score": 0.9975261092185974, "tags": ["tag one", "tag two"]}},
            {"article_id": 101, "sentiment": {"label": "Positive", "score": 0.9961548447608948, "tags": ["tag three", "tag four"]}}
        ]


def test_send_webhook(mocker):
    mock_post = mocker.patch('sentiment.tasks.requests.post')
    send_webhook.s({"test": "value"}, "http://test--url.com").apply()

    mock_post.assert_called_with("http://test--url.com", json={"results": {"test": "value"}})
