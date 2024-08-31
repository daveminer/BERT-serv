# syntax=docker/dockerfile:1

FROM python:3.10 AS base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/

FROM base AS webapp
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "your_project_name.wsgi:application"]

FROM base AS celery_worker
RUN python3 -c "from transformers import BertTokenizer, BertForSequenceClassification;\
  BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3);"
CMD [ "celery", "-A", "sentiment", "worker", "--pool=solo", "--loglevel=INFO" ]
