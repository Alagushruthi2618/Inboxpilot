import logging
from typing import Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field

from agent.classifier import classify_email
from agent.extractor import extract_task
from agent.models import ClassificationResult, ExtractionResult

# Load environment variables
load_dotenv()

# Configure logger
logger = logging.getLogger(__name__)

# Initialize FastAPI application
app = FastAPI(
    title="InboxPilot Agent API",
    description="AI-powered email classification and structured task extraction service.",
    version="1.0.0",
)


class EmailProcessRequest(BaseModel):
    """Incoming request model for processing an email."""

    sender: str = Field(
        ...,
        description="Sender name or email address.",
        examples=["sarah.connor@example.com"],
    )
    subject: str = Field(
        ...,
        description="Email subject line.",
        examples=["Urgent: Review Q3 Security Audit and Sign Off by Friday"],
    )
    date: str = Field(
        ...,
        description="Date and time string when the email was sent or received.",
        examples=["2026-08-22 10:30 AM"],
    )
    body: str = Field(
        ...,
        description="Plain text content of the email body.",
        examples=["Please review the attached report and sign off by Friday 5 PM."],
    )


class EmailProcessResponse(BaseModel):
    """Combined response model containing classification and optional task extraction."""

    classification: ClassificationResult = Field(
        ...,
        description="Email actionability classification decision and confidence.",
    )
    task: Optional[ExtractionResult] = Field(
        default=None,
        description="Extracted task details if email is actionable, otherwise null.",
    )


@app.post(
    "/process-email",
    response_model=EmailProcessResponse,
    status_code=status.HTTP_200_OK,
    summary="Process Email",
    description=(
        "Accepts email metadata and body, classifies actionability, and extracts "
        "structured task details if actionable."
    ),
)
def process_email(payload: EmailProcessRequest) -> EmailProcessResponse:
    """Process an incoming email for classification and structured task extraction.

    Args:
        payload: EmailProcessRequest containing sender, subject, date, and body.

    Returns:
        EmailProcessResponse: Classification result combined with extracted task (if actionable).

    Raises:
        HTTPException: 502 if LLM processing/extraction fails, or 500 for unexpected errors.
    """
    try:
        # Step 1: Classify email actionability
        classification = classify_email(
            sender=payload.sender,
            subject=payload.subject,
            date=payload.date,
            body=payload.body,
        )

        # Step 2: Extract structured task details if email is actionable
        task: Optional[ExtractionResult] = None
        if classification.is_actionable:
            task = extract_task(
                sender=payload.sender,
                subject=payload.subject,
                date=payload.date,
                body=payload.body,
            )

        return EmailProcessResponse(
            classification=classification,
            task=task,
        )

    except RuntimeError as e:
        logger.error("LLM processing failure in /process-email: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Downstream LLM processing failed: {e}",
        )
    except Exception as e:
        logger.error("Unexpected error in /process-email: %s", e, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred while processing email: {e}",
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agent.main:app", host="0.0.0.0", port=8000, reload=True)
