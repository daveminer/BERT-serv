# syntax=docker/dockerfile:1

FROM python:3.10 as base
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/

FROM base as webapp
CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]

FROM base as celery_worker
RUN pip3 install torch
RUN python3 -c "from transformers import BertTokenizer, BertForSequenceClassification;\
  BertForSequenceClassification.from_pretrained('yiyanghkust/finbert-tone', num_labels=3);"
CMD [ "celery", "-A", "sentiment", "worker", "--pool=solo", "--loglevel=INFO" ]
