from fastapi import APIRouter, Body
from fastapi.exceptions import HTTPException
from typing import List, Dict

from src.entity.models import TaskResponseShema, TaskCreateShema, TaskUpdateShema
from src.conf.messages import (task_not_found, task_deleted)
from src.database.storage import storage

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("/", response_model=List[TaskResponseShema])
def get_tasks():
    result = storage.get_tasks()
    if result is None:
        raise HTTPException(status_code=404, detail=task_not_found)
    return result


@router.post("/", response_model=TaskResponseShema)
def create_task(body: TaskCreateShema, ):
    result = storage.create_task(body)
    if result is None:
        raise HTTPException(status_code=404, detail=task_not_found)
    return result


@router.get("/{task_id}", response_model=TaskResponseShema)
def get_task_by_id(task_id: int):
    result = storage.get_task_by_id(task_id)
    if result is None:
        raise HTTPException(status_code=404, detail=task_not_found)
    return result


@router.put("/{task_id}", response_model=TaskResponseShema)
def update_task(task_id: int, task_data: TaskUpdateShema = Body(...)):
    result = storage.update_task(task_id, task_data)
    if result is None:
        raise HTTPException(status_code=404, detail=task_not_found)
    return result


@router.delete("/{task_id}", response_model=Dict[str, str])
def delete_task(task_id: int):
    result = storage.delete_task(task_id)
    if not result:
        raise HTTPException(status_code=404, detail=task_not_found)
    return {"message": task_deleted}
