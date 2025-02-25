import asyncio
import traceback
from datetime import datetime
from functools import wraps
from logging import Logger

from pydantic import BaseModel, ConfigDict
from mv_platform_observability.collectors.metrics import MetricCollector

class TrackExecution(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    metrics_collector: MetricCollector
    input_parameters: dict
    logger: Logger

    def __call__(self, original_func=None):
        @wraps(original_func)
        def wrapper(*args, **kwargs):
            original_func_result = None
            start = datetime.now()
            try:
                original_func_result = original_func(*args, **kwargs)
                end, execution_time = _execution_time(start)
                self.metrics_collector.send_metric(dict(
                    job_result=original_func_result,
                    start_time=start.isoformat(),
                    end_time=end.isoformat(),
                    execution_time=execution_time.total_seconds(),
                    input_params=self.input_parameters
                ))
            except Exception as e:
                self.logger.error(f"Error occurred: {str(e)}")
                raise
            return original_func_result


        def _execution_time(start):
            end = datetime.now()
            return end, end - start
        return wrapper
