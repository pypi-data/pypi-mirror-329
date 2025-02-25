from typing import Any
from typing import ClassVar

from amsdal_models.builder.validators.dict_validators import validate_non_empty_keys
from amsdal_models.classes.model import TypeModel
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field
from pydantic.functional_validators import field_validator


class ClassProperty(TypeModel):
    __module_type__: ClassVar[ModuleType] = ModuleType.CORE
    type: str = Field(title='Type')
    items: dict[str, Any | None] | None = Field(None, title='Items')

    @field_validator('items')
    @classmethod
    def _non_empty_keys_items(cls: type, value: Any) -> Any:  # type: ignore # noqa: A003
        return validate_non_empty_keys(value)
