from dataclasses import dataclass, field, asdict
from datetime import datetime


@dataclass
class UserNotificationHistory:
    title: str
    content: str
    user_id: int
    is_read: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def to_dict(self):
        return {k: v for k, v in asdict(self).items() if v is not None}
