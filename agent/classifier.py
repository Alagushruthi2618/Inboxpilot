import logging
import os
from typing import Optional

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from agent.models import ClassificationResult
from agent.prompts import CLASSIFICATION_PROMPT

logger = logging.getLogger(__name__)


def get_default_llm() -> BaseChatModel:
    """Instantiate the default chat model for classification."""
    model_name = os.getenv("GROQ_MODEL", "openai/gpt-oss-120b")
    api_key = os.getenv("GROQ_API_KEY")
    return ChatGroq(model=model_name, api_key=api_key, temperature=0)


def classify_email(
    sender: str,
    subject: str,
    date: str,
    body: str,
    llm: Optional[BaseChatModel] = None,
) -> ClassificationResult:
    """Classify an email to determine if it is actionable and assign a confidence score.

    Args:
        sender: Email sender address or name.
        subject: Email subject line.
        date: Date and time the email was received or sent.
        body: Plain text content of the email body.
        llm: Optional LangChain chat model instance. If not provided, defaults to ChatGroq.

    Returns:
        ClassificationResult: Validated Pydantic model containing is_actionable and confidence.

    Raises:
        RuntimeError: If the LLM invocation or structured validation fails.
    """
    try:
        model = llm or get_default_llm()
        prompt = PromptTemplate.from_template(CLASSIFICATION_PROMPT)
        structured_llm = model.with_structured_output(ClassificationResult)
        chain = prompt | structured_llm

        result = chain.invoke(
            {
                "sender": sender,
                "subject": subject,
                "date": date,
                "body": body,
            }
        )

        if not isinstance(result, ClassificationResult):
            result = ClassificationResult.model_validate(result)

        return result
    except Exception as e:
        logger.error("Failed to classify email: %s", e, exc_info=True)
        raise RuntimeError(f"Email classification failed: {e}") from e
