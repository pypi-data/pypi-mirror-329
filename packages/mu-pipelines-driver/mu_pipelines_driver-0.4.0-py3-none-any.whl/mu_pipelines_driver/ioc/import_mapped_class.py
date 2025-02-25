from importlib import import_module
from typing import NotRequired, Type, TypedDict, TypeVar

TClass = TypeVar("TClass")


class ClassModuleMappingItem(TypedDict):
    module_path: str
    class_name: str
    intialize_context_module: NotRequired[str]


def import_mapped_class(
    mapping: ClassModuleMappingItem, ClassType: Type[TClass]
) -> Type[TClass]:
    module_cls: Type[TClass] = getattr(
        import_module(mapping["module_path"]), mapping["class_name"]
    )
    return module_cls
