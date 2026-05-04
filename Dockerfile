#FROM python:3.10.6

# Set the working directory in the container
#WORKDIR /app

# Copy the current directory contents into the container at /app
#COPY . /app/

# Update package lists and upgrade existing packages
#RUN apt-get update && \
  #  apt-get upgrade -y && \
  #  apt-get install -y ffmpeg && \
 #   pip install --upgrade pip && \
   # pip install -r requirements.txt

# Command to run when the container starts
#CMD ["bash", "run.sh"]


FROM python:3.10.6

WORKDIR /app
COPY . /app/

# Install system dependencies required by Playwright
RUN apt-get update && apt-get install -y \
    ffmpeg \
    wget \
    gnupg \
    ca-certificates \
    fonts-liberation \
    libnss3 \
    libatk-bridge2.0-0 \
    libatk1.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libcairo2 \
    libatspi2.0-0 \
    libxdamage1 \
    libxfixes3 \
    libxext6 \
    libx11-6 \
    libxcb1 \
    libx11-xcb1 \
    libxrender1 \
    libxi6 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright browsers
RUN python -m playwright install chromium

CMD ["bash", "run.sh"]
