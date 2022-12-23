from django.db import models


class Sentiment(models.Model):
    text = models.TextField(null=False)
    sentiment = models.CharField(max_length=100, null=False)
    created = models.DateTimeField(auto_now=True)
