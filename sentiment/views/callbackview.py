from django.http import HttpResponse
from django.views.generic import View


class SentimentCallback(View):
    def post(_self, request, *args, **kwargs):
        return HttpResponse(status=200)
