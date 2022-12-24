from .celery import app
from .models import Sentiment
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np
import requests

model = 'yiyanghkust/finbert-tone'

finbert = BertForSequenceClassification.from_pretrained(
    model, num_labels=3)

tokenizer = BertTokenizer.from_pretrained(model)

labels = {0: 'neutral', 1: 'positive', 2: 'negative'}


@app.task
def run_sentiment(sentences):
    inputs = tokenizer(sentences, return_tensors="pt", padding=True)

    outputs = finbert(**inputs)[0]

    for idx, sent in enumerate(sentences):
        label = labels[np.argmax(outputs.detach().numpy()[idx])]
        Sentiment.objects.create(text=sent, sentiment=label)


def send_webhook(url, data):
    requests.post(url, data)
