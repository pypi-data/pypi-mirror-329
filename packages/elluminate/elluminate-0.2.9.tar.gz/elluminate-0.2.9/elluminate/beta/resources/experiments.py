import asyncio
import time

from loguru import logger
from pydantic import BaseModel

from elluminate.beta.resources.base import BaseResource
from elluminate.beta.schemas import (
    CreateExperimentRequest,
    Experiment,
    ExperimentGenerationStatus,
    LLMConfig,
    PromptTemplate,
    RatingMode,
    TemplateVariablesCollection,
)
from elluminate.utils import run_async


class ExperimentsResource(BaseResource):
    async def aget(self, name: str) -> Experiment:
        """Async version of get."""
        response = await self._aget("experiments", params={"experiment_name": name})
        experiments = [Experiment.model_validate(e) for e in response.json()["items"]]

        if not experiments:
            raise ValueError(f"No experiment found with name '{name}'")

        # Since experiment names are unique per project, there should be only one if `experiments` is nonempty.
        experiment = experiments[0]

        # Fetch the `experiment` by `id` since this response includes the embedded rated responses
        response = await self._aget(f"experiments/{experiment.id}")
        experiment = Experiment.model_validate(response.json())

        return experiment

    def get(self, name: str) -> Experiment:
        """Get the experiment with the given name.

        Args:
            name (str): The name of the experiment to get.

        Returns:
            Experiment: The experiment object.

        Raises:
            ValueError: If no experiment is found with the given name.

        """
        return run_async(self.aget)(name)

    async def acreate(
        self,
        name: str,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode = RatingMode.DETAILED,
    ) -> Experiment:
        """Async version of create."""
        response = await self._apost(
            "experiments",
            json=CreateExperimentRequest(
                name=name,
                description=description,
                prompt_template_id=prompt_template.id,
                collection_id=collection.id,
                llm_config_id=llm_config.id if llm_config else None,
                generate=generate,
                rating_mode=rating_mode,
            ).model_dump(),
        )
        return Experiment.model_validate(response.json())

    def create(
        self,
        name: str,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode = RatingMode.DETAILED,
    ) -> Experiment:
        """Creates a new experiment.

        Args:
            name (str): The name of the experiment.
            prompt_template (PromptTemplate): The prompt template to use for the experiment.
            collection (TemplateVariablesCollection): The collection of template variables to use for the experiment.
            llm_config (LLMConfig | None): Optional LLMConfig to use for the experiment. Uses platform default if not specified.
            description (str): Optional description for the experiment.
            generate (bool): Whether to generate responses and ratings immediately. Defaults to False.
            rating_mode (RatingMode): The rating mode to use if generating responses (Only used if generate=True). Defaults to RatingMode.DETAILED.

        Returns:
            Experiment: The newly created experiment object. If generate=True,
            responses and ratings will be generated. The returned experiment object will
            then include a generation task ID that can be used to check the status of the
            generation.

        Raises:
            httpx.HTTPStatusError: If the experiment with the same name already exists

        """
        return run_async(self.acreate)(
            name=name,
            prompt_template=prompt_template,
            collection=collection,
            llm_config=llm_config,
            description=description,
            generate=generate,
            rating_mode=rating_mode,
        )

    async def aget_or_create(
        self,
        name: str,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode = RatingMode.DETAILED,
    ) -> tuple[Experiment, bool]:
        """Async version of get_or_create."""
        # Create a dict of the requested parameters (excluding None values)
        # TODO: Change the order to avoid race condition if the backend returns a 409 instead of
        # a 400 if an experiment already exists
        requested_dict = {
            k: v
            for k, v in {
                "name": name,
                "prompt_template": prompt_template,
                "collection": collection,
                "llm_config": llm_config,
                "description": description,
                "generate": generate,
                "rating_mode": rating_mode,
            }.items()
            if v is not None
        }

        try:
            # Try to get existing experiment first
            existing_config = await self.aget(name=name)
            existing_dict = existing_config.model_dump()

            differences = []
            for k, v in requested_dict.items():
                if isinstance(v, BaseModel):
                    v = v.model_dump()

                if k not in {"name"} and k in existing_dict and v != existing_dict[k]:
                    differences.append(k)

            if differences:
                logger.warning(
                    f"Experiment with name '{name}' already exists with different values for: {', '.join(differences)}. Returning existing experiment."
                )

            return existing_config, False

        except ValueError:
            experiment = await self.acreate(
                name,
                prompt_template=prompt_template,
                collection=collection,
                llm_config=llm_config,
                description=description,
                generate=generate,
                rating_mode=rating_mode,
            )
            return experiment, True

    def get_or_create(
        self,
        name: str,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        generate: bool = False,
        rating_mode: RatingMode = RatingMode.DETAILED,
    ) -> tuple[Experiment, bool]:
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
            rating_mode (RatingMode): The rating mode to use if generating responses. Defaults to RatingMode.DETAILED.

        Returns:
            tuple[Experiment | ExperimentGenerationStatus, bool]: A tuple containing:
                - The experiment object (either existing or newly created)
                - Boolean indicating if a new experiment was created (True) or existing one returned (False)

        """
        return run_async(self.aget_or_create)(
            name=name,
            prompt_template=prompt_template,
            collection=collection,
            llm_config=llm_config,
            description=description,
            generate=generate,
            rating_mode=rating_mode,
        )

    async def acreate_and_run(
        self,
        name: str,
        prompt_template: PromptTemplate,
        collection: TemplateVariablesCollection,
        llm_config: LLMConfig | None = None,
        description: str = "",
        rating_mode: RatingMode = RatingMode.DETAILED,
        timeout: float | None = None,
    ) -> Experiment:
        """Asynchronous version of create_and_run_experiment."""
        # Create experiment with generate flag
        experiment = await self.acreate(
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
            status = await self._aget(f"experiments/{experiment.id}/generation/{experiment.generation_task_id}")
            status_data = ExperimentGenerationStatus.model_validate(status.json())

            if status_data.status == "FAILURE":
                raise RuntimeError(f"Generation failed: {status_data.error_msg}")

            if status_data.status == "SUCCESS" and status_data.result:
                return status_data.result

            # Delay before polling again
            await asyncio.sleep(3)
        else:
            raise TimeoutError("Experiment generation timed out")

    def create_and_run(
        self,
        name: str,
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
        return run_async(self.acreate_and_run)(
            name=name,
            prompt_template=prompt_template,
            collection=collection,
            llm_config=llm_config,
            description=description,
            rating_mode=rating_mode,
            timeout=timeout,
        )

    async def adelete(self, experiment: Experiment) -> None:
        """Async version of delete."""
        await self._adelete(f"experiments/{experiment.id}")

    def delete(self, experiment: Experiment) -> None:
        """Deletes an experiment.

        Args:
            experiment (Experiment): The experiment to delete.

        Raises:
            httpx.HTTPStatusError: If the experiment doesn't exist or belongs to a different project.

        """
        return run_async(self.adelete)(experiment)
