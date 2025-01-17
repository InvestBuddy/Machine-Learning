FROM python:3.12-slim

WORKDIR /app

# Install build dependencies (including distutils)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev gcc python3-dev python3-distutils && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY ./requirements.txt /app/requirements.txt

# Install Python dependencies using a build stage
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy application code
COPY . /app/

EXPOSE 8087

# Run the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8087"]
