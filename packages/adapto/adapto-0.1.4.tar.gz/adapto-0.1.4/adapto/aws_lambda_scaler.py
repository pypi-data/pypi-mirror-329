import logging
from utils.aws_client import get_aws_client
from adapto.config.settings import EXECUTION_TIME_THRESHOLD, LAMBDA_MEMORY_STEP, MIN_MEMORY, MAX_MEMORY
from adapto.aws_lambda_monitor import AWSLambdaMonitor


class AWSLambdaScaler:
    def __init__(self, function_name):
        self.client = get_aws_client("lambda")
        self.monitor = AWSLambdaMonitor(function_name)
        self.function_name = function_name

    def get_current_memory(self):
        """Retrieves the current memory allocation of the Lambda function."""
        try:
            response = self.client.get_function_configuration(FunctionName=self.function_name)
            return response["MemorySize"]
        except Exception as e:
            logging.error(f"Error fetching Lambda memory configuration: {e}")
            return None

    def scale_lambda_memory(self):
        """Adjusts Lambda memory allocation based on execution time."""
        execution_time = self.monitor.get_execution_time()
        if execution_time is None:
            return

        current_memory = self.get_current_memory()
        if current_memory is None:
            return

        if execution_time > EXECUTION_TIME_THRESHOLD and current_memory < MAX_MEMORY:
            new_memory = min(current_memory + LAMBDA_MEMORY_STEP, MAX_MEMORY)
            self.update_lambda_memory(new_memory)
        elif execution_time < EXECUTION_TIME_THRESHOLD * 0.6 and current_memory > MIN_MEMORY:
            new_memory = max(current_memory - LAMBDA_MEMORY_STEP, MIN_MEMORY)
            self.update_lambda_memory(new_memory)

    def update_lambda_memory(self, new_memory):
        """Updates the Lambda memory configuration."""
        try:
            self.client.update_function_configuration(
                FunctionName=self.function_name,
                MemorySize=new_memory
            )
            logging.info(f"Updated Lambda {self.function_name} memory to {new_memory}MB")
        except Exception as e:
            logging.error(f"Error updating Lambda memory: {e}")
