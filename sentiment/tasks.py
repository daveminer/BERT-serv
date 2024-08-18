from .celery import Celery
from .models import Sentiment
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from typing import List, Tuple
import html
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
def run_sentiment(content: List[Tuple[int, List[str], str]]):
    results = nlp([html.unescape(item[2]) for item in content])

    sentiments = []

    for idx, result in enumerate(results):
        label = result['label']
        score = result['score']
        sentiment = Sentiment(
            label=label,
            text=content[idx][2],
            score=score,
            tags=content[idx][1]
        )
        sentiments.append(sentiment)

    Sentiment.objects.bulk_create(sentiments)

    return [
        {
            "article_id": content[idx][0],
            "sentiment": {k: v for k, v in sentiment.to_dict().items() if k in ["label", "score", "tags"]}
        }
        for idx, sentiment in enumerate(sentiments)
    ]


@celery.task
def send_webhook(sentiments, url):
    payload = {
        "results": sentiments
    }
    requests.post(url, json=payload)
