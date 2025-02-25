from typing import List, Tuple

from elluminate.beta.resources.base import BaseResource
from elluminate.beta.schemas import (
    Criterion,
    PromptTemplate,
)
from elluminate.beta.schemas.criterion import CreateCriteriaRequest
from elluminate.utils import retry_request, run_async


class CriteriaResource(BaseResource):
    async def alist(
        self,
        prompt_template: PromptTemplate,
    ) -> List[Criterion]:
        """Async version of list."""
        params = {"prompt_template_id": prompt_template.id}
        return await self._paginate(
            path="criteria",
            model=Criterion,
            params=params,
            resource_name="Criteria",
        )

    def list(
        self,
        prompt_template: PromptTemplate,
    ) -> List[Criterion]:
        """Get the evaluation criteria for a prompt template.

        This method retrieves all criteria associated with the prompt template. If template
        variables are provided, only criteria specific to those variables will be returned.

        Args:
            prompt_template (PromptTemplate): The prompt template to get criteria for.

        Returns:
            list[Criterion]: List of criterion objects, ordered by creation date.

        """
        return run_async(self.alist)(prompt_template)

    @retry_request
    async def aadd_many(
        self,
        criteria: List[str],
        prompt_template: PromptTemplate,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> List[Criterion]:
        """Async version of add."""
        request_data = CreateCriteriaRequest(
            prompt_template_id=prompt_template.id,
            criteria=criteria,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )
        response = await self._apost("criteria", json=request_data.model_dump())
        return [Criterion.model_validate(criterion) for criterion in response.json()]

    def add_many(
        self,
        criteria: List[str],
        prompt_template: PromptTemplate,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> List[Criterion]:
        """Adds custom evaluation criteria to the prompt template.

        If criteria with the same strings already exist for this prompt template, they will be reused rather than duplicated.

        Args:
            criteria (list[str]): List of criterion strings to add.
            prompt_template (PromptTemplate): The prompt template to add criteria to.
            criterion_set (str | None): Optional name to group related criteria together. If not provided, a default name is used.
            delete_existing (bool): If True, deletes any existing criteria for this prompt template
                before adding the new ones. Defaults to False.

        Returns:
            list[Criterion]: List of created and/or existing criterion objects.

        Raises:
            httpx.HTTPStatusError: If the prompt template doesn't belong to the project,
                or other API errors occur.

        """
        return run_async(self.aadd_many)(
            criteria=criteria,
            prompt_template=prompt_template,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )

    @retry_request
    async def agenerate_many(
        self,
        prompt_template: PromptTemplate,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> List[Criterion]:
        """Async version of generate."""
        request_data = CreateCriteriaRequest(
            prompt_template_id=prompt_template.id,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )
        response = await self._apost("criteria", json=request_data.model_dump())
        return [Criterion.model_validate(criterion) for criterion in response.json()]

    def generate_many(
        self,
        prompt_template: PromptTemplate,
        criterion_set: str | None = None,
        delete_existing: bool = False,
    ) -> List[Criterion]:
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
        return run_async(self.agenerate_many)(
            prompt_template=prompt_template,
            criterion_set=criterion_set,
            delete_existing=delete_existing,
        )

    async def aget_or_generate_many(
        self,
        prompt_template: PromptTemplate,
        criterion_set: str | None = None,
    ) -> Tuple[List[Criterion], bool]:
        """Async version of get_or_generate_criteria."""
        # TODO: This can cause a race condition when multiple consumers
        # calls this functions at the same time. The solution is to switch the order
        # of alist and agenerate_many. However, the backend raises a 400 error when
        # agenerate_many is called with delete_existing=False and criteria already exist.
        # This is also happenen in other cases, so we need to adjust the backend, before doing this.
        criteria = await self.alist(
            prompt_template,
        )
        if criteria:
            return criteria, False

        return await self.agenerate_many(
            prompt_template,
            criterion_set=criterion_set,
        ), True

    def get_or_generate_many(
        self,
        prompt_template: PromptTemplate,
        criterion_set: str | None = None,
    ) -> Tuple[List[Criterion], bool]:
        """Gets existing criteria or generates new ones if none exist.

        This method generates new criteria if none exist, otherwise it returns the existing criteria.

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
        return run_async(self.aget_or_generate_many)(
            prompt_template,
            criterion_set=criterion_set,
        )

    async def adelete(self, criterion: Criterion) -> None:
        """Async version of delete."""
        await self._adelete(f"criteria/{criterion.id}")

    def delete(self, criterion: Criterion) -> None:
        """Delete a criterion.

        Args:
            criterion (Criterion): The criterion to delete.

        """
        return run_async(self.adelete)(criterion)

    async def adelete_all(
        self,
        prompt_template: PromptTemplate,
    ) -> None:
        """Async version of delete_all."""
        params = {"prompt_template_id": prompt_template.id}
        await self._adelete("criteria", params=params)

    def delete_all(
        self,
        prompt_template: PromptTemplate,
    ) -> None:
        """Delete the all criteria associated with the prompt template.

        This method deletes all criteria associated with the given prompt template. If template
        variables are provided, only criteria specific to those variables will be deleted.

        Args:
            prompt_template (PromptTemplate): The prompt template to delete criteria for.

        Raises:
            httpx.HTTPStatusError: If the prompt template or the template variables don't exist.

        """
        return run_async(self.adelete_all)(prompt_template)
