# syntax=docker/dockerfile:1

FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

# Cache this early for the worker cache layer and to leave it out of app requirements
RUN pip3 install torch
RUN pip3 install transformers

# Load the pretrained model before the worker starts
RUN python3 -c "from transformers import BertTokenizer, BertForSequenceClassification;\
  BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3);"

COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/

CMD [ "celery", "-A", "sentiment", "worker", "--pool=solo", "--loglevel=INFO" ]
