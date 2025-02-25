from mu_pipelines_interfaces.config_types.execute_config import ExecuteConfig
from mu_pipelines_interfaces.config_types.global_properties.global_properties import (
    GlobalProperties,
)

from mu_pipelines_driver.ioc.import_mapped_class import ClassModuleMappingItem


class ExecuteModuleMappingItem(ClassModuleMappingItem):
    type: str


EXECUTE_MODULE_MAPPING: list[ExecuteModuleMappingItem] = [
    {
        "type": "csvreadcommand-mock",
        "module_path": "test.mock.load_csv.load_csv",
        "class_name": "LoadCSV",
    },
    {
        "type": "csvreadcommand-spark",
        "module_path": "mu_pipelines_execute_spark.load_csv.load_csv",
        "class_name": "LoadCSV",
        "intialize_context_module": "mu_pipelines_execute_spark.context",
    },
    {
        "type": "ingestcsv-spark",
        "module_path": "mu_pipelines_execute_spark.ingest_csv.ingest_csv",
        "class_name": "IngestCSV",
        "intialize_context_module": "mu_pipelines_execute_spark.context",
    },
]


def find_execute_module_mapping(
    exec_config: ExecuteConfig, global_properties: GlobalProperties
) -> ExecuteModuleMappingItem | None:
    mapping_type: str = "{execute_type}-{library_type}".format(
        execute_type=exec_config["type"], library_type=global_properties["library"]
    )
    return next(
        (
            MAPPING
            for MAPPING in EXECUTE_MODULE_MAPPING
            if MAPPING["type"] == mapping_type.lower()
        ),
        None,
    )
