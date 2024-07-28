from django.db import models
from django.contrib.postgres.fields import ArrayField

class Sentiment(models.Model):
    label = models.TextField(null=False)
    score = models.FloatField(null=False)
    tags = ArrayField(models.TextField(), null=False)
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now=True)
