from django.http import HttpResponse
from django.views.generic import ListView
from ..models import Sentiment


class SentimentList(ListView):
    model = Sentiment

    def index(request):
        last_100 = Sentiment.objects.all().order_by('-created')[:100]

        return HttpResponse(map(Sentiment.__display__, last_100))

    def __display__(record):
        return f'{record.created} : {record.sentiment} : {record.text}'
