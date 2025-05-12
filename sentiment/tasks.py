from .celery import Celery, worker_logger
from .models import Sentiment
from transformers import BertTokenizer, BertForSequenceClassification, pipeline
from typing import List, Tuple
import html
import requests
import logging

# Use the worker logger
logger = worker_logger

celery = Celery()

max_text_length = 512

model = 'yiyanghkust/finbert-tone'

finbert = BertForSequenceClassification.from_pretrained(
    model, num_labels=3)

tokenizer = BertTokenizer.from_pretrained(model)

nlp = pipeline("text-classification", model=finbert, tokenizer=tokenizer)

@celery.task
def run_sentiment(content: List[Tuple[int, List[str], str]]):
    logger.info("Starting sentiment analysis", extra={
        "content_items": len(content),
        "task_type": "sentiment_analysis",
        "task_name": "run_sentiment"
    })
    
    try:
        results = nlp([html.unescape(item[2])[:max_text_length] for item in content])
        logger.debug("NLP processing completed", extra={
            "results_count": len(results),
            "task_name": "run_sentiment"
        })

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
            logger.debug("Processed item", extra={
                "item_index": idx,
                "sentiment_label": label,
                "sentiment_score": float(score),  # Convert to float for OpenTelemetry
                "task_name": "run_sentiment"
            })

        results = Sentiment.objects.bulk_create(sentiments)
        logger.info("Successfully saved sentiments", extra={
            "saved_count": len(results),
            "task_name": "run_sentiment"
        })

        return [
            {
                "article_id": content[idx][0],
                "sentiment": {k: v for k, v in sentiment.to_dict().items() if k in ["label", "score", "tags"]}
            }
            for idx, sentiment in enumerate(sentiments)
        ]
    except Exception as e:
        logger.error("Error in sentiment analysis", extra={
            "error_message": str(e),
            "error_type": type(e).__name__,
            "task_name": "run_sentiment"
        }, exc_info=True)
        raise


@celery.task
def send_webhook(sentiments, url):
    logger.info("Sending webhook", extra={
        "webhook_url": url,
        "results_count": len(sentiments),
        "task_name": "send_webhook"
    })
    
    try:
        payload = {
            "results": sentiments
        }
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logger.info("Webhook sent successfully", extra={
            "status_code": response.status_code,
            "task_name": "send_webhook"
        })
    except Exception as e:
        logger.error("Error sending webhook", extra={
            "error_message": str(e),
            "error_type": type(e).__name__,
            "webhook_url": url,
            "task_name": "send_webhook"
        }, exc_info=True)
        raise
