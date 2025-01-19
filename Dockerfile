# Use an official Python image
FROM python:3.11-slim

# Install Poetry
RUN pip install poetry

# Set the working directory
WORKDIR /app

# Copy the project files
COPY pyproject.toml poetry.lock* /app/

# Install dependencies
RUN poetry config virtualenvs.create false && poetry install --no-root

# Copy the application code
COPY service.py /app/

# Expose the port for FastAPI
EXPOSE 8000

# Command to run the FastAPI server
CMD ["uvicorn", "prepare_data_service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
