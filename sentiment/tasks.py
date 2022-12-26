from .celery import Celery
from .models import Sentiment
from transformers import BertTokenizer, BertForSequenceClassification
import json
import numpy as np
import requests

celery = Celery()

model = 'yiyanghkust/finbert-tone'

finbert = BertForSequenceClassification.from_pretrained(
    model, num_labels=3)

tokenizer = BertTokenizer.from_pretrained(model)

labels = {0: 'neutral', 1: 'positive', 2: 'negative'}


@celery.task
def run_sentiment(sentences):
    inputs = tokenizer(sentences, return_tensors="pt", padding=True)
    outputs = finbert(**inputs)[0]

    sentiments = []

    for idx, sent in enumerate(sentences):
        results = outputs.detach().numpy()
        label = labels[np.argmax(results[idx])]
        sentiment = Sentiment.objects.create(text=sent, sentiment=label)
        sentiments.append(sentiment)

    return json.dumps({'ids': list(map(lambda s: s.id, sentiments))})


@celery.task
def send_webhook(self, url):
    requests.post(url, json=self)
