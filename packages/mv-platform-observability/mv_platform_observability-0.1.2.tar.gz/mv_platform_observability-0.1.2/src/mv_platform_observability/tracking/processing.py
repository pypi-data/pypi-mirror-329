import logging
from abc import ABC
from typing import Dict, Any, Optional, List

from mv_platform_core import DataReader, DataWriter, DefaultDataProcessing
from pydantic import BaseModel
from pyspark.sql import SparkSession

from mv_platform_observability.collectors.metrics import MetricCollector
from mv_platform_observability.decorator import TrackExecution


# This needs to be moved into future mv-platform-data-contract library
class PipelineConfig(BaseModel):
    job_name: str
    input_tables: Dict[str, Any]
    transformation_file: str
    output_destination: str

    class Config:
        arbitrary_types_allowed = True


class TrackableProcessing(ABC):
    config: PipelineConfig
    """Mixin for adding tracking capabilities"""
    def get_tracking_parameters(self) -> Dict[str, Any]:
        return {
            "job_name": getattr(self, "job_name", self.__class__.__name__),
            "input_tables": self.config.input_tables,
            "output_destination": self.config.output_destination
        }


class ConfigurableDataProcessing(DefaultDataProcessing, TrackableProcessing):
    def __init__(self,
                 config: PipelineConfig,
                 reader: DataReader,
                 writer: DataWriter,
                 spark: SparkSession = None,
                 metrics_collector: Optional[MetricCollector] = None):
        super().__init__(
            reader=reader,
            writer=writer,
            spark=spark,
            configs=dict(
                path=config.transformation_file
            )
        )
        self.metrics_collector = metrics_collector
        self.config = config
        self.job_name = config.job_name

    @property
    def tracking_decorator(self):
        return TrackExecution(
            metrics_collector=self.metrics_collector,
            input_parameters=self.get_tracking_parameters(),
            logger=logging.Logger("ConfigurableDataProcessing")
        )

    def execute_pipeline(self):
        return self.tracking_decorator(super().execute_pipeline)()
