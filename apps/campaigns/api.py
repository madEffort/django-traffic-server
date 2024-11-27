from django.core.cache import cache
from django.shortcuts import get_object_or_404
from ninja_extra import api_controller, route
from ninja_jwt.authentication import JWTAuth

from apps.common.schemas import Error, Success

from .models import Campaign
from .schemas import CampaignIn, CampaignOut, CampaignStatOut

from .mongo_models import CampaignViewHistory, CampaignClickHistory
from config.mongodb.collections import (
    # campaign_click_collection,
    # campaign_view_collection,
    CampaignClickCollection,
    CampaignViewCollection,
)

from .tasks import (
    aggregate_and_insert_campaigns_clicks,
    aggregate_campaign_clicks,
)


@api_controller("/campaigns", tags=["campaigns"])
class CampaignController:

    def get_campaign_cache_key(self, campaign_id: int) -> str:
        return f"campaign:{campaign_id}"

    @route.get("/history", response={200: list[CampaignStatOut], 404: Error})
    def get_campaigns_history_handler(self):
        """캠페인(광고) 별 집계 + PostgreSQL에 집계된 데이터(클릭 수) 저장"""
        clicks_data: list[CampaignStatOut] = aggregate_campaign_clicks()

        # PostgreSQL에 클릭 집계 저장 - 비동기
        aggregate_and_insert_campaigns_clicks.delay()

        return 200, clicks_data

    @route.post("/{campaign_id}", response={200: Success, 404: Error}, auth=JWTAuth())
    def save_campaign_click_history_handler(self, request, campaign_id: int):
        """캠페인(광고) 클릭 기록 저장 - mongodb에 클릭 기록 저장"""

        client_ip = request.META.get("REMOTE_ADDR")

        CampaignClickCollection().insert_one(
            CampaignClickHistory(
                campaign_id=campaign_id,
                user_id=request.user.id,
                client_ip=client_ip,
            ).to_dict()
        )

        return 200, {"detail": "Clicked"}

    @route.get(
        "/{campaign_id}", response={200: CampaignOut, 404: Error}, auth=JWTAuth()
    )
    def save_campaign_view_history_handler(
        self, request, campaign_id: int, is_true_view: bool | None = None
    ):
        """캠페인(광고) 조회 기록 저장 - mongodb에 조회 기록 저장"""
        client_ip = request.META.get("REMOTE_ADDR")

        CampaignViewCollection().insert_one(
            CampaignViewHistory(
                campaign_id=campaign_id,
                user_id=request.user.id,
                client_ip=client_ip,
                is_true_view=is_true_view,
            ).to_dict()
        )

        cache_key = self.get_campaign_cache_key(campaign_id=campaign_id)

        campaign: Campaign | None = cache.get(cache_key)
        if not campaign:
            campaign = get_object_or_404(Campaign, id=campaign_id)

            cache.set(cache_key, campaign, timeout=300)

        return 200, campaign

    @route.get("", response={200: list[CampaignOut], 404: Error})
    def get_campaigns_handler(self):
        """캠페인(광고) 전체 조회"""

        campaigns: list[Campaign] = Campaign.objects.all()

        return 200, campaigns

    @route.post("", response={201: CampaignOut, 400: Error, 404: Error})
    def create_campaign_handler(self, data: CampaignIn):
        """캠페인(광고) 생성"""

        campaign, created = Campaign.objects.get_or_create(
            title=data.title,
            content=data.content,
            start_date=data.start_date,
            end_date=data.end_date,
        )

        if not created:
            return 400, {"detail": "Bad Request"}

        cache_key = self.get_campaign_cache_key(campaign_id=campaign.id)
        cache.set(cache_key, campaign, timeout=300)

        return 201, campaign
