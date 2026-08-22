from typing import Literal, Optional
from pydantic import BaseModel, Field


class ClassificationResult(BaseModel):
    """Result schema for email actionability classification."""

    is_actionable: bool = Field(
        ...,
        description="Indicates whether the email contains an actionable task requiring follow-up.",
    )
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the classification decision, bounded between 0.0 and 1.0.",
    )


class ExtractionResult(BaseModel):
    """Structured extraction schema for actionable email tasks."""

    task_title: str = Field(
        ...,
        description="A concise and actionable title summarizing the task to be completed.",
    )
    deadline: Optional[str] = Field(
        default=None,
        description="Explicit or inferred deadline/due date mentioned in the email, or None if unspecified.",
    )
    priority: Literal["low", "medium", "high"] = Field(
        ...,
        description="Assessed priority level ('low', 'medium', 'high') based on urgency and context.",
    )
    sender_context: str = Field(
        ...,
        description="Brief background or context about the sender and request (e.g., sender role, organization, key project references).",
    )
