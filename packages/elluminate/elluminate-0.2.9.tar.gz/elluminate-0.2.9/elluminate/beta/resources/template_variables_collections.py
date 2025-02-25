from typing import Tuple

import httpx
from loguru import logger

from elluminate.beta.resources.base import BaseResource
from elluminate.beta.schemas import (
    CreateCollectionRequest,
    TemplateVariablesCollection,
)
from elluminate.utils import run_async


class TemplateVariablesCollectionsResource(BaseResource):
    async def aget(
        self,
        name: str,
    ) -> TemplateVariablesCollection:
        """Async version of get_collection."""
        response = await self._aget("collections", params={"name": name})
        collections = [TemplateVariablesCollection.model_validate(c) for c in response.json()["items"]]

        if not collections:
            raise ValueError(f"No collection found with name '{name}'")
        return collections[0]

    def get(
        self,
        *,
        name: str,
    ) -> TemplateVariablesCollection:
        """Get a collection by name.

        Args:
            name (str): The name of the collection to get.

        Returns:
            TemplateVariablesCollection: The collection object.

        Raises:
            ValueError: If no collection is found with the given name.

        """
        return run_async(self.aget)(name=name)

    async def acreate(self, name: str | None = None, description: str = "") -> TemplateVariablesCollection:
        """Async version of create_collection."""
        response = await self._apost(
            "collections", json=CreateCollectionRequest(name=name, description=description).model_dump()
        )
        return TemplateVariablesCollection.model_validate(response.json())

    def create(self, name: str, description: str = "") -> TemplateVariablesCollection:
        """Creates a new collection.

        Args:
            name (str): The name for the new collection.
            description (str): Optional description for the collection.

        Returns:
            (TemplateVariablesCollection): The newly created collection object.

        Raises:
            httpx.HTTPStatusError: If collection with same name already exists (400 BAD REQUEST)

        """
        return run_async(self.acreate)(name=name, description=description)

    async def aget_or_create(self, name: str, description: str = "") -> Tuple[TemplateVariablesCollection, bool]:
        """Async version of get_or_create_collection."""
        try:
            return await self.acreate(name=name, description=description), True
        except httpx.HTTPStatusError as e:
            # Code 409 means resource already exists, simply get and return it
            if e.response.status_code == 409:
                collection = await self.aget(name=name)
                if description != "" and collection.description != description:
                    logger.warning(
                        f"Collection with name {name} already exists with a different description (expected: {description}, actual: {collection.description}), returning existing collection."
                    )
                return collection, False
            raise  # Re-raise any other HTTP status errors s

    def get_or_create(self, name: str, description: str = "") -> tuple[TemplateVariablesCollection, bool]:
        """Gets an existing collection by name or creates a new one if it doesn't exist.
        The existence check is only based on the name parameter - if a collection with
        the given name exists, it will be returned regardless of the other parameters.

        Args:
            name: The name of the collection to get or create.
            description: Optional description for the collection if created.

        Returns:
            tuple[TemplateVariablesCollection, bool]: A tuple containing:
                - Collection: The retrieved or created collection object
                - bool: True if a new collection was created, False if existing was found

        """
        return run_async(self.aget_or_create)(name=name, description=description)

    async def adelete(self, template_variables_collection: TemplateVariablesCollection) -> None:
        await self._adelete(f"collections/{template_variables_collection.id}")

    def delete(self, template_variables_collection: TemplateVariablesCollection) -> None:
        return run_async(self.adelete)(template_variables_collection)
