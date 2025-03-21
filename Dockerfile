# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    POETRY_VERSION=1.7.1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/venv"

# Add Poetry to PATH
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        build-essential \
        curl \
        git \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set working directory
WORKDIR $PYSETUP_PATH

# Copy project files
COPY ./pyproject.toml ./poetry.lock* ./

# Install dependencies
RUN poetry install --no-dev --no-root

# Copy application code
COPY ./telecomdb1 ./telecomdb1

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser $PYSETUP_PATH

# Switch to non-root user
USER appuser

# Set environment variables for the application
ENV FLASK_APP=telecomdb1.api.app \
    FLASK_ENV=production \
    PYTHONPATH=$PYSETUP_PATH

# Expose port
EXPOSE 5000

# Run the application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "telecomdb1.api.app:app"] 