import numpy as np
# from django.shortcuts import render
from transformers import BertTokenizer, BertForSequenceClassification

# Create your views here.
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def post(request, *args, **kwargs):
    print("POST")
    # finbert = BertForSequenceClassification.from_pretrained(
    #     'yiyanghkust/finbert-tone', num_labels=3)
    #tokenizer = BertTokenizer.from_pretrained('yiyanghkust/finbert-tone')

    # sentences = ["there is a shortage of capital, and we need extra financing",
    #              "growth is strong and we have plenty of liquidity",
    #              "there are doubts about our finances",
    #              "profits are flat"]

    # inputs = tokenizer(sentences, return_tensors="pt", padding=True)
    # outputs = finbert(**inputs)[0]

    # labels = {0: 'neutral', 1: 'positive', 2: 'negative'}
    # for idx, sent in enumerate(sentences):
    #     print(sent, '----', labels[np.argmax(outputs.detach().numpy()[idx])])

    return HttpResponse(status=201)
    # return HttpResponse("{\"name\": \"test\"}")
