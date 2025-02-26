from typing import Any
from typing import ClassVar
from typing import Optional

from amsdal_models.builder.validators.dict_validators import validate_non_empty_keys
from amsdal_models.classes.model import Model
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field
from pydantic.functional_validators import field_validator

from amsdal.models.core.class_property_meta import *  # noqa: F403


class ClassObjectMeta(Model):
    __module_type__: ClassVar[ModuleType] = ModuleType.CORE
    title: str = Field(title='Title')
    type: str = Field(title='Type')
    default: Any | None = Field(None, title='Default')
    class_schema_type: str | None = Field(None, title='Schema Type')
    properties: dict[str, Optional['ClassPropertyMeta']] | None = Field(None, title='Properties')  # noqa: F405
    custom_code: str | None = Field(None, title='Custom Code')

    @field_validator('properties')
    @classmethod
    def _non_empty_keys_properties(cls: type, value: Any) -> Any:  # type: ignore # noqa: A003
        return validate_non_empty_keys(value)
