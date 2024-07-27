FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install wget -y

COPY . /app
RUN pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir -r requirements.txt

RUN wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1d6mOV97rQWL5h4hIU75_8mmkSyPmlv5N' -O /app/SRGAN_x2.pth
RUN wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=1gm6-k8YdH1Sx8jSofRRDQDSWkzgfW0AS' -O /app/SRGAN_x4.pth
RUN wget --no-check-certificate 'https://drive.google.com/uc?export=download&id=15qWXQsQ0zDj-LNgxDYlpsp2NWcUtrOZQ' -O /app/SRGAN_x8.pth

RUN ["chmod", "+x", "./docker-entrypoint.sh"]

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]
