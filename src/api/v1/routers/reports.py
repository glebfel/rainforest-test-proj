from datetime import datetime

from fastapi import APIRouter

from celery_app import celery_app
from src.tasks import generate_report_task

reports_router = APIRouter()


@reports_router.get("/")
def generate_report_background(start_date: datetime, end_date: datetime) -> dict:
    task = generate_report_task.delay(start_date, end_date)
    return {"task_id": task.id}


@reports_router.get("/{task_id}")
def get_report_status(task_id: str) -> dict:
    task = celery_app.AsyncResult(task_id)

    if task.state == "PENDING":
        return {"task_id": task_id, "status": task.state}
    elif task.state == "STARTED":
        return {"task_id": task_id, "status": task.state}
    elif task.state == "SUCCESS":
        return {
            "task_id": task_id,
            "status": task.state,
            "result": task.result,
        }
    elif task.state == "FAILURE":
        return {
            "task_id": task_id,
            "status": task.state,
            "error": str(task.result),
        }
    else:
        return {"task_id": task_id, "status": task.state}

