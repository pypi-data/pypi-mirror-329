from pydantic import BaseModel


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
