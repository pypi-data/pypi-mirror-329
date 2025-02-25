from datetime import datetime

from pydantic import BaseModel

from elluminate.beta.schemas.prompt_template import PromptTemplate
from elluminate.beta.schemas.template_variables import TemplateVariables


class Criterion(BaseModel):
    """Rating criterion model."""

    id: int
    criterion_str: str
    prompt_template: PromptTemplate | None = None
    template_variables: TemplateVariables | None = None
    created_at: datetime


class CreateCriteriaRequest(BaseModel):
    """Request to create a new rating criteria.

    This model intentionally supports two mutually exclusive modes of operation:
    1. Manual Entry Mode:
       - Set criteria with your criteria
       - Used for direct creation of criteria

    2. AI Generation Mode:
       - Leave criteria as None
       - Used for AI-powered generation of criteria
    """

    prompt_template_id: int
    template_variables_id: int | None = None
    criteria: list[str] | None = None
    criterion_set: str | None = None
    delete_existing: bool = False
