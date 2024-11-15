# Use Python base image
FROM python:3.11-slim

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="metens@pdx.edu"

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set the working dir to our app
WORKDIR /app

# Cache the requirements first
COPY requirements.txt . 

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc libpq-dev && \
    python3 -m venv /env && . /env/bin/activate && \
    pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt && \
    apt-get remove -y gcc libpq-dev && apt-get autoremove -y && rm -rf /var/lib/apt/lists/*

# Add venv to PATH
ENV PATH="/venv/bin:$PATH"

# Copy application files
COPY . .

# Expose Flask app port
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
