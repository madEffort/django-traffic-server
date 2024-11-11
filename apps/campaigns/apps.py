from django.apps import AppConfig
from config.mongodb.client import initialize_mongo_connection


class CampaignsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.campaigns"

    def ready(self):
        # MongoDB 연결 설정
        initialize_mongo_connection()
