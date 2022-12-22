from django.http import HttpResponse
from django.views.generic import View

from ..tasks import run_sentiment

import json


class SentimentCreate(View):

    def post(self, request, *args, **kwargs):
        try:
            run_sentiment.delay(json.loads(request.body))
            return HttpResponse(status=201)
        except ValueError:
            return HttpResponse(status=400, content="Could not parse the request body to JSON.")
