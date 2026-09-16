FROM python:3.12-slim

# Install system tools, git, and maven for testbed sandboxing
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    maven \
    openjdk-17-jdk-headless \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy dependency specifications
COPY backend/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy source code
COPY backend /app/backend
COPY .env-template /app/.env-template

ENV PYTHONPATH=/app/backend
EXPOSE 8000

CMD ["python", "backend/src/main.py"]
