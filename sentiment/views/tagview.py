from django.core.exceptions import BadRequest
from django.db.models import Avg
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse
from django.views.generic import ListView
from ..models import Sentiment

class SentimentTagList(ListView):
    model = Sentiment
    template_name: str = '../templates/taglist.html'
    paginate_by: int = 10  # Number of items per page

    def get_queryset(self, period: int, tags: str) -> QuerySet[Sentiment]:
        #queryset = Sentiment.objects.filter(tags__in=tag_list).order_by('-created_at')
        print(tags, "TAGS")
        tag_list = [tag.strip() for tag in tags.split(',')]
        print(tag_list, "TAG LIST")
        queryset = Sentiment.objects.filter(tags__contains=tag_list).values('tags').annotate(mean_score=Avg('score')).order_by('-mean_score')
        #queryset = Sentiment.objects.filter(tags__contains=tag_list).order_by('-created_at')
        print(queryset, "QUERSET")
        return queryset

    def get(self, request, *args, **kwargs) -> HttpResponse | JsonResponse:
        tags = self.request.GET.get('tags')
        if not tags:
            raise BadRequest("The 'tags' query parameter is required as a comma-separated list.")
        #if 'application/json' in request.META.get('HTTP_ACCEPT'):

        period = self.request.GET.get('period')
        if period:
            try:
                period = int(period)
            except ValueError:
                raise BadRequest("The 'period' query parameter must be an integer.")
        else:
            period = 30  # Default period value if not provided

        self.object_list = self.get_queryset(period, tags)
        context = self.get_context_data()
        return JsonResponse(list(
            context['object_list'].values('created_at', 'label', 'score', 'tags', 'text')
        ), safe=False)

        #return super().get(request, *args, **kwargs)