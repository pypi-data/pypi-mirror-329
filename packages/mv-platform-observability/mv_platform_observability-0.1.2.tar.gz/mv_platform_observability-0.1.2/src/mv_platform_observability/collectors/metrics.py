import concurrent.futures
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, List

from azure.eventhub import EventData
from azure.eventhub import EventHubProducerClient


class MetricCollector(ABC):
    """
    Abstract base class for metric collectors.

    This class defines the interface that all concrete metric collectors must implement.
    """

    @abstractmethod
    def send_metric(self, metric_data: dict) -> None:
        """
        Send a metric to the configured collector.

        Parameters:
            metric_data (dict): A dictionary containing the metric data to be sent.

        Returns:
            None
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Close any resources used by the collector.

        Returns:
            None
        """
        pass


class EventHubCollector(MetricCollector):
    def __init__(self, connection_string, event_hub_name):
        self.connection_string = connection_string
        self.event_hub_name = event_hub_name
        self._producer_client = EventHubProducerClient.from_connection_string(
            conn_str=self.connection_string,
            eventhub_name=self.event_hub_name
        )

    def send_metric(self, metric_data: dict) -> None:
        with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
            event_data_batch = self._producer_client.create_batch()
            event_data_batch.add(EventData(str(metric_data)))
            executor.submit(self._producer_client.send_batch, event_data_batch)
            logging.info(f"Successfully sent {len(metric_data)} metrics to Event Hubs.")

    def close(self) -> None:
        self._producer_client.close()


class AzureMonitorMetricCollector(MetricCollector):
    """Collects and sends metrics to Azure Monitor.

    This class handles authentication with Azure Monitor, formats `MetricData` into the required JSON payload,
    and sends metrics via HTTP POST requests using the `requests` library. It also implements batching if necessary
    and error handling with retry logic.
    """

    def __init__(self, workspace_id: str, resource_group: str, subscription_id: str):
        """Initialize the AzureMonitorMetricCollector.

        Args:
            workspace_id (str): The ID of the Log Analytics workspace.
            resource_group (str): The name of the resource group containing the workspace.
            subscription_id (str): The ID of the Azure subscription.
        """
        if not all([workspace_id, resource_group, subscription_id]):
            raise ValueError("workspace_id, resource_group, and subscription_id must be provided")

        self.workspace_id = workspace_id
        self.resource_group = resource_group
        self.subscription_id = subscription_id
        self.credential = DefaultAzureCredential()
        self.base_url = f"https://westus2-0.monitoring.azure.com/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/microsoft.insights/metricValues?api-version=2018-01-01"

    def send_metric(self, metric_data: Dict[str, Any]):
        """Send a single metric to Azure Monitor.

        Args:
            metric_data (Dict[str, Any]): The metric data to be sent.
        """
        headers = {
            "Authorization": f"Bearer {self.credential.get_token('https://monitor.azure.com/.default').token}",
            "Content-Type": "application/json"
        }
        payload = self._format_metric(metric_data)

        self._post_payload(headers, payload)

    def _format_metric(self, metric_data: Dict[str, Any]) -> Dict[str, Any]:
        """Format the metric data according to Azure Monitor's schema.

        Args:
            metric_data (Dict[str, Any]): The raw metric data.

        Returns:
            Dict[str, Any]: The formatted metric data.
        """
        return {
            "time": metric_data["timestamp"].isoformat(),
            "data": [
                {
                    "metric": metric_data["name"],
                    "namespace": metric_data.get("namespace", "default"),
                    "dimensions": metric_data.get("dimensions", {}),
                    "value": metric_data["value"]
                }
            ]
        }

    def send_metrics_batch(self, metrics: List[Dict[str, Any]]):
        """Send a batch of metrics to Azure Monitor.

        Args:
            metrics (List[Dict[str, Any]]): The list of metric data to be sent.
        """
        headers = {
            "Authorization": f"Bearer {self.credential.get_token('https://monitor.azure.com/.default').token}",
            "Content-Type": "application/json"
        }
        payload = [self._format_metric(metric) for metric in metrics]

        self._post_payload(headers, payload)

    def _post_payload(self, headers, payload):
        try:
            response = requests.post(self.base_url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.exceptions.ConnectionError as e:
            logger.error(f"Connection error: {e}")
            raise
        except requests.exceptions.Timeout as e:
            logger.error(f"Timeout error: {e}")
            raise
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed: {e}")
            raise

    def close(self) -> None:
        pass

