from enum import Enum
from pydantic import BaseModel, Field


class Intent(str, Enum):
    HOUSEKEEPING = "HOUSEKEEPING"
    MAINTENANCE = "MAINTENANCE"
    FOOD = "FOOD"
    BOOKING = "BOOKING"
    INFORMATION = "INFORMATION"
    COMPLAINT = "COMPLAINT"
    EMERGENCY = "EMERGENCY"
    UNKNOWN = "UNKNOWN"


class IntentResult(BaseModel):
    intent: Intent
    confidence: float = Field(ge=0, le=1)
    needs_clarification: bool
    clarification_question: str | None = None
    multiple_requests_detected: bool = False
    rationale: str = Field(default="No rationale provided.", max_length=200)