from .celery import Celery
from .models import Sentiment
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
import json
import numpy as np
import requests

celery = Celery()

model = 'yiyanghkust/finbert-tone'

finbert = BertForSequenceClassification.from_pretrained(
    model, num_labels=3)

tokenizer = BertTokenizer.from_pretrained(model)

nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)

@celery.task
def run_sentiment(sentences, tags):
    results = nlp(sentences)

    sentiment_objects = []

    for idx, result in enumerate(results):
        label = result['label']
        score = result['score']
        sentiment = Sentiment(
            label=label,
            text=sentences[idx],
            score=score,
            tags=tags
        )
        sentiment_objects.append(sentiment)

    # Bulk create all sentiment objects in one query
    Sentiment.objects.bulk_create(sentiment_objects)

    # Return the IDs of the created sentiments
    return json.dumps({'ids': [sentiment.id for sentiment in sentiment_objects]})


@celery.task
def send_webhook(self, url):
    requests.post(url, json=self)
