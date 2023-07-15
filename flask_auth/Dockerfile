FROM python:3.10.8-slim
RUN apt-get update && apt-get install -y libpq-dev gcc && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/app/src

# RUN useradd -ms /bin/bash app

COPY requirements.txt ./

# scripts py.test and pytest are installed in '/home/app/.local/bin' which is not on PATH.
ENV PATH="${PATH}:/home/app/.local/bin"

# pg_config is in postgresql-devel (libpq-dev in Debian/Ubuntu)
RUN pip install --no-cache-dir --upgrade pip==22.3
RUN pip install --no-cache-dir -r requirements.txt

COPY ./src ./
COPY ./src/entrypoint.sh ./entrypoint.sh
# RUN chown -R app .
# USER app

ENTRYPOINT [ "sh", "./entrypoint.sh" ]