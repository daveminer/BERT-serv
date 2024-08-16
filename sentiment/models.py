from django.db import models
from django.contrib.postgres.fields import ArrayField

class Sentiment(models.Model):
    id = models.AutoField(primary_key=True)
    label = models.TextField(null=False)
    score = models.FloatField(null=False)
    tags = ArrayField(models.TextField(), null=False)
    text = models.TextField(null=False)
    created_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'score': self.score,
            'tags': self.tags,
            'text': self.text,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }