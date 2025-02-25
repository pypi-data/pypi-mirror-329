from mu_pipelines_interfaces.configuration_provider import ConfigurationProvider
from mu_pipelines_interfaces.destination_module_interface import (
    DestinationConfig,
    DestinationModuleInterface,
)
from pyspark.sql import DataFrame

from mu_pipelines_destination_spark.context.spark_context import MUPipelinesSparkContext


class PrintDestination(DestinationModuleInterface):
    def __init__(
        self, config: DestinationConfig, configuration_provider: ConfigurationProvider
    ):
        super().__init__(config, configuration_provider)

    def save(self, df: DataFrame, context: MUPipelinesSparkContext) -> None:
        df.show()
