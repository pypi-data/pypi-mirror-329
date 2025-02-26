from amsdal.models.core.option import *
from amsdal_models.classes.model import TypeModel
from amsdal_utils.models.enums import ModuleType
from typing import Any, ClassVar

class ClassPropertyMeta(TypeModel):
    __module_type__: ClassVar[ModuleType]
    title: str | None
    default: Any | None
    options: list['Option'] | None
