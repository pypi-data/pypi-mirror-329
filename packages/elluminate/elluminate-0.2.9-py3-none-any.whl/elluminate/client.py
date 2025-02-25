import asyncio
import atexit
import math
import os
import time
import warnings
from typing import Any, Awaitable, Callable, ClassVar, Literal

import httpx
from loguru import logger
from tqdm import tqdm

from elluminate.schemas import (
    BatchCreatePromptResponseRequest,
    BatchCreatePromptResponseStatus,
    BatchCreateRatingRequest,
    BatchCreateRatingResponseStatus,
    CreateCollectionRequest,
    CreatePromptResponseRequest,
    CreatePromptTemplateRequest,
    CreateRatingRequest,
    CreateTemplateVariablesRequest,
    Criterion,
    Experiment,
    ExperimentGenerationStatus,
    GenerateCriteriaRequest,
    GenerationMetadata,
    LLMConfig,
    Project,
    PromptResponse,
    PromptTemplate,
    Rating,
    RatingMode,
    TemplateVariables,
    TemplateVariablesCollection,
)
from elluminate.utils import deprecated, raise_for_status_with_detail, retry_request, run_async


class Client:
    _semaphore: ClassVar[asyncio.Semaphore] = asyncio.Semaphore(10)

    def __init__(
        self,
        base_url: str | None = None,
        api_key: str | None = None,
        api_key_env: str = "ELLUMINATE_API_KEY",
        base_url_env: str = "ELLUMINATE_BASE_URL",
        timeout: float = 120.0,
    ) -> None:
        """Initialize the Elluminate SDK client.

        Args:
            base_url (str): Base URL of the Elluminate API. Defaults to "https://elluminate.de".
            api_key (str | None): API key for authentication. If not provided, will look for key in environment variable given by `api_key_env`.
            api_key_env (str): Name of environment variable containing API key. Defaults to "ELLUMINATE_API_KEY".
            base_url_env (str): Name of environment variable containing base URL. Defaults to "ELLUMINATE_BASE_URL". If set, overrides base_url.
            timeout (float): Timeout in seconds for API requests. Defaults to 120.0.

        Raises:
            ValueError: If no API key is provided or found in environment.

        """
        warnings.warn(
            "Client is deprecated since version 0.2.9. It will be removed in version 0.3.0. "
            "Migrate to the new Client using `from elluminate.beta import Client`, otherwise your code will break in the next version release. "
            "You can visit our docs for more information: https://docs.elluminate.de/get_started/quick_start/#beta-client",
            category=DeprecationWarning,
            stacklevel=2,
        )
        # Init the API key
        self.api_key = api_key or os.getenv(api_key_env)
        if not self.api_key:
            raise ValueError(f"{api_key_env} not set.")

        # Init the base URL. Use a sane default if no values are provided
        self.base_url = base_url or os.getenv(base_url_env) or "https://elluminate.de"
        self.base_url = self.base_url.strip("/")
        if not base_url and os.getenv(base_url_env):
            logger.debug(f"Using base URL from environment: {self.base_url}")

        # Create async client with the API key header
        headers = {"X-API-Key": self.api_key}
        self.timeout = timeout
        timeout_config = httpx.Timeout(self.timeout)
        self.async_session = httpx.AsyncClient(headers=headers, timeout=timeout_config)
        # This is only needed to get the project synchronously
        self.sync_session = httpx.Client(headers=headers, timeout=timeout_config)

        # Check the SDK version compatibility and print a warning if not compatible
        self.check_version()

        # Load the project and set the route prefix
        self.project = self.load_project()
        self.project_route_prefix = f"{self.base_url}/api/v0/projects/{self.project.id}"

    async def aload_project(self) -> Project:
        """Async version of load_project."""
        response = await self.async_session.get(f"{self.base_url}/api/v0/projects")
        raise_for_status_with_detail(response)
        projects = [Project.model_validate(project) for project in response.json()["items"]]
        if not projects:
            raise RuntimeError("No projects found.")
        return projects[0]

    def load_project(self) -> Project:
        """Loads the project associated with the API key.

        Returns:
            (Project): The project associated with the API key.

        Raises:
            RuntimeError: If no projects are found.

        """
        response = self.sync_session.get(f"{self.base_url}/api/v0/projects")
        if response.status_code == 404:
            raise httpx.HTTPStatusError(
                request=response.request,
                response=response,
                message="No project found (404). Please double check that your base_url and API key are set correctly (also check your environment variables ELLUMINATE_API_KEY and ELLUMINATE_BASE_URL).",
            )
        raise_for_status_with_detail(response)
        projects = [Project.model_validate(project) for project in response.json()["items"]]
        if not projects:
            raise RuntimeError("No projects found.")
        return projects[0]

    def check_version(self) -> None:
        """Check if the SDK version is compatible with the required version."""
        # Import locally to avoid circular imports
        from elluminate import __version__

        response = self.sync_session.post(
            f"{self.base_url}/api/v0/version/compatible",
            json={"current_sdk_version": __version__},
        )
        raise_for_status_with_detail(response)
        compatibility_status = response.json()

        if not compatibility_status["is_compatible"]:
            response = self.sync_session.get("https://pypi.org/pypi/elluminate/json")
            current_pypi_version = response.json()["info"]["version"]
            error_message = (
                f"Current SDK version ({__version__}) is no longer supported. "
                f"The minimum fully supported version is ({compatibility_status['required_sdk_version']}). "
                f"Please upgrade to the latest version ({current_pypi_version}) by running `pip install -U elluminate`."
            )
            logger.error(error_message)
            raise RuntimeError(error_message)

        if compatibility_status["is_deprecated"]:
            response = self.sync_session.get("https://pypi.org/pypi/elluminate/json")
            current_pypi_version = response.json()["info"]["version"]
            logger.warning(
                f"Current SDK version ({__version__}) is deprecated and will be sunset sometime in a future release. "
                f"The minimum fully supported version is ({compatibility_status['required_sdk_version']}). "
                f"Please upgrade to the latest version ({current_pypi_version}) by running `pip install -U elluminate`."
            )

    async def acreate_prompt_template(
        self,
        user_prompt_template: str,
        *,
        name: str | None = None,
        parent_prompt_template_id: int | None = None,
        default_collection_id: int | None = None,
    ) -> PromptTemplate:
        """Async version of create_prompt_template."""
        response = await self.async_session.post(
            f"{self.project_route_prefix}/prompt_templates",
            json=CreatePromptTemplateRequest(
                name=name,
                user_prompt_template_str=user_prompt_template,
                parent_prompt_template_id=parent_prompt_template_id,
                default_collection_id=default_collection_id,
            ).model_dump(),
        )
        raise_for_status_with_detail(response)
        return PromptTemplate.model_validate(response.json())

    def create_prompt_template(
        self,
        user_prompt_template: str,
        *,
        name: str | None = None,
        parent_prompt_template_id: int | None = None,
        default_collection_id: int | None = None,
    ) -> PromptTemplate:
        """Creates a new prompt template.

        Each created prompt template is assigned a default collection. If no `default_collection_id` is provided, a random
        default collection is created.

        Args:
            user_prompt_template (str): The template string containing variables in {{variable_name}} format.
            name (str | None): Optional name for the template. If not provided, a random name will be generated.
            parent_prompt_template_id (int | None): Optional ID of parent template to inherit from.
            default_collection_id (int | None): Optional ID of default template variables collection.

        Returns:
            (PromptTemplate): The created prompt template.

        Raises:
            httpx.HTTPStatusError: If a prompt template with the same name and content already exists or the given parent according to `parent_prompt_template_id` does not exist.

        """
        return run_async(self.acreate_prompt_template)(
            user_prompt_template,
            name=name,
            parent_prompt_template_id=parent_prompt_template_id,
            default_collection_id=default_collection_id,
        )

    async def aget_prompt_template(
        self,
        *,
        name: str,
        version: int | Literal["latest"] = "latest",
    ) -> PromptTemplate:
        """Async version of get_prompt_template."""
        params = {"name": name}
        if version != "latest":
            params["version"] = str(version)

        response = await self.async_session.get(f"{self.project_route_prefix}/prompt_templates", params=params)
        raise_for_status_with_detail(response)
        templates = [PromptTemplate.model_validate(template) for template in response.json().get("items", [])]
        if not templates:
            raise ValueError(f"No prompt template found with name {name} and version {version}")
        return templates[0]

    def get_prompt_template(
        self,
        *,
        name: str,
        version: int | Literal["latest"] = "latest",
    ) -> PromptTemplate:
        """Get a prompt template by name and version.

        Args:
            name (str): Name of the prompt template.
            version (int | Literal["latest"]): Version number or "latest". Defaults to "latest".

        Returns:
            (PromptTemplate): The requested prompt template.

        Raises:
            ValueError: If no template is found with given name and version.

        """
        return run_async(self.aget_prompt_template)(name=name, version=version)

    async def aget_or_create_prompt_template(
        self,
        user_prompt_template: str,
        *,
        name: str,
        parent_prompt_template_id: int | None = None,
        default_collection_id: int | None = None,
    ) -> tuple[PromptTemplate, bool]:
        """Async version of get_or_create_prompt_template."""
        try:
            # Try to create first
            template = await self.acreate_prompt_template(
                user_prompt_template,
                name=name,
                parent_prompt_template_id=parent_prompt_template_id,
                default_collection_id=default_collection_id,
            )
            return template, True
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 409:
                # If we got a conflict, extract the existing template ID and fetch it
                error_data = e.response.json()
                template_id = error_data.get("prompt_template_id")
                if template_id is None:
                    raise ValueError("Received 409 without prompt_template_id") from e

                response = await self.async_session.get(
                    f"{self.project_route_prefix}/prompt_templates/{template_id}",
                )
                raise_for_status_with_detail(response)
                return PromptTemplate.model_validate(response.json()), False
            raise

    def get_or_create_prompt_template(
        self,
        user_prompt_template: str,
        *,
        name: str,
        parent_prompt_template_id: int | None = None,
        default_collection_id: int | None = None,
    ) -> tuple[PromptTemplate, bool]:
        """Gets the prompt template by its name and user prompt contents if it exists.
        If the prompt template name does not exist, it creates a new prompt template with version 1.
        If a prompt template with the same name exists, but the user prompt is new,
        then it creates a new prompt template version with the new user prompt
        which will be the new latest version.

        Args:
            user_prompt_template (str): The template string containing variables in {{variable}} format.
            name (str): Name for the template.
            parent_prompt_template_id (int | None): Optional ID of parent template to inherit from.
            default_collection_id (int | None): Optional ID of default template variables collection.

        Returns:
            tuple[PromptTemplate, bool]: A tuple containing:
                - The prompt template
                - Boolean indicating if a new template was created (True) or existing one returned (False)

        Raises:
            ValueError: If a 409 response is received without a prompt_template_id.

        """
        return run_async(self.aget_or_create_prompt_template)(
            user_prompt_template,
            name=name,
            parent_prompt_template_id=parent_prompt_template_id,
            default_collection_id=default_collection_id,
        )

    async def adelete_prompt_template(
        self,
        prompt_template: PromptTemplate,
    ) -> None:
        """Async version of delete_prompt_template."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/prompt_templates/{prompt_template.id}",
        )
        raise_for_status_with_detail(response)

    def delete_prompt_template(
        self,
        prompt_template: PromptTemplate,
    ) -> None:
        """Deletes a prompt template.

        Args:
            prompt_template (PromptTemplate): The prompt template to delete.

        Raises:
            httpx.HTTPStatusError: If the prompt template doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete_prompt_template)(prompt_template)

    async def acreate_llm_config(
        self,
        name: str,
        llm_model_name: str,
        api_key: str,
        *,
        description: str = "",
        llm_base_url: str | None = None,
        api_version: str | None = None,
        max_connections: int = 10,
        max_retries: int | None = None,
        timeout: int | None = None,
        system_message: str | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        temperature: float | None = None,
        best_of: int | None = None,
        top_k: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
    ) -> LLMConfig:
        """Async version of create_llm_config."""
        # The create request data is the same as the `LLMConfig`, just without the ID
        create_request_data = LLMConfig(
            name=name,
            description=description,
            llm_model_name=llm_model_name,
            api_key=api_key,
            llm_base_url=llm_base_url,
            api_version=api_version,
            max_connections=max_connections,
            max_retries=max_retries,
            timeout=timeout,
            system_message=system_message,
            max_tokens=max_tokens,
            top_p=top_p,
            temperature=temperature,
            best_of=best_of,
            top_k=top_k,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
        ).model_dump(exclude={"id"})
        response = await self.async_session.post(
            f"{self.project_route_prefix}/llm_configs",
            json=create_request_data,
        )
        raise_for_status_with_detail(response)
        return LLMConfig.model_validate(response.json())

    def create_llm_config(
        self,
        name: str,
        llm_model_name: str,
        api_key: str,
        *,
        description: str = "",
        llm_base_url: str | None = None,
        api_version: str | None = None,
        max_connections: int = 10,
        max_retries: int | None = None,
        timeout: int | None = None,
        system_message: str | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        temperature: float | None = None,
        best_of: int | None = None,
        top_k: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
    ) -> LLMConfig:
        """Create a new LLM configuration.

        Args:
            name (str): Name for the LLM config.
            llm_model_name (str): Name of the LLM model.
            api_key (str): API key for the LLM service.
            description (str): Optional description for the LLM config.
            llm_base_url (str | None): Optional base URL for the LLM service.
            api_version (str | None): Optional API version.
            max_connections (int): Maximum number of concurrent connections to the LLM provider.
            max_retries (int | None): Optional maximum number of retries.
            timeout (int | None): Optional timeout in seconds.
            system_message (str | None): Optional system message for the LLM.
            max_tokens (int | None): Optional maximum tokens to generate.
            top_p (float | None): Optional nucleus sampling parameter.
            temperature (float | None): Optional temperature parameter.
            best_of (int | None): Optional number of completions to generate.
            top_k (int | None): Optional top-k sampling parameter.
            logprobs (bool | None): Optional flag to return log probabilities.
            top_logprobs (int | None): Optional number of top log probabilities to return.

        Returns:
            (LLMConfig): The created LLM configuration.

        Raises:
            httpx.HTTPStatusError: If an LLM config with the same name already exists.

        """
        return run_async(self.acreate_llm_config)(
            name,
            llm_model_name,
            api_key,
            description=description,
            llm_base_url=llm_base_url,
            api_version=api_version,
            max_connections=max_connections,
            max_retries=max_retries,
            timeout=timeout,
            system_message=system_message,
            max_tokens=max_tokens,
            top_p=top_p,
            temperature=temperature,
            best_of=best_of,
            top_k=top_k,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
        )

    async def aget_llm_config(self, name: str) -> LLMConfig:
        """Sync version of aget_llm_config."""
        response = await self.async_session.get(
            f"{self.project_route_prefix}/llm_configs",
            params={"name": name},
        )
        raise_for_status_with_detail(response)
        configs = [LLMConfig.model_validate(config) for config in response.json()["items"]]
        if not configs:
            raise ValueError(f"No LLM config found with name '{name}'")
        return configs[0]

    def get_llm_config(self, name: str) -> LLMConfig:
        """Get an LLM config by name.

        Args:
            name (str): Name of the LLM config.

        Returns:
            (LLMConfig): The requested LLM config.

        Raises:
            ValueError: If no LLM config is found with the given name.

        """
        return run_async(self.aget_llm_config)(name=name)

    async def aget_or_create_llm_config(
        self,
        name: str,
        llm_model_name: str | None = None,
        api_key: str | None = None,
        *,
        description: str = "",
        llm_base_url: str | None = None,
        api_version: str | None = None,
        max_connections: int = 10,
        max_retries: int | None = None,
        timeout: int | None = None,
        system_message: str | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        temperature: float | None = None,
        best_of: int | None = None,
        top_k: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
    ) -> tuple[LLMConfig, bool]:
        """Async version of get_or_create_llm_config."""
        # First try to get by name
        try:
            llm_config = await self.aget_llm_config(name=name)
            return llm_config, False
        except ValueError:
            pass  # Continue to creation

        # Some input sanity checks
        if llm_model_name is None:
            raise ValueError("`llm_model_name` is required to create a new LLM config")
        if api_key is None:
            raise ValueError("`api_key` is required to create a new LLM config")

        logger.info("No matching LLM config found. Creating a new config.")
        llm_config = await self.acreate_llm_config(
            name=name,
            description=description,
            llm_model_name=llm_model_name,
            api_key=api_key,
            llm_base_url=llm_base_url,
            api_version=api_version,
            max_connections=max_connections,
            max_retries=max_retries,
            timeout=timeout,
            system_message=system_message,
            max_tokens=max_tokens,
            top_p=top_p,
            temperature=temperature,
            best_of=best_of,
            top_k=top_k,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
        )
        return llm_config, True

    def get_or_create_llm_config(
        self,
        name: str,
        llm_model_name: str,
        api_key: str,
        *,
        description: str = "",
        llm_base_url: str | None = None,
        api_version: str | None = None,
        max_connections: int = 10,
        max_retries: int | None = None,
        timeout: int | None = None,
        system_message: str | None = None,
        max_tokens: int | None = None,
        top_p: float | None = None,
        temperature: float | None = None,
        best_of: int | None = None,
        top_k: int | None = None,
        logprobs: bool | None = None,
        top_logprobs: int | None = None,
    ) -> tuple[LLMConfig, bool]:
        """Get an existing LLM config or create a new one.

        The existence check is only based on the name parameter - if an LLM config with
        the given name exists, it will be returned regardless of the other parameters.
        If no config with that name exists, a new one will be created using all provided
        parameters.

        Args:
            name (str): Name for the LLM config.
            llm_model_name (str): Name of the LLM model.
            api_key (str): API key for the LLM service.
            description (str): Optional description for the LLM config.
            llm_base_url (str | None): Optional base URL for the LLM service.
            api_version (str | None): Optional API version.
            max_connections (int): Maximum number of concurrent connections to the LLM provider.
            max_retries (int | None): Optional maximum number of retries.
            timeout (int | None): Optional timeout in seconds.
            system_message (str | None): Optional system message for the LLM.
            max_tokens (int | None): Optional maximum tokens to generate.
            top_p (float | None): Optional nucleus sampling parameter.
            temperature (float | None): Optional temperature parameter.
            best_of (int | None): Optional number of completions to generate.
            top_k (int | None): Optional top-k sampling parameter.
            logprobs (bool | None): Optional flag to return log probabilities.
            top_logprobs (int | None): Optional number of top log probabilities to return.

        Returns:
            tuple[LLMConfig, bool]: A tuple containing:
                - The LLM configuration
                - Boolean indicating if a new config was created (True) or existing one returned (False)

        """
        return run_async(self.aget_or_create_llm_config)(
            name=name,
            description=description,
            llm_model_name=llm_model_name,
            api_key=api_key,
            llm_base_url=llm_base_url,
            api_version=api_version,
            max_connections=max_connections,
            max_retries=max_retries,
            timeout=timeout,
            system_message=system_message,
            max_tokens=max_tokens,
            top_p=top_p,
            temperature=temperature,
            best_of=best_of,
            top_k=top_k,
            logprobs=logprobs,
            top_logprobs=top_logprobs,
        )

    async def adelete_llm_config(self, llm_config: LLMConfig) -> None:
        """Async version of delete_llm_config."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/llm_configs/{llm_config.id}",
        )
        raise_for_status_with_detail(response)

    def delete_llm_config(self, llm_config: LLMConfig) -> None:
        """Deletes an LLM configuration.

        Args:
            llm_config (LLMConfig): The LLM configuration to delete.

        Raises:
            httpx.HTTPStatusError: If the LLM config doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete_llm_config)(llm_config)

    async def _form_response_request_helper(
        self,
        prompt_template: PromptTemplate,
        *,
        llm_config: LLMConfig | None = None,
        response: str | None = None,
        template_variables: dict[str, str] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        template_variables_id: int | None = None,
        metadata: LLMConfig | GenerationMetadata | None = None,
    ) -> CreatePromptResponseRequest:
        """Helper function for creating responses."""
        # Validate that a response cannot be provided along with a llm_config
        if llm_config is not None and (response is not None or metadata is not None):
            raise ValueError("A llm_config cannot be provided along with a response or metadata.")

        if template_variables_id is None and template_variables is not None:
            if template_variables_collection is None:
                template_variables_collection = prompt_template.default_template_variables_collection

            if template_variables_collection is None:
                raise ValueError("No template variables collection specified")

            variables_response, _ = await self.aget_or_add_entry(
                template_variables_collection,
                template_variables,
            )
            template_variables_id = variables_response.id

        # If metadata is an LLMConfig, wrap it in GenerationMetadata
        if isinstance(metadata, LLMConfig):
            metadata = GenerationMetadata(
                llm_model_config=metadata,
            )

        request_data = CreatePromptResponseRequest(
            llm_config_id=llm_config.id if llm_config else None,
            response=response,
            prompt_template_id=prompt_template.id,
            template_variables_id=template_variables_id,
            metadata=metadata,
        )
        return request_data

    async def _form_batch_response_request_helper(
        self,
        prompt_template: PromptTemplate,
        *,
        batch_responses: list[str] | None = None,
        batch_template_variables: list[dict[str, str]] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        batch_template_variables_ids: list[int] | None = None,
        llm_config: LLMConfig | None = None,
        batch_metadata: list[LLMConfig | GenerationMetadata | None] | None = None,
    ) -> BatchCreatePromptResponseRequest:
        # Get length from first non-None list parameter
        n_responses = None
        for param_list in [batch_responses, batch_template_variables, batch_template_variables_ids, batch_metadata]:
            if param_list is not None:
                n_responses = len(param_list)
                break

        if n_responses is None:
            raise ValueError("Batch inputs must be provided.")

        # Validate all non-None lists have matching length
        for param_name, param_list in [
            ("batch_responses", batch_responses),
            ("batch_template_variables", batch_template_variables),
            ("batch_template_variables_ids", batch_template_variables_ids),
            ("batch_metadata", batch_metadata),
        ]:
            if param_list is not None and len(param_list) != n_responses:
                raise ValueError(f"Expected {n_responses} {param_name} entries, got {len(param_list)}")

        # Transform `None` list parameters into lists of `None` values
        processed_params = {
            "batch_responses": batch_responses,
            "batch_template_variables": batch_template_variables,
            "batch_template_variables_ids": batch_template_variables_ids,
            "batch_metadata": batch_metadata,
        }

        processed_params = {
            key: value if value is not None else [None] * n_responses for key, value in processed_params.items()
        }

        # Create the batch request
        batch_request_data = [
            await self._form_response_request_helper(
                prompt_template,
                llm_config=llm_config,
                response=response,
                template_variables=template_variables,
                template_variables_collection=template_variables_collection,
                template_variables_id=template_variables_id,
                metadata=metadata,
            )
            for response, template_variables, template_variables_id, metadata in zip(
                processed_params["batch_responses"],
                processed_params["batch_template_variables"],
                processed_params["batch_template_variables_ids"],
                processed_params["batch_metadata"],
            )
        ]

        return BatchCreatePromptResponseRequest(
            prompt_response_ins=batch_request_data,
        )

    @retry_request
    async def aadd_response(
        self,
        prompt_template: PromptTemplate,
        response: str,
        *,
        template_variables: dict[str, str] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        template_variables_id: int | None = None,
        metadata: LLMConfig | GenerationMetadata | None = None,
    ) -> PromptResponse:
        """Async version of add_response."""
        async with self._semaphore:
            request_data = await self._form_response_request_helper(
                prompt_template,
                llm_config=None,
                response=response,
                template_variables=template_variables,
                template_variables_collection=template_variables_collection,
                template_variables_id=template_variables_id,
                metadata=metadata,
            )

            _response = await self.async_session.post(
                f"{self.project_route_prefix}/responses",
                json=request_data.model_dump(),
            )
            raise_for_status_with_detail(_response)
            return PromptResponse.model_validate(_response.json())

    def add_response(
        self,
        prompt_template: PromptTemplate,
        response: str,
        *,
        template_variables: dict[str, str] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        template_variables_id: int | None = None,
        metadata: LLMConfig | GenerationMetadata | None = None,
    ) -> PromptResponse:
        """Add a response to a prompt template.

        Args:
            prompt_template (PromptTemplate): The prompt template to add the response to.
            response (str): The response to add.
            template_variables (dict[str, str] | None): The template variables to use for the response.
            template_variables_collection (TemplateVariablesCollection | None): The collection to use for the template variables.
            template_variables_id (int | None): The ID of the template variables to use.
            metadata (LLMConfig | GenerationMetadata | None): Optional metadata to associate with the response.

        Returns:
            PromptResponse: The newly created prompt response object.

        """
        return run_async(self.aadd_response)(
            prompt_template,
            response,
            template_variables=template_variables,
            template_variables_collection=template_variables_collection,
            template_variables_id=template_variables_id,
            metadata=metadata,
        )

    @retry_request
    async def abatch_add_responses(
        self,
        prompt_template: PromptTemplate,
        batch_responses: list[str],
        *,
        batch_template_variables: list[dict[str, str]] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        batch_template_variables_ids: list[int] | None = None,
        batch_metadata: list[LLMConfig | GenerationMetadata | None] | None = None,
        timeout: float | None = None,
    ) -> list[PromptResponse]:
        """Async version of batch_add_responses."""
        request_data = await self._form_batch_response_request_helper(
            prompt_template,
            batch_responses=batch_responses,
            batch_template_variables=batch_template_variables,
            template_variables_collection=template_variables_collection,
            batch_template_variables_ids=batch_template_variables_ids,
            llm_config=None,
            batch_metadata=batch_metadata,
        )
        async with self._semaphore:
            response = await self.async_session.post(
                f"{self.project_route_prefix}/responses/batches",
                json=request_data.model_dump(),
            )
            raise_for_status_with_detail(response)
            task_id = response.json()

        start_time = time.time()
        while timeout is None or time.time() - start_time < timeout:
            # For the status
            response = await self.async_session.get(
                f"{self.project_route_prefix}/responses/batches/{task_id}",
            )
            raise_for_status_with_detail(response)
            status = BatchCreatePromptResponseStatus.model_validate(response.json())
            if status.status == "FAILURE":
                raise RuntimeError(f"Failed to batch add responses. Status error message: {status.error_msg}")
            elif status.status == "SUCCESS":
                result = status.result
                if result is None:
                    raise RuntimeError("Failed to batch add responses.")
                else:
                    return result

            # Delay before looping again
            await asyncio.sleep(3)
        else:
            raise TimeoutError("Batch add responses timed out.")

    def batch_add_responses(
        self,
        prompt_template: PromptTemplate,
        batch_responses: list[str],
        *,
        batch_template_variables: list[dict[str, str]] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        batch_template_variables_ids: list[int] | None = None,
        batch_metadata: list[LLMConfig | GenerationMetadata | None] | None = None,
        timeout: float | None = None,
    ) -> list[PromptResponse]:
        """Batched version of add_response.

        Args:
            prompt_template (PromptTemplate): The prompt template to add responses to.
            batch_responses (list[str]): List of responses to add.
            batch_template_variables (list[dict[str, str]] | None): List of template variables for each response.
            template_variables_collection (TemplateVariablesCollection | None): The collection to use for the template variables.
            batch_template_variables_ids (list[int] | None): List of template variable IDs for each response.
            batch_metadata (list[LLMConfig | GenerationMetadata | None] | None): List of metadata for each response.
            timeout (float): Timeout in seconds for API requests. Defaults to no timeout.

        Returns:
            list[PromptResponse]: List of newly created prompt response objects.

        """
        return run_async(self.abatch_add_responses)(
            prompt_template,
            batch_responses,
            batch_template_variables=batch_template_variables,
            template_variables_collection=template_variables_collection,
            batch_template_variables_ids=batch_template_variables_ids,
            batch_metadata=batch_metadata,
            timeout=timeout,
        )

    @retry_request
    async def agenerate_response(
        self,
        prompt_template: PromptTemplate,
        *,
        template_variables: dict[str, str] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        template_variables_id: int | None = None,
        llm_config: LLMConfig | None = None,
    ) -> PromptResponse:
        """Async version of generate_response."""
        async with self._semaphore:
            request_data = await self._form_response_request_helper(
                prompt_template,
                llm_config=llm_config,
                response=None,
                template_variables=template_variables,
                template_variables_collection=template_variables_collection,
                template_variables_id=template_variables_id,
                metadata=None,
            )

            if llm_config and llm_config.id is None:
                logger.warning("The LLM config id is None. Using default LLM config.")

            response = await self.async_session.post(
                f"{self.project_route_prefix}/responses",
                json=request_data.model_dump(),
            )
            raise_for_status_with_detail(response)
            return PromptResponse.model_validate(response.json())

    def generate_response(
        self,
        prompt_template: PromptTemplate,
        *,
        llm_config: LLMConfig | None = None,
        template_variables: dict[str, str] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        template_variables_id: int | None = None,
    ) -> PromptResponse:
        """Generate a response for a prompt template using an LLM.

        This method sends the prompt to an LLM for generation. If no LLM config is provided,
        the project's default LLM config will be used.

        Args:
            prompt_template (PromptTemplate): The prompt template to generate a response for.
            llm_config (LLMConfig | None): Optional LLM configuration to use for generation.
                If not provided, the project's default config will be used.
            template_variables (dict[str, str] | None): Dictionary of variables to populate
                the template. Required if the prompt template contains variables. If provided,
                these variables will be added to the template's default collection or the
                specified collection.
            template_variables_collection (TemplateVariablesCollection | None): Optional collection
                to store the template variables in. If not provided and template_variables is given,
                the template's default collection will be used.
            template_variables_id (int | None): Optional ID of existing template variables to use.
                If provided, template_variables and template_variables_collection are ignored.

        Returns:
            PromptResponse: The generated response object

        Raises:
            ValueError: If no template variables source is provided (either template_variables or template_variables_id)

        """
        return run_async(self.agenerate_response)(
            prompt_template,
            llm_config=llm_config,
            template_variables=template_variables,
            template_variables_collection=template_variables_collection,
            template_variables_id=template_variables_id,
        )

    @retry_request
    async def abatch_generate_responses(
        self,
        prompt_template: PromptTemplate,
        *,
        batch_template_variables: list[dict[str, str]] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        batch_template_variables_ids: list[int] | None = None,
        llm_config: LLMConfig | None = None,
        batch_metadata: list[LLMConfig | GenerationMetadata | None] | None = None,
        timeout: float | None = None,
    ) -> list[PromptResponse]:
        """Async version of batch_generate_responses."""
        request_data = await self._form_batch_response_request_helper(
            prompt_template,
            batch_responses=None,
            batch_template_variables=batch_template_variables,
            template_variables_collection=template_variables_collection,
            batch_template_variables_ids=batch_template_variables_ids,
            llm_config=llm_config,
            batch_metadata=batch_metadata,
        )

        if llm_config and llm_config.id is None:
            logger.warning("The LLM config id is None. Using default LLM config.")

        async with self._semaphore:
            response = await self.async_session.post(
                f"{self.project_route_prefix}/responses/batches",
                json=request_data.model_dump(),
            )
            raise_for_status_with_detail(response)
            task_id = response.json()

        start_time = time.time()
        while timeout is None or time.time() - start_time < timeout:
            # For the status
            response = await self.async_session.get(
                f"{self.project_route_prefix}/responses/batches/{task_id}",
            )
            raise_for_status_with_detail(response)
            status = BatchCreatePromptResponseStatus.model_validate(response.json())
            if status.status == "FAILURE":
                raise RuntimeError(f"Failed to batch add responses. Status error message: {status.error_msg}")
            elif status.status == "SUCCESS":
                result = status.result
                if result is None:
                    raise RuntimeError("Failed to batch add responses.")
                else:
                    return result

            # Delay before looping again
            await asyncio.sleep(3)
        else:
            raise TimeoutError("Batch add responses timed out.")

    def batch_generate_responses(
        self,
        prompt_template: PromptTemplate,
        *,
        batch_template_variables: list[dict[str, str]] | None = None,
        template_variables_collection: TemplateVariablesCollection | None = None,
        batch_template_variables_ids: list[int] | None = None,
        llm_config: LLMConfig | None = None,
        batch_metadata: list[LLMConfig | GenerationMetadata | None] | None = None,
        timeout: float | None = None,
    ) -> list[PromptResponse]:
        """Batch version of generate_response.

        Args:
            prompt_template (PromptTemplate): The prompt template to use for generation.
            batch_template_variables (list[dict[str, str]] | None): List of template variables for each response.
            template_variables_collection (TemplateVariablesCollection | None): The collection to use for the template variables.
            batch_template_variables_ids (list[int] | None): List of template variable IDs for each response.
            llm_config (LLMConfig | None): Optional LLMConfig to use for generation.
            batch_metadata (list[LLMConfig | GenerationMetadata | None] | None): List of metadata for each response.
            timeout (float): Timeout in seconds for API requests. Defaults to no timeout.

        Returns:
            list[PromptResponse]: List of newly created prompt response objects.

        """
        return run_async(self.abatch_generate_responses)(
            prompt_template,
            batch_template_variables=batch_template_variables,
            template_variables_collection=template_variables_collection,
            batch_template_variables_ids=batch_template_variables_ids,
            llm_config=llm_config,
            batch_metadata=batch_metadata,
            timeout=timeout,
        )

    async def aget_responses(
        self,
        prompt_id: int | None = None,
        prompt_template_id: int | None = None,
        template_variables_id: int | None = None,
    ) -> list[PromptResponse]:
        """Async version of get_responses."""
        params = {}
        if prompt_id is not None:
            params["prompt_id"] = prompt_id
        if prompt_template_id is not None:
            params["prompt_template_id"] = prompt_template_id
        if template_variables_id is not None:
            params["template_variables_id"] = template_variables_id

        async def fetch_page(params: dict) -> tuple[list[PromptResponse], int]:
            response = await self.async_session.get(
                f"{self.project_route_prefix}/responses",
                params=params,
            )
            raise_for_status_with_detail(response)
            data = response.json()
            return [PromptResponse.model_validate(r) for r in data["items"]], data["count"]

        return await self._apaginate(fetch_page, params, "responses")

    def get_responses(
        self,
        prompt_id: int | None = None,
        prompt_template_id: int | None = None,
        template_variables_id: int | None = None,
    ) -> list[PromptResponse]:
        """Get the responses for a prompt template.

        Args:
            prompt_id (int | None): The ID of the prompt to get responses for.
            prompt_template_id (int | None): The ID of the prompt template to get responses for.
            template_variables_id (int | None): The ID of the template variables to get responses for.

        Returns:
            list[PromptResponse]: The list of prompt responses.

        """
        return run_async(self.aget_responses)(
            prompt_id=prompt_id, prompt_template_id=prompt_template_id, template_variables_id=template_variables_id
        )

    async def agenerate_responses_from_collection(
        self,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        *,
        llm_config: LLMConfig | None = None,
    ) -> list[PromptResponse]:
        """Async version of generate_responses_from_collection."""
        entries = await self.aget_entries(collection)
        return await self.abatch_generate_responses(
            prompt_template,
            batch_template_variables_ids=[template_variables.id for template_variables in entries],
            llm_config=llm_config,
        )

    def generate_responses_from_collection(
        self,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        *,
        llm_config: LLMConfig | None = None,
    ) -> list[PromptResponse]:
        """Generates responses using the template for all entries in the collection.

        This method batches the generation requests and processes them asynchronously on the server.
        All responses will be generated using the same LLM configuration.

        Args:
            prompt_template (PromptTemplate): The prompt template to use for generation.
            collection (TemplateVariablesCollection): Collection containing template variables.
            llm_config (LLMConfig | None): Optional LLMConfig to use for generation.
                If not provided, the project's default LLM config will be used.

        Returns:
            list[PromptResponse]: List of generated response objects.

        """
        return run_async(self.agenerate_responses_from_collection)(
            prompt_template, collection, llm_config=llm_config
        )

    @retry_request
    async def aadd_criteria(
        self,
        prompt_template: PromptTemplate,
        criteria: list[str],
        *,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> list[Criterion]:
        """Async version of add_criteria."""
        request_data = GenerateCriteriaRequest(
            prompt_template_id=prompt_template.id,
            criteria=criteria,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )
        response = await self.async_session.post(
            f"{self.project_route_prefix}/criteria",
            json=request_data.model_dump(),
        )
        raise_for_status_with_detail(response)
        return [Criterion.model_validate(criterion) for criterion in response.json()]

    def add_criteria(
        self,
        prompt_template: PromptTemplate,
        criteria: list[str],
        *,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> list[Criterion]:
        """Adds custom evaluation criteria to the prompt template.

        This method creates criteria from the provided list. If criteria with the same strings
        already exist for this prompt template, they will be reused rather than duplicated.

        Args:
            prompt_template (PromptTemplate): The prompt template to add criteria to.
            criteria (list[str]): List of criterion strings to add.
            criterion_set (str | None): Optional name to group related criteria together. If not provided, a default name is used.
            delete_existing (bool): If True, deletes any existing criteria for this prompt template
                before adding the new ones. Defaults to False.

        Returns:
            list[Criterion]: List of created and/or existing criterion objects.

        Raises:
            httpx.HTTPStatusError: If the prompt template doesn't belong to the project,
                or other API errors occur.

        """
        return run_async(self.aadd_criteria)(
            prompt_template,
            criteria,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )

    @retry_request
    async def agenerate_criteria(
        self,
        prompt_template: PromptTemplate,
        *,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> list[Criterion]:
        """Async version of generate_criteria."""
        request_data = GenerateCriteriaRequest(
            prompt_template_id=prompt_template.id,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )
        response = await self.async_session.post(
            f"{self.project_route_prefix}/criteria",
            json=request_data.model_dump(),
        )
        raise_for_status_with_detail(response)
        return [Criterion.model_validate(criterion) for criterion in response.json()]

    def generate_criteria(
        self,
        prompt_template: PromptTemplate,
        *,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> list[Criterion]:
        """Automatically generates evaluation criteria for the prompt template using an LLM.

        This method uses the project's default LLM to analyze the prompt template and generate
        appropriate evaluation criteria. If template variables are provided, the criteria will be
        generated based on the rendered prompt with those variables.

        Args:
            prompt_template (PromptTemplate): The prompt template to generate criteria for.
            criterion_set (str | None): Optional name to group related criteria together. If not provided, a default name is used.
            delete_existing (bool): If True, deletes any existing criteria before generating
                new ones. If False and criteria exist, raises an error. Defaults to False.

        Returns:
            list[Criterion]: List of generated criterion objects. Each criterion includes
                the generation metadata from the LLM.

        Raises:
            httpx.HTTPStatusError: If criteria already exist and delete_existing is False, if the template variables are not found in the project, template variables don't match the template

        """
        return run_async(self.agenerate_criteria)(
            prompt_template,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )

    async def aget_criteria(self, prompt_template: PromptTemplate) -> list[Criterion]:
        """Async version of get_criteria."""
        params = {"prompt_template_id": prompt_template.id}

        async def fetch_page(params: dict) -> tuple[list[Criterion], int]:
            response = await self.async_session.get(
                f"{self.project_route_prefix}/criteria",
                params=params,
            )
            raise_for_status_with_detail(response)
            data = response.json()
            return [Criterion.model_validate(criterion) for criterion in data["items"]], data["count"]

        return await self._apaginate(fetch_page, params, "criteria")

    def get_criteria(self, prompt_template: PromptTemplate) -> list[Criterion]:
        """Get the evaluation criteria for a prompt template.

        This method retrieves all criteria associated with the prompt template. If template
        variables are provided, only criteria specific to those variables will be returned.

        Args:
            prompt_template (PromptTemplate): The prompt template to get criteria for.

        Returns:
            list[Criterion]: List of criterion objects, ordered by creation date.

        """
        return run_async(self.aget_criteria)(prompt_template)

    async def adelete_criteria(self, prompt_template: PromptTemplate) -> None:
        """Async version of delete_criteria."""
        # TODO: Remove this once we've migrated to the new 'delete_criterionset' method
        logger.warning(
            "Attention: Starting with Service version 2.2.3, this function will delete ALL criteria for the given prompt template, even those that are used for multiple prompt templates. Please migrate to the new 'delete_criterionset' method or delete Criteria individually!"
        )
        params = {"prompt_template_id": prompt_template.id}
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/criteria",
            params=params,
        )
        raise_for_status_with_detail(response)

    def delete_criteria(self, prompt_template: PromptTemplate) -> None:
        """Delete the evaluation criteria for a prompt template.

        This method deletes all criteria associated with the given prompt template. If template
        variables are provided, only criteria specific to those variables will be deleted.

        Args:
            prompt_template (PromptTemplate): The prompt template to delete criteria for.

        Raises:
            httpx.HTTPStatusError: If the prompt template or the template variables don't exist.

        """
        return run_async(self.adelete_criteria)(prompt_template)

    async def aget_or_generate_criteria(
        self,
        prompt_template: PromptTemplate,
        *,
        criterion_set: str | None = None,
    ) -> tuple[list[Criterion], bool]:
        """Async version of get_or_generate_criteria."""
        criteria = await self.aget_criteria(prompt_template)
        if criteria:
            return criteria, False

        return await self.agenerate_criteria(prompt_template, criterion_set=criterion_set), True

    def get_or_generate_criteria(
        self,
        prompt_template: PromptTemplate,
        *,
        criterion_set: str | None = None,
    ) -> tuple[list[Criterion], bool]:
        """Gets existing criteria or generates new ones if none exist.

        This method first attempts to retrieve existing criteria. If no criteria are found,
        it automatically generates new ones using an LLM.

        Args:
            prompt_template (PromptTemplate): The prompt template to get or generate criteria for.
            criterion_set (str | None): Optional name to group related criteria together. If not provided, a default name is used.

        Returns:
            tuple[list[Criterion], bool]: A tuple containing:
                - List of criterion objects, either existing or newly generated
                - Boolean indicating if criteria were generated (True) or existing ones returned (False)

        Raises:
            httpx.HTTPStatusError: If criteria already exist and delete_existing is False, if the template variables are not found in the project, template variables don't match the template

        """
        return run_async(self.aget_or_generate_criteria)(prompt_template, criterion_set=criterion_set)

    async def adelete_criterion(
        self,
        criterion: Criterion,
    ) -> None:
        """Async version of delete_criterion."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/criteria/{criterion.id}",
        )
        raise_for_status_with_detail(response)

    def delete_criterion(
        self,
        criterion: Criterion,
    ) -> None:
        """Deletes an evaluation criterion.

        Args:
            criterion (Criterion): The criterion to delete.
                This will also delete any associated ratings.

        Raises:
            httpx.HTTPStatusError: If the criterion doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete_criterion)(criterion)

    async def acreate_collection(
        self, *, name: str | None = None, description: str = ""
    ) -> TemplateVariablesCollection:
        """Async version of create_collection."""
        response = await self.async_session.post(
            f"{self.project_route_prefix}/collections",
            json=CreateCollectionRequest(name=name, description=description).model_dump(),
        )
        raise_for_status_with_detail(response)
        return TemplateVariablesCollection.model_validate(response.json())

    def create_collection(self, *, name: str | None = None, description: str = "") -> TemplateVariablesCollection:
        """Creates a new collection.

        Args:
            name (str | None): The name for the new collection.
            description (str): Optional description for the collection.

        Returns:
            (TemplateVariablesCollection): The newly created collection object.

        Raises:
            httpx.HTTPStatusError: If collection with same name already exists (400 BAD REQUEST)

        """
        return run_async(self.acreate_collection)(name=name, description=description)

    async def aget_collection(self, *, name: str) -> TemplateVariablesCollection:
        """Async version of get_collection."""
        response = await self.async_session.get(
            f"{self.project_route_prefix}/collections",
            params={"name": name},
        )
        raise_for_status_with_detail(response)
        collections = [TemplateVariablesCollection.model_validate(c) for c in response.json()["items"]]
        if not collections:
            raise ValueError(f"No collection found with name '{name}'")
        return collections[0]

    def get_collection(self, *, name: str) -> TemplateVariablesCollection:
        """Get a collection by name.

        Args:
            name (str): The name of the collection to get.

        Returns:
            TemplateVariablesCollection: The collection object.

        Raises:
            ValueError: If no collection is found with the given name.

        """
        return run_async(self.aget_collection)(name=name)

    async def aget_or_create_collection(
        self,
        *,
        name: str,
        description: str = "",
    ) -> tuple[TemplateVariablesCollection, bool]:
        try:
            return await self.acreate_collection(name=name, description=description), True
        except httpx.HTTPStatusError as e:
            # Code 409 means resource already exists, simply get and return it
            if e.response.status_code == 409:
                return await self.aget_collection(name=name), False
            raise  # Re-raise any other HTTP status errors

    def get_or_create_collection(
        self,
        *,
        name: str,
        description: str = "",
    ) -> tuple[TemplateVariablesCollection, bool]:
        """Gets an existing collection by name or creates a new one if it doesn't exist.

        Args:
            name: The name of the collection to get or create.
            description: Optional description for the collection if created.

        Returns:
            tuple[TemplateVariablesCollection, bool]: A tuple containing:
                - Collection: The retrieved or created collection object
                - bool: True if a new collection was created, False if existing was found

        """
        return run_async(self.aget_or_create_collection)(name=name, description=description)

    async def adelete_collection(
        self,
        collection: TemplateVariablesCollection,
    ) -> None:
        """Async version of delete_collection."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/collections/{collection.id}",
        )
        raise_for_status_with_detail(response)

    def delete_collection(
        self,
        collection: TemplateVariablesCollection,
    ) -> None:
        """Deletes a template variables collection.

        Args:
            collection (TemplateVariablesCollection): The collection to delete.

        Raises:
            httpx.HTTPStatusError: If the collection doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete_collection)(collection)

    async def aget_entries(
        self,
        collection: TemplateVariablesCollection,
    ) -> list[TemplateVariables]:
        """Async version of get_entries."""

        async def fetch_page(params: dict) -> tuple[list[TemplateVariables], int]:
            response = await self.async_session.get(
                f"{self.project_route_prefix}/collections/{collection.id}/entries",
                params=params,
            )
            raise_for_status_with_detail(response)
            data = response.json()
            return [TemplateVariables.model_validate(entry) for entry in data["items"]], data["count"]

        return await self._apaginate(fetch_page, {}, "collection entries")

    def get_entries(
        self,
        collection: TemplateVariablesCollection,
    ) -> list[TemplateVariables]:
        """Get the entries for a collection.

        Args:
            collection (TemplateVariablesCollection): The collection to get entries for.

        Returns:
            list[TemplateVariables]: List of template variables entries.

        Raises:
            httpx.HTTPStatusError: If the collection is not found

        """
        return run_async(self.aget_entries)(collection)

    async def aget_or_add_entry(
        self,
        collection: TemplateVariablesCollection,
        template_variables: dict[str, str],
    ) -> tuple[TemplateVariables, bool]:
        async with self._semaphore:
            response = await self.async_session.post(
                f"{self.project_route_prefix}/collections/{collection.id}/entries",
                json=CreateTemplateVariablesRequest(input_values=template_variables).model_dump(),
            )
            raise_for_status_with_detail(response)
            return TemplateVariables.model_validate(response.json()), response.status_code == 201

    def get_or_add_entry(
        self,
        collection: TemplateVariablesCollection,
        template_variables: dict[str, str],
    ) -> tuple[TemplateVariables, bool]:
        """Gets an existing entry or adds a new entry to a collection.

        Args:
            collection (TemplateVariablesCollection): The collection to get or add the entry to.
            template_variables (dict[str, str]): The template variables to get or add.

        Returns:
            tuple[TemplateVariables, bool]: A tuple containing:
                - TemplateVariables: The retrieved or created template variables object
                - bool: True if a new entry was created, False if existing was found

        """
        return run_async(self.aget_or_add_entry)(collection, template_variables)

    @deprecated(alternative="adelete_entry")
    async def aremove_entry(
        self,
        collection: TemplateVariablesCollection,
        template_variables: TemplateVariables,
    ) -> None:
        """Async version of remove_entry."""
        return await self.adelete_entry(collection, template_variables)

    @deprecated(alternative="delete_entry")
    def remove_entry(
        self,
        collection: TemplateVariablesCollection,
        template_variables: TemplateVariables,
    ) -> None:
        """Deletes a template variables entry.

        Args:
            collection (TemplateVariablesCollection): The collection containing the entry.
            template_variables (TemplateVariables): The template variables entry to delete.

        Raises:
            httpx.HTTPStatusError: If the entry doesn't exist, belongs to a different collection,
                or belongs to a different project.

        """
        return run_async(self.aremove_entry)(collection, template_variables)

    async def adelete_entry(
        self,
        collection: TemplateVariablesCollection,
        template_variables: TemplateVariables,
    ) -> None:
        """Async version of delete_entry."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/collections/{collection.id}/entries/{template_variables.id}",
        )
        raise_for_status_with_detail(response)

    def delete_entry(
        self,
        collection: TemplateVariablesCollection,
        template_variables: TemplateVariables,
    ) -> None:
        """Deletes a template variables entry.

        Args:
            collection (TemplateVariablesCollection): The collection containing the entry.
            template_variables (TemplateVariables): The template variables entry to delete.

        Raises:
            httpx.HTTPStatusError: If the entry doesn't exist, belongs to a different collection,
                or belongs to a different project.

        """
        return run_async(self.adelete_entry)(collection, template_variables)

    async def adelete_entries(
        self,
        collection: TemplateVariablesCollection,
    ) -> None:
        """Async version of delete_entries."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/collections/{collection.id}/entries",
        )
        raise_for_status_with_detail(response)

    def delete_entries(
        self,
        collection: TemplateVariablesCollection,
    ) -> None:
        """Deletes all template variables entries.

        Args:
            collection (TemplateVariablesCollection): The collection to delete entries from.

        Raises:
            httpx.HTTPStatusError: If the collection doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete_entries)(collection)

    async def agenerate_entry(
        self,
        collection: TemplateVariablesCollection,
        prompt_template: PromptTemplate,
    ) -> TemplateVariables:
        """Async version of generate_entry."""
        async with self._semaphore:
            response = await self.async_session.post(
                f"{self.project_route_prefix}/collections/{collection.id}/entries",
                json=CreateTemplateVariablesRequest(
                    input_values=None,
                    prompt_template_id=prompt_template.id,
                ).model_dump(),
            )
            raise_for_status_with_detail(response)
            return TemplateVariables.model_validate(response.json())

    def generate_entry(
        self,
        collection: TemplateVariablesCollection,
        prompt_template: PromptTemplate,
    ) -> TemplateVariables:
        """Generates a new entry in a collection using a prompt template.

        Args:
            collection (TemplateVariablesCollection): The collection to add the generated entry to.
            prompt_template (PromptTemplate): The prompt template to use for generation.

        Returns:
            TemplateVariables: The newly generated template variables object.

        """
        return run_async(self.agenerate_entry)(collection, prompt_template)

    @deprecated(alternative="agenerate_entry")
    async def agenerate_synthetic_entry(
        self,
        collection: TemplateVariablesCollection,
        prompt_template: PromptTemplate,
    ) -> TemplateVariables:
        """Async version of generate_synthetic_entry."""
        return await self.agenerate_entry(collection, prompt_template)

    @deprecated(alternative="generate_entry")
    def generate_synthetic_entry(
        self,
        collection: TemplateVariablesCollection,
        prompt_template: PromptTemplate,
    ) -> TemplateVariables:
        """Generates a new entry in a collection using a prompt template.

        Args:
            collection (TemplateVariablesCollection): The collection to add the generated entry to.
            prompt_template (PromptTemplate): The prompt template to use for generation.

        Returns:
            TemplateVariables: The newly generated template variables object.

        """
        return run_async(self.agenerate_synthetic_entry)(collection, prompt_template)

    async def acreate_experiment(
        self,
        name: str,
        *,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode | None = None,
    ) -> Experiment:
        """Asynchronous version of create_experiment."""
        response = await self.async_session.post(
            f"{self.project_route_prefix}/experiments",
            json={
                "name": name,
                "description": description,
                "prompt_template_id": prompt_template.id,
                "collection_id": collection.id,
                "llm_config_id": llm_config.id if llm_config else None,
                "generate": generate,
                "rating_mode": rating_mode,
            },
        )
        raise_for_status_with_detail(response)
        return Experiment.model_validate(response.json())

    def create_experiment(
        self,
        name: str,
        *,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode | None = None,
    ) -> Experiment:
        """Creates a new experiment.

        Args:
            name (str): The name of the experiment.
            prompt_template (PromptTemplate): The prompt template to use for the experiment.
            collection (TemplateVariablesCollection): The collection of template variables to use for the experiment.
            llm_config (LLMConfig | None): Optional LLMConfig to use for the experiment.
            description (str): Optional description for the experiment.
            generate (bool): Whether to generate responses and ratings immediately. Defaults to False.
            rating_mode (RatingMode | None): The rating mode to use if generating responses. Defaults to None.

        Returns:
            Experiment: The newly created experiment object. If generate=True,
            responses and ratings will be generated. The returned experiment object will
            then include a generation task ID that can be used to check the status of the
            generation.

        Raises:
            httpx.HTTPStatusError: If the experiment with the same name already exists

        """
        return run_async(self.acreate_experiment)(
            name,
            prompt_template=prompt_template,
            collection=collection,
            llm_config=llm_config,
            description=description,
            generate=generate,
            rating_mode=rating_mode,
        )

    async def aget_experiment(self, *, name: str) -> Experiment:
        """Async version of get_experiment."""
        response = await self.async_session.get(
            f"{self.project_route_prefix}/experiments",
            params={"experiment_name": name},
        )
        raise_for_status_with_detail(response)
        experiments = [Experiment.model_validate(e) for e in response.json()["items"]]

        if not experiments:
            raise ValueError(f"No experiment found with name '{name}'")

        # Since experiment names are unique per project, there should be only one if `experiments` is nonempty.
        experiment = experiments[0]

        # Fetch the `experiment` by `id` since this response includes the embedded rated responses
        response = await self.async_session.get(
            f"{self.project_route_prefix}/experiments/{experiment.id}",
        )
        raise_for_status_with_detail(response)
        return Experiment.model_validate(response.json())

    def get_experiment(self, *, name: str) -> Experiment:
        """Get the experiment with the given name.

        Args:
            name (str): The name of the experiment to get.

        Returns:
            Experiment: The experiment object.

        Raises:
            ValueError: If no experiment is found with the given name.

        """
        return run_async(self.aget_experiment)(name=name)

    async def aget_or_create_experiment(
        self,
        name: str,
        *,
        prompt_template: PromptTemplate | None = None,
        collection: TemplateVariablesCollection | None = None,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode | None = None,
    ) -> tuple[Experiment | ExperimentGenerationStatus, bool]:
        """Async version of get_or_create_experiment.

        Returns
        -------
            A tuple of (experiment, created) where created is True if a new experiment
            was created, False if an existing one was retrieved.

        """
        try:
            # Try to get existing experiment first
            experiment = await self.aget_experiment(name=name)
            return experiment, False
        except ValueError:
            # If not found, create new experiment
            logger.info(f"No experiment was found with name {name}. Creating a new experiment.")
            if prompt_template is None:
                raise ValueError("`prompt_template` is required to create a new experiment")
            if collection is None:
                raise ValueError("`collection` is required to create a new experiment")
            experiment = await self.acreate_experiment(
                name,
                prompt_template=prompt_template,
                collection=collection,
                llm_config=llm_config,
                description=description,
                generate=generate,
                rating_mode=rating_mode,
            )
            return experiment, True

    def get_or_create_experiment(
        self,
        name: str,
        *,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode | None = None,
    ) -> tuple[Experiment | ExperimentGenerationStatus, bool]:
        """Gets an existing experiment by name or creates a new one if it doesn't exist.

        The existence of an experiment is determined solely by its name. If an experiment with the given name exists,
        it will be returned regardless of its other properties. If no experiment exists with that name, a new one
        will be created with the provided parameters.

        Args:
            name (str): The name of the experiment to get or create.
            prompt_template (PromptTemplate): The prompt template to use if creating a new experiment.
            collection (TemplateVariablesCollection): The collection of template variables to use if creating a new experiment.
            llm_config (LLMConfig | None): Optional LLMConfig to use if creating a new experiment.
            description (str): Optional description if creating a new experiment.
            generate (bool): Whether to generate responses and ratings immediately. Defaults to False.
            rating_mode (RatingMode | None): The rating mode to use if generating responses. Defaults to None.

        Returns:
            tuple[Experiment | ExperimentGenerationStatus, bool]: A tuple containing:
                - The experiment object (either existing or newly created)
                - Boolean indicating if a new experiment was created (True) or existing one returned (False)

        """
        return run_async(self.aget_or_create_experiment)(
            name,
            prompt_template=prompt_template,
            collection=collection,
            llm_config=llm_config,
            description=description,
            generate=generate,
            rating_mode=rating_mode,
        )

    async def adelete_experiment(
        self,
        experiment: Experiment,
    ) -> None:
        """Async version of delete_experiment."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/experiments/{experiment.id}",
        )
        raise_for_status_with_detail(response)

    def delete_experiment(
        self,
        experiment: Experiment,
    ) -> None:
        """Deletes an experiment.

        Args:
            experiment (Experiment): The experiment to delete.

        Raises:
            httpx.HTTPStatusError: If the experiment doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete_experiment)(experiment)

    @retry_request
    async def arate(
        self,
        prompt_response: PromptResponse,
        *,
        experiment: Experiment | None = None,
        rating_mode: RatingMode = RatingMode.DETAILED,
    ) -> list[Rating]:
        """Async version of rate."""
        async with self._semaphore:
            response = await self.async_session.post(
                f"{self.project_route_prefix}/ratings",
                json=CreateRatingRequest(
                    prompt_response_id=prompt_response.id,
                    experiment_id=experiment.id if experiment else None,
                    rating_mode=rating_mode,
                ).model_dump(),
            )
            raise_for_status_with_detail(response)
            ratings = [Rating.model_validate(rating) for rating in response.json()]

        # Add the rated response to the experiment if one was provided
        if experiment and ratings:
            # Add the ratings to the prompt response
            prompt_response.ratings = ratings
            # Add the prompt response to the experiment's rated responses if not already present
            if prompt_response not in experiment.rated_responses:
                experiment.rated_responses.append(prompt_response)

        return ratings

    def rate(
        self,
        prompt_response: PromptResponse,
        *,
        experiment: Experiment | None = None,
        rating_mode: RatingMode = RatingMode.DETAILED,
    ) -> list[Rating]:
        """Rates a response against its prompt template's criteria using an LLM.

        This method evaluates a prompt response against all applicable criteria associated with its prompt template.
        If template variables were used for the response, it will consider both general criteria and criteria specific
        to those variables.

        Args:
            prompt_response (PromptResponse): The response to rate.
            experiment (Experiment | None): Optional experiment to associate ratings with. If provided,
                the method will verify that the response matches the experiment's prompt template,
                collection, and LLM configuration before rating.
            rating_mode (RatingMode): Mode for rating generation:
                - FAST: Quick evaluation without detailed reasoning
                - DETAILED: Includes explanations for each rating

        Returns:
            list[Rating]: List of rating objects, one per criterion.

        Raises:
            httpx.HTTPStatusError: If no criteria exist for the prompt template

        """
        return run_async(self.arate)(prompt_response, experiment=experiment, rating_mode=rating_mode)

    @retry_request
    async def abatch_rate(
        self,
        batch_prompt_responses: list[PromptResponse],
        *,
        experiment: Experiment | None = None,
        rating_mode: RatingMode = RatingMode.DETAILED,
        timeout: float | None = None,
    ) -> list[list[Rating]]:
        """Async version of batch_rate."""
        # Start with all responses and remove invalid ones
        filtered_prompt_responses = batch_prompt_responses.copy()
        async with self._semaphore:
            response = await self.async_session.post(
                f"{self.project_route_prefix}/ratings/batches",
                json=BatchCreateRatingRequest(
                    prompt_response_ids=[prompt_response.id for prompt_response in filtered_prompt_responses],
                    experiment_id=experiment.id if experiment else None,
                    rating_mode=rating_mode,
                ).model_dump(),
            )
            raise_for_status_with_detail(response)
            task_id = response.json()

        start_time = time.time()
        while timeout is None or time.time() - start_time < timeout:
            # For the status
            response = await self.async_session.get(
                f"{self.project_route_prefix}/ratings/batches/{task_id}",
            )
            raise_for_status_with_detail(response)
            status = BatchCreateRatingResponseStatus.model_validate(response.json())
            if status.status == "FAILURE":
                raise RuntimeError(f"Failed to batch add responses. Status error message: {status.error_msg}")
            elif status.status == "SUCCESS":
                result = status.result
                if result is None:
                    raise RuntimeError("Failed to batch add responses.")
                else:
                    return result

            # Delay before looping again
            await asyncio.sleep(3)
        else:
            raise TimeoutError("Batch add responses timed out.")

    def batch_rate(
        self,
        batch_prompt_responses: list[PromptResponse],
        *,
        experiment: Experiment | None = None,
        rating_mode: RatingMode = RatingMode.DETAILED,
        timeout: float | None = None,
    ) -> list[list[Rating]]:
        """Batch version of rate.

        Args:
            batch_prompt_responses (list[PromptResponse]): List of prompt responses to rate.
            experiment (Experiment | None): Optional experiment to associate ratings with.
            rating_mode (RatingMode): Mode for rating generation (FAST or DETAILED). If DETAILED a reasoning is added to the rating.
            timeout (float): Timeout in seconds for API requests. Defaults to no timeout.

        Returns:
            list[list[Rating]]: List of lists of rating objects, one per criterion for each prompt response.

        """
        return run_async(self.abatch_rate)(
            batch_prompt_responses, experiment=experiment, rating_mode=rating_mode, timeout=timeout
        )

    async def aget_ratings(
        self,
        prompt_response: PromptResponse,
        *,
        only_latest: bool = True,
    ) -> list[Rating]:
        """Async version of get_ratings."""
        params = {
            "prompt_response_id": prompt_response.id,
            "only_latest": only_latest,
        }

        async def fetch_page(params: dict) -> tuple[list[Rating], int]:
            response = await self.async_session.get(
                f"{self.project_route_prefix}/ratings",
                params=params,
            )
            raise_for_status_with_detail(response)
            data = response.json()
            return [Rating.model_validate(rating) for rating in data["items"]], data["count"]

        return await self._apaginate(fetch_page, params, "ratings")

    def get_ratings(
        self,
        prompt_response: PromptResponse,
        *,
        only_latest: bool = True,
    ) -> list[Rating]:
        """Gets the ratings for a prompt response.

        Args:
            prompt_response (PromptResponse): The prompt response to get ratings for.
            only_latest (bool): If True, only returns the most recent rating for each criterion.
                If False, returns all historical ratings. Defaults to True.

        Returns:
            list[Rating]: List of rating objects for the prompt response.

        Raises:
            httpx.HTTPStatusError: If the prompt response doesn't exist or belongs to a different project.

        """
        return run_async(self.aget_ratings)(prompt_response, only_latest=only_latest)

    async def adelete_ratings(
        self,
        prompt_response: PromptResponse,
    ) -> None:
        """Async version of delete_ratings."""
        response = await self.async_session.delete(
            f"{self.project_route_prefix}/ratings",
            params={
                "prompt_response_id": prompt_response.id,
            },
        )
        raise_for_status_with_detail(response)

    def delete_ratings(
        self,
        prompt_response: PromptResponse,
    ) -> None:
        """Deletes all ratings for a prompt response.

        Args:
            prompt_response (PromptResponse): The prompt response to delete ratings for.

        Raises:
            httpx.HTTPStatusError: If the prompt response doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete_ratings)(prompt_response)

    async def acreate_and_run_experiment(
        self,
        name: str,
        *,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        rating_mode: RatingMode = RatingMode.DETAILED,
        timeout: float | None = None,
    ) -> Experiment:
        """Asynchronous version of create_and_run_experiment."""
        # Create experiment with generate flag
        experiment = await self.acreate_experiment(
            name,
            prompt_template=prompt_template,
            collection=collection,
            llm_config=llm_config,
            description=description,
            generate=True,
            rating_mode=rating_mode,
        )

        # Poll for generation status
        start_time = time.time()
        while timeout is None or time.time() - start_time < timeout:
            status = await self.async_session.get(
                f"{self.project_route_prefix}/experiments/{experiment.id}/generation/{experiment.generation_task_id}"
            )
            raise_for_status_with_detail(status)
            status_data = ExperimentGenerationStatus.model_validate(status.json())

            if status_data.status == "FAILURE":
                raise RuntimeError(f"Generation failed: {status_data.error_msg}")

            if status_data.status == "SUCCESS" and status_data.result:
                return status_data.result

            # Delay before polling again
            await asyncio.sleep(3)
        else:
            raise TimeoutError("Experiment generation timed out")

    def create_and_run_experiment(
        self,
        name: str,
        *,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        rating_mode: RatingMode = RatingMode.DETAILED,
        timeout: float | None = None,
    ) -> Experiment:
        """Creates a new experiment and runs it (generates responses and ratings) in one go.

        Args:
            name (str): The name of the experiment.
            prompt_template (PromptTemplate): The prompt template to use for the experiment.
            collection (TemplateVariablesCollection): The collection of template variables to use for the experiment.
            llm_config (LLMConfig | None): Optional LLMConfig to use for the experiment.
            description (str): Optional description for the experiment.
            rating_mode (RatingMode): The rating mode to use for evaluating responses. Defaults to DETAILED.
            timeout (float | None): Optional timeout in seconds. Defaults to None (no timeout).

        Returns:
            ExperimentOut: The experiment with generated responses and ratings.

        Raises:
            RuntimeError: If generation fails or returns no result.
            TimeoutError: If the operation times out.

        """
        return run_async(self.acreate_and_run_experiment)(
            name,
            prompt_template=prompt_template,
            collection=collection,
            llm_config=llm_config,
            description=description,
            rating_mode=rating_mode,
            timeout=timeout,
        )

    async def _apaginate(
        self,
        make_request: Callable[[dict], Awaitable[tuple[list[Any], int]]],
        params: dict,
        resource_name: str,
    ) -> list[Any]:
        """Helper that handles pagination given a request function.

        Args:
            make_request: Async function that takes params and returns (items, total_count)
            params: Query parameters for the request
            resource_name: Name of the resource being fetched (e.g. "responses", "entries")

        Returns:
            list[Any]: Combined list of all items across all pages

        """
        all_items = []
        page = 1

        # Get first page and total count
        items, total_count = await self.fetch_page_with_semaphore(page, make_request, params)
        all_items.extend(items)

        # Calculate remaining pages (100 items per page)
        total_pages = math.ceil(total_count / 100)  # Round up division

        # Fetch remaining pages if any
        # Only show progress for operations with more than 10 pages
        should_show_progress = total_pages > 10
        page_range = (
            tqdm(range(2, total_pages + 1), desc=f"Getting {resource_name}")
            if should_show_progress
            else range(2, total_pages + 1)
        )

        for page in page_range:
            items, _ = await self.fetch_page_with_semaphore(page, make_request, params)
            all_items.extend(items)

        return all_items

    async def fetch_page_with_semaphore(
        self, page_num: int, make_request: Callable[[dict], Awaitable[tuple[list[Any], int]]], params: dict
    ) -> tuple[list[Any], int]:
        """Helper that handles pagination given a request function.
        Semaphore is used per-request rather than around the entire pagination
        to allow other operations to run between page fetches and to release
        the semaphore while processing results

        Args:
            page_num: The page number to fetch
            make_request: Async function that takes params and returns (items, total_count)
            params: Query parameters for the request

        """
        async with self._semaphore:
            return await make_request({**params, "page": page_num})

    # Resource management methods
    async def _aclose(self) -> None:
        """Safely close the async client."""
        try:
            await self.async_session.aclose()
        except Exception:
            pass

    def _cleanup(self) -> None:
        """Clean up resources."""
        try:
            # Create a new event loop for cleanup if necessary
            try:
                loop = asyncio.get_event_loop()
                if loop.is_closed():
                    raise RuntimeError("Event loop is closed")
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
            loop.run_until_complete(self._aclose())
        except Exception:
            pass
        finally:
            atexit.unregister(self._cleanup)

    async def __aenter__(self) -> "Client":
        return self

    async def __aexit__(
        self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any
    ) -> None:
        await self._aclose()

    def __enter__(self) -> "Client":
        return self

    def __exit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        self._cleanup()
