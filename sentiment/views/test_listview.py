import json
import numpy
import pytest
from django.test import Client, override_settings
from sentiment.models import Sentiment
from sentiment.test_helpers import create_sentiment

@pytest.mark.django_db
def test_get(mocker):
    client = Client()

    create_sentiment(label='test-label', text='test-text-two', tags=['test-tag'])
    create_sentiment(label='test-label-two', text='test-text-two', tags=['test-tag', 'other-test-tag'])

    response = client.get("/sentiment/", {'tags': ['test-tag', 'another-tag'], 'period': 30}, HTTP_ACCEPT='application/json')

    assert response.status_code == 200

    json = response.json()
    assert json[0]['label'] == 'test-label-two'
    assert json[0]['score'] < 1.0 and json[0]['score'] > -1.0
    assert json[1]['label'] == 'test-label'
