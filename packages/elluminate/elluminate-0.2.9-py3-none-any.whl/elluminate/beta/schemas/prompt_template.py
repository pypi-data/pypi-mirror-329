from __future__ import annotations

import re
from datetime import datetime
from typing import ClassVar

from pydantic import BaseModel

from elluminate.beta.schemas.template_variables_collection import TemplateVariablesCollection


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


class CreatePromptTemplateRequest(BaseModel):
    """Request to create a new prompt template."""

    name: str | None = None
    user_prompt_template_str: str
    parent_prompt_template_id: int | None = None
    default_collection_id: int | None = None
