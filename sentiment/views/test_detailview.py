import json
import pytest
from django.test import Client
from sentiment.models import Sentiment
from sentiment.test_helpers import create_sentiment

@pytest.mark.django_db
def test_sentiment_detail_view(mocker):
    client = Client()
    sentiment = create_sentiment(label='test-label', text='test-text', tags=['test-tag'])

    response = client.get(f"/sentiment/{sentiment.id}/", HTTP_ACCEPT='application/json')

    assert response.status_code == 200

    json_response = response.json()
    assert json_response['label'] == 'test-label'
    assert json_response['text'] == 'test-text'
    assert json_response['tags'] == ['test-tag']
    assert json_response['score'] < 1.0 and json_response['score'] > -1.0
