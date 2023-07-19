
FROM python:3.11-slim as uwsgi-builder


RUN pip install --no-cache-dir --upgrade pip==22.3.1

COPY requirements.txt requirements.txt
RUN pip wheel --no-cache-dir --wheel-dir=/root/wheels -r requirements.txt


FROM python:3.11-slim
WORKDIR /opt/app
COPY . .
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt requirements.txt
COPY --from=uwsgi-builder /root/wheels /root/wheels

RUN pip install \
    --no-index \
    --no-cache-dir \
    --find-links=/root/wheels \
    -r requirements.txt

RUN rm -rf /root/wheels
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8002"]
