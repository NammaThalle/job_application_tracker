# Use a Python base image (slim version for smaller size)
FROM python:3.9-slim-buster

# Update apt and install necessary packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --upgrade pip 

# Set the working directory inside the container
WORKDIR /app

# Copy requirements file first to leverage Docker's caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY ./src /app/
COPY .env /app/.env

# Specify the command to run when the container starts
ENTRYPOINT ["python", "app.py"]