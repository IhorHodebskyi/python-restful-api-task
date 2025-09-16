from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class TaskShema(BaseModel):
    title: str = Field(min_length=1, max_length=100, description="Title of the task")
    description: str = Field(None, max_length=1000, description="Description of the task")
    is_completed: bool = Field(default=False)

class TaskResponseShema(TaskShema):
    id: int = Field(default=None)
    created_at: datetime = Field(default=datetime.now())
    updated_at: datetime = Field(None)

class TaskCreateShema(TaskShema):
    pass

class TaskUpdateShema(TaskShema):
    id: int = Field(default=None)
    title: str = Field(min_length=1, max_length=100, description="Title of the task")
    description: Optional[str] = Field(None, max_length=1000, description="Description of the task")
    is_completed: Optional[bool] = Field(default=False)
