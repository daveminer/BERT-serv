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

        try:
            content = body.get('content', [])
            tags = body.get('tags', [])

            content = [(item['id'], item['text']) for item in content]

            callback_url = request.GET.get('callback_url')
            if callback_url:
                chain(
                    signature("sentiment.tasks.run_sentiment", args=(content,tags,)),
                    signature("sentiment.tasks.send_webhook", args=(callback_url,), retries=3)
                ).delay()
            else:
                signature("sentiment.tasks.run_sentiment", args=(
                    text,tags,)).delay()

            return HttpResponse(status=201)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return HttpResponse(status=500)


def parse_request_body(request):
    try:
        return json.loads(request.body)
    except ValueError:
        raise BadRequest("Could not parse request body as JSON.")
