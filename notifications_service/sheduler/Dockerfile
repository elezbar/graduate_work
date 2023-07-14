FROM python:3.11-slim

RUN apt-get update
RUN apt-get install nano

RUN pip install --no-cache-dir --upgrade pip==22.3.1

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./requirements.txt
COPY ./sheduler ./sheduler

RUN pip install \
    --no-cache-dir \
    -r requirements.txt

# CMD ["celery", "-A", "sheduler", "beat", "--loglevel=INFO"]
CMD celery -A sheduler beat --loglevel=INFO ; celery -A sheduler worker --loglevel=INFO