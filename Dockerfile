# Dockerfile
FROM python:3.9

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Create app directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/
