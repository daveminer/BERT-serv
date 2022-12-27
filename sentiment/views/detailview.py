from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse
from django.views.generic import DetailView
from ..models import Sentiment

class SentimentDetail(DetailView):
  model = Sentiment

  template_name: str = '../templates/detail.html'

  def get(self, request, *args, **kwargs) -> HttpResponse | JsonResponse:
    if 'application/json' in request.META.get('HTTP_ACCEPT'):
      return JsonResponse(model_to_dict(self.get_object()))

    return super().get(request, *args, **kwargs)
