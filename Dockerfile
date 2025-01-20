FROM python:3.11-slim

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virtualenvs.create false && poetry install --no-root

COPY src/src_data_preparation/prepare_data_service.py /app/

EXPOSE 8000

CMD ["uvicorn", "prepare_data_service:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
