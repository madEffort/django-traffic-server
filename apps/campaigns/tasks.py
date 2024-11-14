from datetime import datetime, timedelta

from celery import shared_task

from config.mongodb.collections import (
    campaign_click_collection,
    campaign_view_collection,
)

from .models import CampaignStat
from .schemas import CampaignStatOut


def aggregate_campaigns_views() -> list[CampaignStatOut]:
    """캠페인(광고) 조회 수 집계"""
    data = campaign_view_collection.aggregate(
        [
            {
                "$match": {
                    "user_id": {"$exists": True},
                    "created_at": {
                        "$gte": datetime.now() - timedelta(days=1),
                        "$lt": datetime.now(),
                    },
                }
            },
            {
                "$group": {
                    "_id": {"campaign_id": "$campaign_id", "user_id": "$user_id"},
                }
            },
            {"$group": {"_id": "$_id.campaign_id", "count": {"$sum": 1}}},
            {
                "$project": {  # _id를 campaign_id로 변경
                    "_id": 0,  # _id를 숨김
                    "campaign_id": "$_id",
                    "count": 1,
                }
            },
        ],
        session=None,
    )

    return list(data)


def aggregate_campaigns_clicks() -> list[CampaignStatOut]:
    """캠페인(광고) 클릭 수 집계"""
    data = campaign_click_collection.aggregate(
        [
            {
                "$match": {
                    "user_id": {"$exists": True},
                    "created_at": {
                        "$gte": datetime.now() - timedelta(days=1),
                        "$lt": datetime.now(),
                    },
                }
            },
            {
                "$group": {
                    "_id": {"campaign_id": "$campaign_id", "user_id": "$user_id"},
                }
            },
            {"$group": {"_id": "$_id.campaign_id", "count": {"$sum": 1}}},
            {
                "$project": {  # _id를 campaign_id로 변경
                    "_id": 0,  # _id를 숨김
                    "campaign_id": "$_id",
                    "count": 1,
                }
            },
        ],
        session=None,
    )

    return list(data)


def insert_campaigns_stats(data: list[CampaignStat]):
    """집계된 데이터를 PostgreSQL에 저장"""
    campaign_stats = [
        CampaignStat(
            campaign_id=int(item["campaign_id"]),
            count=int(item["count"]),
        )
        for item in data
    ]
    CampaignStat.objects.bulk_create(campaign_stats)


@shared_task
def aggregate_and_insert_campaigns_stats():
    """캠페인(광고) 클릭 데이터 집계 및 저장 작업"""
    data: list[CampaignStat] = aggregate_campaigns_clicks()
    insert_campaigns_stats(data)
