from datetime import datetime

from pydantic import BaseModel

from elluminate.beta.schemas.llm_config import LLMConfig
from elluminate.beta.schemas.prompt_template import PromptTemplate
from elluminate.beta.schemas.rating import RatingMode
from elluminate.beta.schemas.response import PromptResponse
from elluminate.beta.schemas.template_variables_collection import TemplateVariablesCollection


class Experiment(BaseModel):
    """Schema for an experiment."""

    id: int
    name: str
    description: str | None = None
    prompt_template: PromptTemplate
    collection: TemplateVariablesCollection
    llm_config: LLMConfig
    rated_responses: list[PromptResponse] = []
    created_at: datetime
    updated_at: datetime
    generation_task_id: str | None = None


class ExperimentGenerationStatus(BaseModel):
    """Schema for generation status response."""

    status: str
    error_msg: str | None = None
    result: Experiment | None = None


class CreateExperimentRequest(BaseModel):
    """Request to create a new experiment."""

    name: str
    description: str
    prompt_template_id: int
    collection_id: int
    llm_config_id: int | None = None
    generate: bool = False
    rating_mode: RatingMode = RatingMode.DETAILED
