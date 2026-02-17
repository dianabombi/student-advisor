from celery import Celery
import os

# Налаштування Celery
celery_app = Celery(
    'codex',
    broker=os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'),
    backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0')
)

# Конфігурація
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='Europe/Bratislava',
    enable_utc=True,
    
    # Скільки задач може виконувати один worker одночасно
    worker_concurrency=4,
    
    # Автоматично видаляти завершені задачі через 1 годину
    result_expires=3600,
    
    # Beat schedule for periodic tasks
    beat_schedule={
        'daily-price-monitoring': {
            'task': 'tasks.price_monitoring.daily_price_monitoring',
            'schedule': 86400.0,  # Every 24 hours (in seconds)
            # 'schedule': crontab(hour=9, minute=0),  # Alternative: every day at 9 AM
        },
    },
)

# Імпортувати задачі вручну (безпечно для Flower)
try:
    from services.doc_processor import tasks  # noqa
except (ImportError, ModuleNotFoundError):
    pass  # Flower не потребує цих задач

try:
    from tasks import price_monitoring  # noqa
except (ImportError, ModuleNotFoundError):
    pass  # Flower не потребує цих задач

try:
    from tasks import university_scraping  # noqa
except (ImportError, ModuleNotFoundError):
    pass  # Import scraping tasks
