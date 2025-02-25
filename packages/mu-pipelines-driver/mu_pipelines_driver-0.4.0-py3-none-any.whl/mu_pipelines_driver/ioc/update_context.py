from importlib import import_module
from typing import Callable, TypeVar

from mu_pipelines_driver.ioc.import_mapped_class import ClassModuleMappingItem

TFuncType = TypeVar("TFuncType")


def import_function(
    module_path: str, function_name: str, function_type: TFuncType
) -> TFuncType:
    return getattr(import_module(module_path), function_name)


def update_context(mapping: ClassModuleMappingItem, existing_context: dict) -> None:
    if "intialize_context_module" in mapping:
        import_function(
            mapping["intialize_context_module"],
            "initialize_context",
            Callable[[dict], None],
        )(
            existing_context
        )  # type: ignore
