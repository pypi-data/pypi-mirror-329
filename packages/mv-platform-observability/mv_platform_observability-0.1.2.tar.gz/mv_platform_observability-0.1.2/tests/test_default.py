import logging
import os
import tempfile
from unittest.mock import Mock

import pytest
from mv_platform_core import DefaultDataProcessing
from mv_platform_core.writers import WriterFactory

from mv_platform_observability.collectors.metrics import EventHubCollector
from mv_platform_observability.decorator import TrackExecution

from mv_platform_core.readers import ReaderFactory

from pyspark.sql import SparkSession
from dotenv import load_dotenv

from mv_platform_observability.tracking.processing import ConfigurableDataProcessing, PipelineConfig


class TestDefaultTemplate:

    load_dotenv("../.env.tst")

    @pytest.fixture(autouse=True)
    def prepare_spark_session(self, spark_session: SparkSession):
        self.spark = spark_session

    @pytest.fixture(scope="function")
    def sample_data(self):
        data = [("1", "John", 30), ("2", "Jane", 25), ("3", "Bob", 35)]
        columns = ["id", "name", "age"]
        df = self.spark.createDataFrame(data, columns)
        df.createOrReplaceTempView("sample_table")
        self.temp_dir = tempfile.TemporaryDirectory().name
        self.spark.sql(f"""
            CREATE TABLE IF NOT EXISTS below_thirty 
                (ID STRING, NAME STRING, AGE LONG, as_of_date Date) 
                USING DELTA
                PARTITIONED BY (as_of_date)
                LOCATION '{self.temp_dir}/below_thirty'
        """)
        yield
        self.spark.catalog.dropTempView("sample_table")


    def test_decorator(self, sample_data):
        bronze_tables = {
            "sample": {
                "table_name": "sample_table",
                "primary_keys": ["id"],
                "filter_column": "age",
                "filter_condition": "age > 0"
            }
        }
        bronze_reader = ReaderFactory.create_reader("bronze", tables=bronze_tables)
        #FIXME date should be current_date instead of hardcoded
        scd_one_writer = WriterFactory.create_writer("scd_one",spark=self.spark, as_of_date="2025-02-24", destination=f"{self.temp_dir}/below_thirty")

        metrics_collector = EventHubCollector(
            connection_string=os.getenv("EH_TEST"),
            event_hub_name="metrics-events"
        )

        pipeline_config = PipelineConfig(
            job_name="V2_data_transformation_job",
            input_tables=bronze_tables,
            transformation_file="./transformation.sql",
            output_destination="silver.below_thirty"
        )
        pipeline = ConfigurableDataProcessing(
            config=pipeline_config,
            reader=bronze_reader,
            writer=scd_one_writer,
            spark=self.spark,
            metrics_collector=metrics_collector
        )

        pipeline.execute_pipeline()

