from pydantic import BaseModel, Field
from typing import Literal


Category = Literal[
    "delivery",
    "refund",
    "billing",
    "technical",
    "account",
    "fraud_risk",
    "other",
]

Urgency = Literal["low", "medium", "high", "critical"]
Sentiment = Literal["calm", "confused", "frustrated", "angry"]


class TicketAnalysis(BaseModel):
    ticket_id: str
    customer_id: str
    category: Category
    urgency: Urgency
    sentiment: Sentiment
    order_id: str | None = Field(default=None)
    requested_action: str
    confidence: float = Field(ge=0, le=1)
    rationale: str