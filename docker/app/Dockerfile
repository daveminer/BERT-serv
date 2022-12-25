# syntax=docker/dockerfile:1

FROM python:3.10
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code
COPY requirements.txt /code/
RUN pip3 install -r requirements.txt
COPY . /code/

CMD ["python", "/code/manage.py", "runserver", "0.0.0.0:8000"]
