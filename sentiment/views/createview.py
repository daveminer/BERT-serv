from django.core.exceptions import BadRequest, ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.views.generic import View
from celery import signature
import json
import logging


class SentimentCreate(View):

    def post(self, request, *args, **kwargs):
        body = parse_request_body(request)

        print(body, "BODY")
        print(request, "REQ")
        try:
            text = body.get('text', [])
            tags = body.get('tags', [])

            print(text, "TEXT")
            signature("sentiment.tasks.run_sentiment", args=(
                text,tags,), link=callback_task(request)).delay()
            print("SENTIMENT TASK")
            return HttpResponse(status=201)
        except Exception as e:
            logging.error(f"Error occurred: {e}")
            return HttpResponse(status=500)


def parse_request_body(request):
    try:
        return json.loads(request.body)
    except ValueError:
        raise BadRequest("Could not parse request body as JSON.")


def callback_task(request):
    url = request.GET.get('callback_url')

    if url:
        return signature("sentiment.tasks.send_webhook", args=(url,), retries=3)

    return None
