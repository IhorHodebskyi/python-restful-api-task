FROM python:3.12-slim


WORKDIR /app


RUN pip install --no-cache-dir poetry


COPY pyproject.toml poetry.lock* /app/


RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi


COPY . /app


CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]