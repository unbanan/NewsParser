FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        make \
        gcc \
        g++ \
        postgresql \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY .pgpass /root/.pgpass
RUN chmod 600 /root/.pgpass
COPY . .

RUN pip install --no-cache-dir -r ./requirements.txt
ENV AIRFLOW_HOME=/app/airflow
CMD ["make"]