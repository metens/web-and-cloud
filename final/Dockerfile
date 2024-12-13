# Use Python 3.11 Alpine image (minimal image size):
FROM python:3.11-alpine

# Specify e-mail address as the maintainer of the container image:
LABEL maintainer="metens@pdx.edu"

# Set env variables for API keys and session secrets:
ENV YELP_API_KEY=${YELP_API_KEY}
ENV GOOGLE_API_KEY=${GOOGLE_API_KEY}
ENV SECRET=${SECRET}

# Set the working directory inside the container:
WORKDIR /app

# Copy only the requirements file and install only the necessary Python packages:
COPY requirements.txt .

# Install requirements:
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code:
COPY . /app

# Expose Flask app port:
EXPOSE 8080

# Set the command to run the Flask application:
CMD ["python3", "app.py"]
