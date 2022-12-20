from django.http import HttpResponse
from django.views.generic import ListView

from .tasks import run_sentiment
from .models import Sentiment


class SentimentList(ListView):
    model = Sentiment

    def index(request):
        last_100 = Sentiment.objects.all().order_by('-created')[:100]

        return HttpResponse(map(SentimentList.__display__, last_100))

    def post(request, *args, **kwargs):
        run_sentiment.delay(["123acs"])
        return HttpResponse(status=201)

    def __display__(record):
        return f'{record.created} : {record.sentiment} : {record.text} '
