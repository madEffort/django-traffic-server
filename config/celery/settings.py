from celery.schedules import crontab
from decouple import config

# CELERY_BROKER_URL = f'redis://:{config("REDIS_PASSWORD")}@redis:6379/0'
CELERY_BROKER_URL = (
    f'amqp://{config("RABBITMQ_USER")}:{config("RABBITMQ_PASSWORD")}@rabbitmq:5672/'
)

CELERY_RESULT_BACKEND = f'redis://:{config("REDIS_PASSWORD")}@redis:6379/0'
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_EXPIRES = 3600  # 결과 데이터 유효 기간 (1시간)

# beat
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
