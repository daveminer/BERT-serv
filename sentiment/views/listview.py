from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from ..models import Sentiment


class SentimentList(ListView):
    model = Sentiment

    queryset: QuerySet[Sentiment] = Sentiment.objects.all().order_by('-created_at')[:100]

    template_name: str = '../templates/list.html'

    def get(self, request, *args, **kwargs) -> HttpResponse | JsonResponse:
        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            return JsonResponse(list(
                self.get_queryset().values('created_at', 'label', 'score', 'tags', 'text')
            ), safe=False)

        return super().get(request, *args, **kwargs)
