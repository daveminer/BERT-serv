from django.core.exceptions import BadRequest, ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.views.generic import View
from celery import chain, signature
from sentiment.tasks import run_sentiment, send_webhook
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
                    run_sentiment.s(content).set(retries=3),
                    send_webhook.s(callback_url).set(retries=3),
                ).delay()
            else:
                run_sentiment.s(content).set(retries=3).delay()

            return HttpResponse(status=201)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return HttpResponse(status=500)


def parse_request_body(request):
    try:
        return json.loads(request.body)
    except ValueError:
        raise BadRequest("Could not parse request body as JSON.")
