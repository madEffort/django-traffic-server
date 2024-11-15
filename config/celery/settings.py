from celery.schedules import crontab
from decouple import config

CELERY_BROKER_URL = f'redis://:{config("REDIS_PASSWORD")}@redis:6379/0'


CELERY_BEAT_SCHEDULE = {
    "aggregate_and_insert_campaigns_clicks": {
        "task": "apps.campaigns.tasks.aggregate_and_insert_campaigns_clicks",
        # 매 분마다 작업
        "schedule": crontab(
            minute="*",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        ),
    },
    "aggregate_and_insert_campaigns_views": {
        "task": "apps.campaigns.tasks.aggregate_and_insert_campaigns_views",
        # 매 분마다 작업
        "schedule": crontab(
            minute="*",
            hour="*",
            day_of_week="*",
            day_of_month="*",
            month_of_year="*",
        ),
    },
}
