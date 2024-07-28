from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from ..models import Sentiment


class SentimentList(ListView):
    model = Sentiment
    template_name: str = '../templates/list.html'
    paginate_by: int = 10  # Number of items per page

    def get_queryset(self) -> QuerySet[Sentiment]:
        queryset = Sentiment.objects.all().order_by('-created_at')
        tag = self.request.GET.get('tag')
        if tag:
            queryset = queryset.filter(tags__icontains=tag)
        return queryset

    def get(self, request, *args, **kwargs) -> HttpResponse | JsonResponse:
        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            self.object_list = self.get_queryset()
            context = self.get_context_data()
            return JsonResponse(list(
                context['object_list'].values('created_at', 'label', 'score', 'tags', 'text')
            ), safe=False)

        return super().get(request, *args, **kwargs)