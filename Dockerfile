FROM python:3.10-slim

WORKDIR /app

COPY . /app/

# System dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        wget \
        ca-certificates \
        fonts-liberation \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Install Chromium + its required system dependencies
RUN python -m playwright install --with-deps chromium

CMD ["bash", "run.sh"]
