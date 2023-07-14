FROM python:3.11-slim

RUN apt-get update
RUN apt-get install nano

RUN pip install --no-cache-dir --upgrade pip==22.3.1

WORKDIR /worker
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt
COPY . .

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

CMD python -m debugpy --listen 0.0.0.0:5678 start.py