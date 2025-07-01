"""
Celery configuration for background task processing
"""

from celery import Celery
from celery.schedules import crontab

from app.core.config import settings

# Create Celery app
celery_app = Celery(
    "ainovelforge",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
    include=[
        "app.tasks.agent_tasks",
        "app.tasks.export_tasks",
        "app.tasks.notification_tasks",
    ]
)

# Celery configuration
celery_app.conf.update(
    # Task routing
    task_routes={
        "app.tasks.agent_tasks.*": {"queue": "agents"},
        "app.tasks.export_tasks.*": {"queue": "exports"},
        "app.tasks.notification_tasks.*": {"queue": "notifications"},
    },
    
    # Task serialization
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    
    # Task execution
    task_soft_time_limit=settings.CELERY_TASK_SOFT_TIME_LIMIT,
    task_time_limit=settings.CELERY_TASK_TIME_LIMIT,
    worker_prefetch_multiplier=1,
    task_acks_late=True,
    worker_disable_rate_limits=False,
    
    # Result backend
    result_expires=3600,  # 1 hour
    result_persistent=True,
    
    # Beat schedule (for periodic tasks)
    beat_schedule={
        "cleanup-expired-sessions": {
            "task": "app.tasks.maintenance_tasks.cleanup_expired_sessions",
            "schedule": crontab(hour=2, minute=0),  # Daily at 2 AM
        },
        "backup-database": {
            "task": "app.tasks.maintenance_tasks.backup_database",
            "schedule": crontab(hour=3, minute=0),  # Daily at 3 AM
        },
        "update-vector-index": {
            "task": "app.tasks.maintenance_tasks.update_vector_index",
            "schedule": crontab(minute="*/30"),  # Every 30 minutes
        },
    },
    
    # Worker configuration
    worker_max_tasks_per_child=1000,
    worker_max_memory_per_child=200000,  # 200MB
    
    # Monitoring
    worker_send_task_events=True,
    task_send_sent_event=True,
    
    # Error handling
    task_reject_on_worker_lost=True,
    task_remote_tracebacks=True,
)

# Task result configuration
celery_app.conf.result_backend_transport_options = {
    "retry_policy": {
        "timeout": 5.0
    }
}

# Redis broker configuration
celery_app.conf.broker_transport_options = {
    "retry_on_timeout": True,
    "socket_connect_timeout": 30,
    "socket_timeout": 30,
}

# Import tasks to ensure they're registered
celery_app.autodiscover_tasks([
    "app.tasks.agent_tasks",
    "app.tasks.export_tasks", 
    "app.tasks.notification_tasks",
    "app.tasks.maintenance_tasks",
]) 