import logging
import os

from mv_platform_observability.collectors.metrics import EventHubCollector
from mv_platform_observability.decorator import TrackExecution
from dotenv import load_dotenv

load_dotenv("../../.env")

class TestDecorator:

    def test_track_execution_with_eh(self):
        connection=os.getenv("EVENTHUB_DATA12K")
        collector = EventHubCollector(
            connection_string=connection,
            event_hub_name="metrics-events"
        )
        @TrackExecution(
            metrics_collector=collector,
            input_parameters={"name": "test"},
            logger=logging.Logger("test_Decorator")
        )
        def dummy_function():
            return "success"

        result = dummy_function()
        assert result == "success"
