from mu_pipelines_interfaces.config_types.connection_properties import (
    ConnectionConfig,
    ConnectionProperties,
)
from mu_pipelines_interfaces.config_types.job_config import DestinationConfig
from mu_pipelines_interfaces.configuration_provider import GlobalProperties

from mu_pipelines_driver.ioc.import_mapped_class import ClassModuleMappingItem


class DestinationModuleMappingItem(ClassModuleMappingItem):
    type: str


DESTINATION_MODULE_MAPPING: list[DestinationModuleMappingItem] = [
    {
        "type": "jdbc-postgres-mock",
        "module_path": "test.mock.save_to_table.save_to_table",
        "class_name": "SaveToTable",
    },
    {
        "type": "jdbc-postgres-spark",
        "module_path": "mu_pipelines_destination_spark.save_to_table.save_to_table",
        "class_name": "SaveToTable",
    },
    {
        "type": "csv-spark",
        "module_path": "mu_pipelines_destination_spark.save_to_csv.save_to_csv",
        "class_name": "SaveToCSV",
        "intialize_context_module": "mu_pipelines_destination_spark.context",
    },
    {
        "type": "print-spark",
        "module_path": "mu_pipelines_destination_spark.print.print",
        "class_name": "PrintDestination",
    },
    {
        "type": "table-spark",
        "module_path": "mu_pipelines_destination_spark.save_to_table.save_to_table",
        "class_name": "SaveToTable",
        "intialize_context_module": "mu_pipelines_destination_spark.context",
    },
    {
        "type": "destinationcsv-spark",
        "module_path": "mu_pipelines_destination_spark.destination_csv.destination_csv",
        "class_name": "DestinationCSV",
        "intialize_context_module": "mu_pipelines_destination_spark.context",
    },
    {
        "type": "destinationdefaultcatalog-spark",
        "module_path": "mu_pipelines_destination_spark.destination_default_catalog.destination_default_catalog",
        "class_name": "DestinationDefaultCatalog",
        "intialize_context_module": "mu_pipelines_destination_spark.context",
    },
]


def find_destination_module_mapping(
    dest_config: DestinationConfig,
    global_properties: GlobalProperties,
    connection_properties: ConnectionProperties,
) -> DestinationModuleMappingItem | None:
    temp_type: str = dest_config["type"]

    # When the destination depends on a connection_config in connection_properties
    # TODO determine whether this is needed in the mapping
    if "connection_details" in dest_config:
        connection_config: ConnectionConfig = next(
            CONN
            for CONN in connection_properties["connections"]
            if CONN["name"] == dest_config["connection_details"]
        )
        connection_config_type: str = connection_config["type"]
        temp_type = "{temp_type}-{connection_config_type}".format(
            temp_type=temp_type, connection_config_type=connection_config_type
        )

    mapping_type: str = "{type}-{library_type}".format(
        type=temp_type, library_type=global_properties["library"]
    )

    return next(
        (
            MAPPING
            for MAPPING in DESTINATION_MODULE_MAPPING
            if MAPPING["type"] == mapping_type.lower()
        ),
        None,
    )
