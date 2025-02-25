from typing import Type

from mu_pipelines_interfaces.config_types.job_config import JobConfigItem
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider
from mu_pipelines_interfaces.destination_module_interface import (
    DestinationModuleInterface,
)
from mu_pipelines_interfaces.execute_module_interface import ExecuteModuleInterface

from mu_pipelines_driver.ioc.destination_module_mapping import (
    DestinationModuleMappingItem,
    find_destination_module_mapping,
)
from mu_pipelines_driver.ioc.execute_module_mapping import (
    ExecuteModuleMappingItem,
    find_execute_module_mapping,
)
from mu_pipelines_driver.ioc.import_mapped_class import import_mapped_class
from mu_pipelines_driver.ioc.update_context import update_context


class IOCContainer:
    _job_config: JobConfigItem
    _config_provider: ConfigurationProvider
    _context: dict

    def __init__(
        self, job_config: JobConfigItem, config_provider: ConfigurationProvider
    ):
        self._job_config = job_config
        self._config_provider = config_provider
        self._context = {}

    @property
    def context(self) -> dict:
        return self._context

    @property
    def execute_modules(self) -> list[ExecuteModuleInterface]:
        constructed_modules: list[ExecuteModuleInterface] = []
        for exec_config in self._job_config["execution"]:
            mapping: ExecuteModuleMappingItem | None = find_execute_module_mapping(
                exec_config, self._config_provider.global_properties
            )
            if mapping is not None:
                module_cls: Type[ExecuteModuleInterface] = import_mapped_class(
                    mapping, ExecuteModuleInterface
                )
                constructed_modules.append(
                    module_cls(
                        config=exec_config, configuration_provider=self._config_provider
                    )
                )
                update_context(mapping, self._context)
            else:
                raise NotImplementedError("execute_module not mapped", exec_config)
        return constructed_modules

    @property
    def destination_modules(self) -> list[DestinationModuleInterface]:
        constructed_modules: list[DestinationModuleInterface] = []
        for dest_config in self._job_config["destination"]:
            mapping: DestinationModuleMappingItem | None = (
                find_destination_module_mapping(
                    dest_config,
                    self._config_provider.global_properties,
                    self._config_provider.connection_config,
                )
            )
            if mapping is not None:
                module_cls: Type[DestinationModuleInterface] = import_mapped_class(
                    mapping, DestinationModuleInterface
                )
                constructed_modules.append(
                    module_cls(
                        config=dest_config, configuration_provider=self._config_provider
                    )
                )
                update_context(mapping, self._context)
            else:
                raise NotImplementedError("destination_module not mapped", dest_config)
        return constructed_modules
