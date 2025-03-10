# Stage 1: Install dependencies and build app environment
FROM python:3.11-slim as builder

# Set environment variables (prevent interactive prompts)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies if required (e.g. build-essential)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first (improves build cache)
COPY backend/base/pyproject.toml ./

# Install Poetry and Python dependencies
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root --only main

# Copy entire backend application code into the container
COPY backend .

# Stage 2: Create runtime stage
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Copy installed Python environment from the builder stage
COPY --from=builder /usr/local /usr/local
COPY --from=builder /app /app

# Expose backend port (7860 is Langflow default)
EXPOSE 7860

# Use Gunicorn or Uvicorn depending on Langflow's original setup
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]