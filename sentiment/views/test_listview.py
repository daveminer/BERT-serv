import json
import numpy
import pytest
import random
from django.test import Client, override_settings
from sentiment.models import Sentiment

@pytest.mark.django_db
def test_get(mocker):
    client = Client()
    __create_sentiment(label='test-label', text='test-text-two', tags=['test-tag'])
    __create_sentiment(label='test-label-two', text='test-text-two', tags=['test-tag', 'other-test-tag'])

    response = client.get("/sentiment/", {'tags': ['test-tag', 'another-tag'], 'period': 30}, HTTP_ACCEPT='application/json')

    assert response.status_code == 200

    json = response.json()
    assert json[0]['label'] == 'test-label-two'
    assert json[0]['score'] < 1.0 and json[0]['score'] > -1.0
    assert json[1]['label'] == 'test-label'


def __create_sentiment(label, text, score=None, tags=None):
    if score is None:
        score = random.uniform(-1.0, 1.0)  # Generate a random score between -1.0 and 1.0
    if tags is None:
        tags = []  # Set tags to an empty list if not provided

    Sentiment.objects.create(
        label=label,
        score=score,
        tags=tags,
        text=text
    )