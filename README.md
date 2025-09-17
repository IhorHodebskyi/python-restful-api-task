
# FastAPI + Celery + Redis


1. Побудувати контейнери:
   ```bash
    docker-compose build
    docker-compose up

    API доступне на:
    http://localhost:8000/docs
   
    Запуск Celery задачі:
    POST http://localhost:8000/api/users/fetch

Запуск тестів:
poetry run pytest -v