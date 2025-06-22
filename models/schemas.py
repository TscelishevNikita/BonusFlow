from pydantic import BaseModel
from datetime import datetime


class BonusRequest(BaseModel):
    transaction_amount: float
    timestamp: datetime
    customer_status: str  # "regular" или "vip"

class BonusRuleApplied(BaseModel):
    rule: str
    bonus: float

class BonusResponse(BaseModel):
    total_bonus: float
    applied_rules: list[BonusRuleApplied]
