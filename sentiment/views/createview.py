from django.core.exceptions import BadRequest, ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.views.generic import View
from celery import chain, signature
import json
import logging


class SentimentCreate(View):

    def post(self, request, *args, **kwargs):
        body = parse_request_body(request)
        callback_url = request.GET.get('callback_url')

        try:
            content = list(map(lambda item: (item['article_id'], item['tags'], item['text']), body))

            if callback_url:
                chain(
                    signature("sentiment.tasks.run_sentiment", args=(content,), retries=3),
                    signature("sentiment.tasks.send_webhook", args=(callback_url,), retries=3)
                ).delay()
            else:
                signature("sentiment.tasks.run_sentiment", args=(content,)).delay()

            return HttpResponse(status=201)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return HttpResponse(status=500)


def parse_request_body(request):
    try:
        return json.loads(request.body)
    except ValueError:
        raise BadRequest("Could not parse request body as JSON.")


def process_item(item, callback_url):
    content = [(item['article_id'], item['text'])]

    if callback_url:
        chain(
            signature("sentiment.tasks.run_sentiment", args=(content, tags,)),
            signature("sentiment.tasks.send_webhook", args=(callback_url,), retries=3)
        ).delay()
    else:
        signature("sentiment.tasks.run_sentiment", args=(content, tags,)).delay()