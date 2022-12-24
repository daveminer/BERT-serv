from django.views.generic import View


class SentimentCallback(View):
    def post(self, request, *args, **kwargs):
        print(request.body, "CALLBACK RECEIVED")
