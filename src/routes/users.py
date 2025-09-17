from fastapi import APIRouter
from src.celery_app import fetch_and_save_users
from fastapi.exceptions import HTTPException
import os
import csv

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/fetch")
def fetch_users():
    task = fetch_and_save_users.delay()
    return {"task_id": task.id, "status": "Processing..."}


@router.get("/")
def get_all_users():
    file_path = "/data/users.csv"

    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Users data not found. Please run /fetch first."
        )

    users = []
    try:
        with open(file_path, "r", encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users.append({
                    "id": int(row["id"]),
                    "name": row["name"],
                    "email": row["email"]
                })
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error reading users data: {str(e)}"
        )

    return {"users": users, "count": len(users)}