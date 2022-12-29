from django.core.exceptions import BadRequest, ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponse
from django.views.generic import View
from celery import signature
import json


class SentimentCreate(View):

    def post(self, request, *args, **kwargs):
        body = parse_request_body(request)

        try:
            signature("sentiment.tasks.run_sentiment", args=(
                body,), link=callback_task(request)).delay()

            return HttpResponse(status=201)
        except:
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
