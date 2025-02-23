import time
import logging
from utils.aws_client import get_aws_client

class AWSLambdaMonitor:
    def __init__(self, function_name):
        self.client = get_aws_client("cloudwatch")
        self.function_name = function_name

    def get_execution_time(self):
        """Fetches the average execution time of the AWS Lambda function."""
        try:
            response = self.client.get_metric_statistics(
                Namespace="AWS/Lambda",
                MetricName="Duration",
                Dimensions=[{"Name": "FunctionName", "Value": self.function_name}],
                StartTime=time.time() - 3600,
                EndTime=time.time(),
                Period=300,
                Statistics=["Average"]
            )
            return response["Datapoints"][-1]["Average"] if response["Datapoints"] else None
        except Exception as e:
            logging.error(f"Error fetching Lambda execution time: {e}")
            return None
