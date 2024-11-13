from datetime import datetime, timedelta

from config.mongodb.collections import (
    campaign_click_collection,
    campaign_view_collection,
)

from .models import CampaignStat


def get_aggregate_campaigns_data() -> list[dict]:
    """캠페인(광고) 별 조회수, 클릭 수 집계"""
    # view 집계
    view_group = campaign_view_collection.aggregate(
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
        ],
        session=None,
    )

    # click 집계
    click_group = campaign_click_collection.aggregate(
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
        ],
        session=None,
    )

    # view_group과 click_group 결과를 딕셔너리로 변환
    view_counts = {item["_id"]: item["count"] for item in view_group}
    click_counts = {item["_id"]: item["count"] for item in click_group}

    # 두 딕셔너리를 합산하여 병합
    total_counts = view_counts.copy()
    for campaign_id, count in click_counts.items():
        total_counts[campaign_id] = total_counts.get(campaign_id, 0) + count

    # 최종 결과 형식으로 변환
    result_list = [
        {"campaign_id": campaign_id, "count": count}
        for campaign_id, count in total_counts.items()
    ]

    return result_list


def insert_campaign_stats(result_list) -> None:
    """집계된 데이터를 PostgreSQL에 저장"""
    campaign_stats = [
        CampaignStat(
            campaign_id=int(item["campaign_id"]),
            count=int(item["count"]),
        )
        for item in result_list
    ]
    CampaignStat.objects.bulk_create(campaign_stats)