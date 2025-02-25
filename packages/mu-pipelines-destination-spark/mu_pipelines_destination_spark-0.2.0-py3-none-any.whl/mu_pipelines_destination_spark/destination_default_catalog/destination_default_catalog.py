from typing import TypedDict, cast

from mu_pipelines_interfaces.config_types.destination_config import DestinationConfig
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider
from mu_pipelines_interfaces.destination_module_interface import (
    DestinationModuleInterface,
)
from pyspark.sql import DataFrame, DataFrameWriter

from mu_pipelines_destination_spark.context.spark_context import MUPipelinesSparkContext


class AdditionalAttribute(TypedDict):
    key: str
    value: str


class DestinationDefaultCatalogConfig(TypedDict):
    table_name: str
    mode: str
    additional_attributes: list[AdditionalAttribute]


class DestinationDefaultCatalog(DestinationModuleInterface):
    def __init__(
        self, config: DestinationConfig, configuration_provider: ConfigurationProvider
    ):
        super().__init__(config, configuration_provider)
        """
        TODO need to determine how to validate the config
        """
        destination_config: DestinationDefaultCatalogConfig = cast(
            DestinationDefaultCatalogConfig, self._config
        )
        assert "table_name" in destination_config
        assert (
            len(destination_config["table_name"]) > 0
        )  # whatever makes sense to validate for table name
        assert "mode" in destination_config

    def save(self, df: DataFrame, context: MUPipelinesSparkContext) -> None:
        destination_config: DestinationDefaultCatalogConfig = cast(
            DestinationDefaultCatalogConfig, self._config
        )

        writer: DataFrameWriter = df.write

        writer = writer.mode(destination_config["mode"])

        if "additional_attributes" in destination_config:
            for additional_attribute in destination_config["additional_attributes"]:
                writer = writer.option(
                    additional_attribute["key"], additional_attribute["value"]
                )

        writer.saveAsTable(destination_config["table_name"])


# https://spark.apache.org/docs/3.5.3/sql-data-sources-load-save-functions.html#saving-to-persistent-tables

# "destination": [
#     {
#         "type": "DestinationDefaultCatalog",
#         "_table_name": "The name of the table. ex: landing.people",
#         "table_name": "people",
#         "_mode": "overwrite | append | ignore"
#         "mode": "overwrite",
#         "_additional_attributes": "optional argument to pass extra properties",
#         "additional_attributes": [
#             {
#                 "key": "key1",
#                 "value": "value1"
#             },
#             {
#                 "key": "key2",
#                 "value": "value2"
#             }
#         ]
#     }
# ]
