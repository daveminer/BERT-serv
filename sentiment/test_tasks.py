import json
import numpy
import pytest
from .tasks import run_sentiment, send_webhook
import logging

@pytest.fixture(autouse=True)
def mock_logger(mocker):
    """Mock the logger for all tests."""
    mock_logger = mocker.MagicMock(spec=logging.Logger)
    mocker.patch('sentiment.tasks.logger', mock_logger)
    return mock_logger

@pytest.mark.django_db
def test_run_sentiment(mocker, mock_logger):
    mock_finbert = mocker.patch('sentiment.tasks.finbert')

    fake_finbert_return = numpy.array(
        [[ 3.6286101, -4.290355, -2.529494 ], [ -1.0189443, 4.5508056, -5.3832393]]
    )
    mock_finbert().__getitem__().detach().numpy.return_value = fake_finbert_return

    result = run_sentiment.s(
        [
            (100, ["tag one", "tag two"], "Stonks go up."),
            (101, ["tag three", "tag four"], "For great justice.")
        ]
    ).apply().get()

    assert result == [{'article_id': 100, 'sentiment': {'label': 'Neutral', 'score': 0.9975261092185974, 'tags': ['tag one', 'tag two']}}, {'article_id': 101, 'sentiment': {'label': 'Positive', 'score': 0.9961548447608948, 'tags': ['tag three', 'tag four']}}]
    mock_logger.info.assert_called_with("Successfully saved sentiments", extra={
        "saved_count": 2,
        "task_name": "run_sentiment"
    })

def test_send_webhook(mocker, mock_logger):
    mock_post = mocker.patch('sentiment.tasks.requests.post')
    mock_post.return_value.status_code = 200

    send_webhook.s({"test": "value"}, "http://test--url.com").apply().get()

    mock_post.assert_called_with("http://test--url.com", json={"results": {"test": "value"}})
    mock_logger.info.assert_called_with("Webhook sent successfully", extra={'status_code': 200, 'task_name': 'send_webhook'})
