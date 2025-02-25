from importlib import import_module
from typing import TypeVar

TFuncType = TypeVar("TFuncType")


def import_function(
    module_path: str, function_name: str, function_type: TFuncType
) -> TFuncType:
    return getattr(import_module(module_path), function_name)
