import logging
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate

from agent.classifier import get_default_llm
from agent.models import ExtractionResult
from agent.prompts import EXTRACTION_PROMPT

logger = logging.getLogger(__name__)


def extract_task(
    sender: str,
    subject: str,
    date: str,
    body: str,
    llm: Optional[BaseChatModel] = None,
) -> ExtractionResult:
    """Extract structured task details from an actionable email.

    Args:
        sender: Email sender address or name.
        subject: Email subject line.
        date: Date and time the email was received or sent.
        body: Plain text content of the email body.
        llm: Optional LangChain chat model instance. If not provided, defaults to ChatGroq.

    Returns:
        ExtractionResult: Validated Pydantic model containing task_title, deadline, priority, and sender_context.

    Raises:
        RuntimeError: If the LLM invocation or structured validation fails.
    """
    try:
        model = llm or get_default_llm()
        prompt = PromptTemplate.from_template(EXTRACTION_PROMPT)
        structured_llm = model.with_structured_output(ExtractionResult)
        chain = prompt | structured_llm

        result = chain.invoke(
            {
                "sender": sender,
                "subject": subject,
                "date": date,
                "body": body,
            }
        )

        if not isinstance(result, ExtractionResult):
            result = ExtractionResult.model_validate(result)

        return result
    except Exception as e:
        logger.error("Failed to extract task from email: %s", e, exc_info=True)
        raise RuntimeError(f"Task extraction failed: {e}") from e
