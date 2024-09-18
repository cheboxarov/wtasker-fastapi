from pydantic import BaseModel, Field
from fastapi import FastAPI, HTTPException
from uvicorn import run
from typing import List
from enum import Enum
from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi.exceptions import ResponseValidationError

app = FastAPI()


class TaskStatus(Enum):
    pending = "pending"
    active = "active"
    complited = "complited"

class TaskModel(BaseModel):
    title: str
    views: int = Field(ge=0)
    status: TaskStatus = Field(default=TaskStatus.pending)


fake_tasks = [
    {"title": "покакать1", "views": 1, "status": "pending"},
    {"title": "покакать2", "views": 'sdfsadf', "status": "active"},
]


@app.exception_handler(ResponseValidationError)
async def validation_exception_handler(request: Request, exc: ResponseValidationError) -> JSONResponse:
    return JSONResponse({
        "error": "bad entity",
    }, status_code=422)


@app.get("/tasks", response_model=List[TaskModel])
async def get_task(limit: int = 10, offset: int = 0):
    return fake_tasks[offset:limit]


@app.get("/tasks/{task_id}", response_model=TaskModel)
async def get_task(task_id: int):
    if task_id > len(fake_tasks) - 1 or task_id < 0:
        raise HTTPException(status_code=404)
    return fake_tasks[task_id]


@app.post("/tasks", response_model=TaskModel)
async def create_task(task: TaskModel):
    fake_tasks.append(task.model_dump())
    print(fake_tasks)
    return task.model_dump()


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)