from datetime import datetime, timedelta
from django.core.exceptions import BadRequest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from django.db.models.query import QuerySet
from django.http import HttpResponse, JsonResponse, QueryDict
from django.views.generic import ListView
from ..models import Sentiment


class SentimentList(ListView):
    model = Sentiment
    template_name: str = '../templates/list.html'
    default_page_size: int = 100

    def get_queryset(self, params: QueryDict) -> QuerySet[Sentiment]:
        queryset = Sentiment.objects.all().order_by('-created_at')
        tags = params.getlist('tags')
        if tags:
            query = Q()
            for tag in tags:
                query |= Q(tags__icontains=tag)
            queryset = queryset.filter(query)
        period = params.get('period')
        if period:
            try:
                period = int(period)
            except ValueError:
                raise BadRequest("The 'period' query parameter must be an integer.")
        else:
            period = 30  # Default period value if not provided

        timestamp = datetime.now() - timedelta(days=period)
        queryset = queryset.filter(created_at__gte=timestamp)
        return queryset

    def get(self, request, *args, **kwargs) -> HttpResponse | JsonResponse:
        self.object_list = self.get_queryset(self.request.GET)

        # Pagination
        page_size = request.GET.get('page_size', self.default_page_size)
        try:
            page_size = int(page_size)
        except ValueError:
            page_size = self.default_page_size

        page = request.GET.get('page')
        try:
            page = int(page)
        except (TypeError, ValueError):
            page = 1

        paginator = Paginator(self.object_list, page_size)
        paginated_queryset = paginator.page(page)

        if 'application/json' in request.META.get('HTTP_ACCEPT'):
            object_list = [
                {
                    'created_at': obj.created_at,
                    'label': obj.label,
                    'score': obj.score,
                    'tags': obj.tags,
                    'text': obj.text
                }
                for obj in paginated_queryset.object_list
            ]

            return JsonResponse(object_list, safe=False)

        context = self.get_context_data(object_list=paginated_queryset.object_list)
        return self.render_to_response(context)