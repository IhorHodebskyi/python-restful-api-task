
# FastAPI + Celery + Redis


1. Побудувати контейнери:
   ```bash
    docker-compose build
    docker-compose up

    API доступне на:
    http://localhost:8000/docs


Запуск тестів:
poetry run pytest -v


📋 API Ендпоінти
Завдання (Tasks)
GET /api/tasks - отримати всі задачі

POST /api/tasks - створити нову задачу

GET /api/tasks/{id} - отримати задачу по ID

PUT /api/tasks/{id} - оновити задачу

DELETE /api/tasks/{id} - видалити задачу

Користувачі (Users)
GET /api/users - отримати всіх користувачів

POST /api/users/fetch - запустити фонове завантаження користувачів

ML Прогнозування (Predict)
POST /api/predict/ - прогнозувати пріоритет задачі

POST /api/predict/train - запустити навчання моделі

GET /api/predict/task-status/{task_id} - перевірити статус задачі

GET /api/predict/healthchecker - перевірити статус ML моделі

Системні
GET /api/healthchecker - перевірити статус сервісу