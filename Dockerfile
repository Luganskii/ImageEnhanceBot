FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY . /app
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python3", "main.py"]
