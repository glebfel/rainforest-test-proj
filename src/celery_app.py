import socket

from celery import Celery

from settings import settings

broker_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_CELERY_DB}"
backend_url = f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_CELERY_DB}"

celery_app = Celery("tasks", broker=broker_url, backend=backend_url)

celery_app.autodiscover_tasks(
    [
        "tasks",
    ],
    force=True,
)

celery_app.conf.redis_socket_timeout = 8
celery_app.conf.redis_socket_connect_timeout = 4
celery_app.conf.redis_retry_on_timeout = True

celery_app.conf.broker_transport_options = {
    "socket_timeout": 8,
    "socket_connect_timeout": 4,
    "socket_keepalive": True,
    "socket_keepalive_options": {
        socket.TCP_KEEPIDLE: 60,
        socket.TCP_KEEPINTVL: 30,
        socket.TCP_KEEPCNT: 10,
    },
}

celery_app.conf.task_publish_retry_policy = {
    "max_retries": None,
    "interval_start": 0,
    "interval_step": 1,
    "interval_max": 5,
}

celery_settings = {
    # broker
    "broker_connection_max_retries": None,
    "broker_connection_retry_on_startup": True,
    # worker
    "worker_cancel_long_running_tasks_on_connection_loss": True,
    "worker_deduplicate_successful_tasks": True,
}

# Apply settings to the Celery instance
celery_app.conf.update(celery_settings)
