from typing import TypedDict, cast

from deprecation import deprecated
from mu_pipelines_interfaces.config_types.destination_config import DestinationConfig
from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider
from mu_pipelines_interfaces.destination_module_interface import (
    DestinationModuleInterface,
)
from pyspark.sql import DataFrame, DataFrameWriter

from mu_pipelines_destination_spark import __version__
from mu_pipelines_destination_spark.context.spark_context import MUPipelinesSparkContext


class AdditionalAttribute(TypedDict):
    key: str
    value: str


class SaveToCSVConfig(TypedDict):
    file_location: str
    delimiter: str
    quotes: str
    additional_attributes: list[AdditionalAttribute]


class SaveToCSV(DestinationModuleInterface):
    @deprecated(
        removed_in="1.0.0",
        deprecated_in="0.2.0",
        current_version=__version__,
        details="Use DestinationCSV",
    )
    def __init__(
        self, config: DestinationConfig, configuration_provider: ConfigurationProvider
    ):
        super().__init__(config, configuration_provider)
        """
        TODO need to determine how to validate the config
        """
        save_csv_config: SaveToCSVConfig = cast(SaveToCSVConfig, self._config)
        assert "file_location" in save_csv_config
        assert (
            len(save_csv_config["file_location"]) > 0
        )  # whatever makes sense to validate for path
        # TODO should all csv config be required?

    def save(self, df: DataFrame, context: MUPipelinesSparkContext) -> None:
        save_csv_config: SaveToCSVConfig = cast(SaveToCSVConfig, self._config)

        writer: DataFrameWriter = df.write

        if "delimiter" in save_csv_config:
            writer = writer.option("delimiter", save_csv_config["delimiter"])

        if "quotes" in save_csv_config:
            writer = writer.option("quote", save_csv_config["quotes"])

        if "additional_attributes" in save_csv_config:
            for additional_attribute in save_csv_config["additional_attributes"]:
                writer = writer.option(
                    additional_attribute["key"], additional_attribute["value"]
                )

        writer.csv(save_csv_config["file_location"])


# https://spark.apache.org/docs/latest/sql-data-sources-csv.html#csv-files

# "execution": [
#     {
#         "type": "csv",
#         "_file_location": "This can be a URL or accessible location",
#         "file_location": "",
#         "delimiter": ",",
#         "quotes": "escape_all",
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
