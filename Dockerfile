from apache/airflow:2.10.0

ENV DEBIAN_FRONTEND=noninteractive

USER root
# Install needed system packages (for psycopg2, debugging, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    libffi-dev \
    git \
    curl \
    nano \
    && rm -rf /var/lib/apt/lists/*
USER airflow

# Copy and install Python deps (requirements.txt mounted later for dev, but build-time ensures base packages)
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt