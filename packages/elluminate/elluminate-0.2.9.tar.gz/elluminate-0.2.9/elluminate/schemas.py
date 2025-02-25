from __future__ import annotations

import re
from datetime import datetime
from enum import Enum
from typing import Any, ClassVar

from pydantic import BaseModel, model_validator
from typing_extensions import Self


class TemplateString(BaseModel):
    """Convenience class for rendering a string with template variables."""

    template_str: str
    _PLACEHOLDER_PATTERN: ClassVar[re.Pattern] = re.compile(r"{{\s*(\w+)\s*}}")

    @property
    def is_template(self) -> bool:
        """Return True if the template string contains any placeholders."""
        return bool(self._PLACEHOLDER_PATTERN.search(self.template_str))

    @property
    def placeholders(self) -> set[str]:
        """Return a set of all the placeholders in the template string."""
        return set(self._PLACEHOLDER_PATTERN.findall(self.template_str))

    def render(self, **kwargs: str) -> str:
        """Render the template string with the given variables. Raises ValueError if any placeholders are missing."""
        if not set(self.placeholders).issubset(set(kwargs.keys())):
            missing = set(self.placeholders) - set(kwargs.keys())
            raise ValueError(f"Missing template variables: {str(missing)}")

        def replacer(regex_match: re.Match[str]) -> str:
            var_name = regex_match.group(1)
            return str(kwargs[var_name])

        return self._PLACEHOLDER_PATTERN.sub(replacer, self.template_str)

    def __str__(self) -> str:
        return self.template_str

    def __eq__(self, other: object) -> bool:
        """Compare TemplateString with another object.

        If other is a string, compare with template_str.
        If other is a TemplateString, compare template_str values.
        """
        if isinstance(other, str):
            return self.template_str == other
        if isinstance(other, TemplateString):
            return self.template_str == other.template_str
        return NotImplemented


class User(BaseModel):
    """User model."""

    id: int
    name: str
    email: str


class Project(BaseModel):
    """Project model."""

    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime


class APIKey(BaseModel):
    """API key model."""

    id: int
    name: str
    key_slug: str
    expiration: datetime | None = None
    last_used_at: datetime | None = None
    created_at: datetime


class LLMConfig(BaseModel):
    """Model for an LLM configuration."""

    # These fields will be set properly when `LLMConfig` is used as a response (output) model
    id: int | None = None
    name: str | None = None
    description: str = ""

    # LLM configuration settings
    llm_model_name: str
    llm_base_url: str | None = None
    api_key: str | None = None
    api_version: str | None = None
    max_connections: int = 10

    # Sampling parameters
    max_retries: int | None = None
    timeout: int | None = None
    system_message: str | None = None
    max_tokens: int | None = None
    top_p: float | None = None
    temperature: float | None = None
    best_of: int | None = None
    top_k: int | None = None
    logprobs: bool | None = None
    top_logprobs: int | None = None


class GenerationMetadata(BaseModel):
    """Metadata about an LLM generation."""

    llm_model_config: LLMConfig
    duration_seconds: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None

    def __repr__(self) -> str:
        return f"Generation for {self.llm_model_config!s}"


class TemplateVariablesCollection(BaseModel):
    """Collection of template variables."""

    id: int
    name: str
    description: str
    project: Project
    created_at: datetime
    updated_at: datetime


class TemplateVariables(BaseModel):
    """Template variables model."""

    id: int
    input_values: dict[str, Any]
    collection: TemplateVariablesCollection
    created_at: datetime


class TemplateVariablesCollectionWithEntries(TemplateVariablesCollection):
    """Template variables collection with its entries."""

    variables: list[TemplateVariables]


class PromptTemplate(BaseModel):
    """Prompt template model."""

    id: int
    name: str
    version: int
    user_prompt_template: TemplateString
    default_template_variables_collection: TemplateVariablesCollection | None = None
    parent_prompt_template: "PromptTemplate | None" = None
    created_at: datetime
    updated_at: datetime


class Prompt(BaseModel):
    """New prompt model."""

    id: int
    prompt_template: PromptTemplate
    template_variables: TemplateVariables
    prompt_str: str  # Computed field
    created_at: datetime


