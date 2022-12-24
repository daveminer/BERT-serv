from django.http import HttpResponse
from django.views.generic import View
import celery
import json


class SentimentCreate(View):

    def post(self, request, *args, **kwargs):
        try:
            body = json.loads(request.body)
            celery.signature("sentiment.tasks.run_sentiment", args=(
                body,)).delay()

            return HttpResponse(status=201)
        except ValueError:
            return HttpResponse(status=400, content="Could not parse the request body to JSON.")
