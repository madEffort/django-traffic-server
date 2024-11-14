from celery.schedules import crontab
from decouple import config

CELERY_BROKER_URL = f'redis://:{config("REDIS_PASSWORD")}@redis:6379/0'


CELERY_BEAT_SCHEDULE = {
    "aggregate_and_insert_campaigns_stats": {
        "task": "apps.campaigns.tasks.aggregate_and_insert_campaigns_stats",
        "schedule": crontab(
            minute=0, hour=0, day_of_week="*", day_of_month="*", month_of_year="*"
        ),
    },
}
