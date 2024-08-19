import random
from sentiment.models import Sentiment

def create_sentiment(label, text, score=None, tags=None):
    if score is None:
        score = random.uniform(-1.0, 1.0)  # Generate a random score between -1.0 and 1.0
    if tags is None:
        tags = []  # Set tags to an empty list if not provided

    return Sentiment.objects.create(
        label=label,
        score=score,
        tags=tags,
        text=text
    )