class PromptResponse(BaseModel):
    """Prompt response model."""

    id: int
    prompt: Prompt
    response: str
    generation_metadata: GenerationMetadata | None
    ratings: list[Rating] = []
    created_at: datetime


class Criterion(BaseModel):
    """Rating criterion model."""

    id: int
    criterion_str: str
    prompt_template: PromptTemplate | None = None
    template_variables: TemplateVariables | None = None
    created_at: datetime


class Rating(BaseModel):
    """Rating model."""

    id: int
    criterion: Criterion
    rating: bool
    reasoning: str | None = None
    generation_metadata: GenerationMetadata | None = None
    created_at: datetime


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


# Request Models
class CreatePromptTemplateRequest(BaseModel):
    """Request to create a new prompt template."""

    name: str | None = None
    user_prompt_template_str: str
    parent_prompt_template_id: int | None = None
    default_collection_id: int | None = None


class UpdatePromptTemplateRequest(BaseModel):
    """Request to update a prompt template."""

    name: str


class CreateAPIKeyRequest(BaseModel):
    """Request to create a new API key."""

    name: str
    expiration: datetime | None = None


class CreateCollectionRequest(BaseModel):
    """Request to create a new template variables collection."""

    name: str | None = None
    description: str = ""


class CreateTemplateVariablesRequest(BaseModel):
    """Request to create a new template variables entry in a collection.

    This model intentionally supports two mutually exclusive modes of operation:
    1. Manual Entry Mode:
       - Set input_values with your template variable data
       - Leave prompt_template_id as None
       - Used for direct creation of template variables

    2. AI Generation Mode:
       - Set prompt_template_id to reference a prompt template
       - Leave input_values as None
       - Used for AI-powered generation of template variables
    """

    input_values: dict[str, str] | None = None
    prompt_template_id: int | None = None

    @model_validator(mode="after")
    def validate_exactly_one_field(self) -> Self:
        """Validate that at least one of input_values or prompt_template_id is set."""
        if self.input_values is None and self.prompt_template_id is None:
            raise ValueError("Exactly one of input_values or prompt_template_id must be provided")
        return self


class CreatePromptRequest(BaseModel):
    """Request to create a new prompt."""

    prompt_template_id: int
    template_variables_id: int


class CreatePromptResponseRequest(BaseModel):
    """Request to create a new prompt response."""

    prompt_template_id: int
    template_variables_id: int
    llm_config_id: int | None = None
    response: str | None = None
    metadata: GenerationMetadata | None = None


class BatchCreatePromptResponseRequest(BaseModel):
    prompt_response_ins: list[CreatePromptResponseRequest]


class BatchCreatePromptResponseStatus(BaseModel):
    status: str
    result: list[PromptResponse] | None
    percent: int
    progress_msg: str | None = None
    error_msg: str | None = None


class GenerateCriteriaRequest(BaseModel):
    """Request to generate rating criteria."""

    prompt_template_id: int
    criteria: list[str] | None = None
    criterion_set: str | None = None
    delete_existing: bool = False


class RatingMode(str, Enum):
    """Enum for rating mode. In current implementation, only two modes are supported: fast mode is without reasoning and detailed mode is with reasoning."""

    FAST = "fast"
    DETAILED = "detailed"


class CreateRatingRequest(BaseModel):
    prompt_response_id: int
    rating_mode: RatingMode = RatingMode.FAST
    experiment_id: int | None = None


class BatchCreateRatingRequest(BaseModel):
    prompt_response_ids: list[int]
    rating_mode: RatingMode = RatingMode.FAST
    experiment_id: int | None = None


class BatchCreateRatingResponseStatus(BaseModel):
    status: str
    result: list[list[Rating]] | None
    percent: int
    progress_msg: str | None = None
    error_msg: str | None = None


class UpdateRatingRequest(BaseModel):
    """Request to update a rating."""

    rating: bool


class CreateExperimentRequest(BaseModel):
    """Request to create a new experiment."""

    name: str
    description: str
    prompt_template_id: int
    collection_id: int
    llm_config_id: int | None = None
    generate: bool = False
    rating_mode: RatingMode | None = None
