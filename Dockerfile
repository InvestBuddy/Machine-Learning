FROM python:3.12-slim

WORKDIR /app

# Install build dependencies including libpq-dev and gcc (distutils, setuptools and pip are already included in the base image)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc python3-dev && \
    rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements file
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies using the upgraded pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app/

EXPOSE 8087

# Run the application
CMD ["uvicorn", "app.Micro.py:app", "--host", "0.0.0.0", "--port", "8087"]
