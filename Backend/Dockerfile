# Dockerfile backend

# Start from a base image
FROM python:3.9-slim-buster

# Set working directory in the container
WORKDIR /app

# Copy dependencies file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY ./app /app

# Install required system packages
RUN apt-get update \
    && apt-get -y install netcat \
    && apt-get clean

# command to run on container start
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
