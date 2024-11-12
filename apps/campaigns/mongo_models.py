from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class BaseCampaignHistory:
    campaign_id: int
    user_id: int
    client_ip: str
    created_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class CampaignViewHistory(BaseCampaignHistory):
    is_true_view: bool | None = None


@dataclass
class CampaignClickHistory(BaseCampaignHistory):
    pass
