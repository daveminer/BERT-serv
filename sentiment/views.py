from django.http import HttpResponse
from .celery import run_sentiment


def post(request, *args, **kwargs):
    body_unicode = request.body.decode('utf-8')
    print(body_unicode)
    run_sentiment.delay("")
    return HttpResponse(status=201)
