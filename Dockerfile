# Use the official Python slim image as a base
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required for PostgreSQL and WebSockets
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up to reduce image size

# Copy dependency file and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the project files
COPY . /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Change permissions to avoid permission issues
RUN chmod +x manage.py

# Expose port 8000 for Django application
EXPOSE 8000

# Default command to run the application with WebSockets support
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "django_test_app.asgi:application"]
