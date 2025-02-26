from typing import Any
from typing import ClassVar
from typing import Optional

from amsdal_models.builder.validators.dict_validators import validate_non_empty_keys
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field
from pydantic.functional_validators import field_validator

from amsdal.models.core.class_property import *  # noqa: F403


class ClassObject(Model):
    __module_type__: ClassVar[ModuleType] = ModuleType.CORE
    properties: Optional[dict[str, Optional['ClassProperty']]] = Field(None, title='Properties')  # noqa: F405, UP007
    table_name: Optional[str] = Field(None, title='Table name')  # noqa: UP007
    primary_key: Optional[dict[str, list[str]]] = Field(None, title='Primary key fields')  # noqa: UP007
    indexed: Optional[list[str]] = Field(None, title='Indexed')  # noqa: UP007
    unique: Optional[list[list[str]]] = Field(None, title='Unique Fields')  # noqa: UP007
    required: Optional[list[str]] = Field(None, title='Required')  # noqa: UP007
    meta_class: Optional[str] = Field('ClassObject', title='Meta Class')  # noqa: UP007

    @field_validator('properties')
    @classmethod
    def _non_empty_keys_properties(cls: type, value: Any) -> Any:
        return validate_non_empty_keys(value)

    @property
    def display_name(self) -> str:
        """
        Returns the display name of the object.

        Returns:
            str: The display name, which is the title of the object.
        """
        return self.title
