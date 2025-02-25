from mu_pipelines_configuration_provider.diy_configuration_provider import (
    DIYConfigurationProvider,
)
from mu_pipelines_interfaces.config_types.connection_properties import (
    ConnectionProperties,
)
from mu_pipelines_interfaces.config_types.global_properties.global_properties import (
    GlobalProperties,
)
from mu_pipelines_interfaces.config_types.job_config import JobConfigItem
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider

from mu_pipelines_driver.ioc.ioc_container import IOCContainer
from mu_pipelines_driver.job_driver import job_driver


def run_config_from_provider(config_provider: ConfigurationProvider) -> object | None:
    last_df: object | None = None
    for job_item in config_provider.job_config:
        ioc_container = IOCContainer(job_item, config_provider)

        last_df = job_driver(ioc_container)

    return last_df


def run_config(
    job_config: list[JobConfigItem],
    global_properties: GlobalProperties,
    connection_config: ConnectionProperties,
) -> object | None:
    config_provider: ConfigurationProvider = DIYConfigurationProvider(
        job_config, global_properties, connection_config
    )
    return run_config_from_provider(config_provider)
