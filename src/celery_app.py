from celery import Celery
import requests
import csv
import os

from src.ml.ml_service import predictor

celery_app = Celery(
    "worker",
    broker="redis://redis:6379/0",
    backend="redis://redis:6379/0"
)


@celery_app.task
def fetch_and_save_users():
    url = "https://jsonplaceholder.typicode.com/users"
    response = requests.get(url)
    users = response.json()

    file_path = "/data/users.csv"
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["id", "name", "email"])
        writer.writeheader()
        for user in users:
            writer.writerow({
                "id": user["id"],
                "name": user["name"],
                "email": user["email"]
            })

    return f"Saved {len(users)} users to {file_path}"

@celery_app.task
def train_ml_model():
    try:
        success = predictor.train_model()
        if success:
            return {"status": "success", "message": "Model trained successfully"}
        else:
            return {"status": "error", "message": "Model training failed"}
    except Exception as e:
        return {"status": "error", "message": f"Training error: {str(e)}"}