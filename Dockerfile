FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update

COPY . /app
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1n7Gb5-aPsK7A3icV5Zj3wqHu38AZtuNW' -O /app/srresnet_mini_x2.pth
RUN ["chmod", "+x", "./docker-entrypoint.sh"]

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
