from django.db import models
from transformers import BertTokenizer, BertForSequenceClassification
import numpy as np


class Sentiment(models.Model):
    text = models.TextField(null=False)
    sentiment = models.CharField(max_length=100, null=False)
    created = models.DateTimeField(auto_now=True)

    model = 'yiyanghkust/finbert-tone'

    finbert = BertForSequenceClassification.from_pretrained(
        model, num_labels=3)

    tokenizer = BertTokenizer.from_pretrained(model)

    labels = {0: 'neutral', 1: 'positive', 2: 'negative'}

    def run(sentences):
        inputs = Sentiment.tokenizer(
            sentences, return_tensors="pt", padding=True)
        outputs = Sentiment.finbert(**inputs)[0]

        for idx, sent in enumerate(sentences):
            label = Sentiment.labels[np.argmax(outputs.detach().numpy()[idx])]
            Sentiment.objects.create(text=sent, sentiment=label)
