from typing import Any
from typing import ClassVar

from amsdal_models.classes.model import TypeModel
from amsdal_utils.models.enums import ModuleType
from pydantic.fields import Field

from amsdal.models.core.option import *  # noqa: F403


class ClassPropertyMeta(TypeModel):
    __module_type__: ClassVar[ModuleType] = ModuleType.CORE
    title: str | None = Field(None, title='Title')
    default: Any | None = Field(None, title='Default')
    options: list['Option'] | None = Field(None, title='Options')  # noqa: F405
