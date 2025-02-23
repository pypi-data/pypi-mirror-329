import psutil
import time
import logging
from collections import deque
from adapto.predictor import Predictor

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class AutoScaler:
    def __init__(self, scale_up_threshold=75, scale_down_threshold=30, memory_threshold=75,
                 bandwidth_threshold=100000000, min_instances=1, max_instances=10, history_size=10, custom_scaling=None):
        self.scale_up_threshold = scale_up_threshold
        self.scale_down_threshold = scale_down_threshold
        self.memory_threshold = memory_threshold
        self.bandwidth_threshold = bandwidth_threshold  # in bytes per second
        self.current_instances = min_instances
        self.min_instances = min_instances
        self.max_instances = max_instances
        self.previous_network = psutil.net_io_counters()

        # Alias for test compatibility
        self.cpu_threshold = scale_up_threshold  # Fix for test cases

        # Optional custom scaling function; should accept (metrics, predictions) and return 'scale_up', 'scale_down', or 'no_change'
        self.custom_scaling = custom_scaling

        # Data history for prediction
        self.cpu_history = deque(maxlen=history_size)
        self.memory_history = deque(maxlen=history_size)
        self.network_sent_history = deque(maxlen=history_size)
        self.network_recv_history = deque(maxlen=history_size)

        self.predictor = Predictor()

    def get_system_metrics(self):
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        load_avg = psutil.getloadavg()[0] if hasattr(psutil, "getloadavg") else 0  # Unix-only
        disk_usage = psutil.disk_usage('/').percent
        network_metrics = self.get_network_metrics()

        # Store metrics in history
        self.cpu_history.append(cpu_usage)
        self.memory_history.append(memory_usage)
        self.network_sent_history.append(network_metrics['network_sent'])
        self.network_recv_history.append(network_metrics['network_recv'])

        return {
            "cpu_usage": cpu_usage,
            "memory_usage": memory_usage,
            "load_avg": load_avg,
            "disk_usage": disk_usage,
            **network_metrics
        }

    def get_network_metrics(self):
        network_io = psutil.net_io_counters()
        network_sent = network_io.bytes_sent - self.previous_network.bytes_sent
        network_recv = network_io.bytes_recv - self.previous_network.bytes_recv
        self.previous_network = network_io

        return {
            "network_sent": network_sent,
            "network_recv": network_recv
        }

    def predict_future_usage(self):
        return self.predictor.predict(
            list(self.cpu_history),
            list(self.memory_history),
            list(self.network_sent_history),
            list(self.network_recv_history)
        )

    def scale_up(self):
        if self.current_instances < self.max_instances:
            self.current_instances += 1
            logging.info(f"Scaling up: New instance count = {self.current_instances}")
        else:
            logging.info("Max instances reached. Cannot scale up further.")

    def scale_down(self):
        if self.current_instances > self.min_instances:
            self.current_instances -= 1
            logging.info(f"Scaling down: New instance count = {self.current_instances}")
        else:
            logging.info("Min instances reached. Cannot scale down further.")

    def monitor(self, interval=5):
        while True:
            metrics = self.get_system_metrics()
            predictions = self.predict_future_usage()

            logging.info(
                f"CPU: {metrics['cpu_usage']}% | Memory: {metrics['memory_usage']}% | Load Avg: {metrics['load_avg']} | Disk: {metrics['disk_usage']}% | "
                f"Network Sent: {metrics['network_sent']} bytes/s | Network Recv: {metrics['network_recv']} bytes/s"
            )
            logging.info(
                f"Predicted CPU: {predictions['predicted_cpu']}% | Predicted Memory: {predictions['predicted_memory']}% | "
                f"Predicted Network Sent: {predictions['predicted_network_sent']} bytes/s | Predicted Network Recv: {predictions['predicted_network_recv']} bytes/s"
            )

            # If a custom scaling strategy is provided, use it to decide the action
            if self.custom_scaling:
                action = self.custom_scaling(metrics, predictions)
                if action == 'scale_up':
                    self.scale_up()
                elif action == 'scale_down':
                    self.scale_down()
            else:
                # Default scaling strategy
                if (predictions['predicted_cpu'] > self.scale_up_threshold or
                    predictions['predicted_memory'] > self.memory_threshold or
                    predictions['predicted_network_sent'] > self.bandwidth_threshold or
                    predictions['predicted_network_recv'] > self.bandwidth_threshold):
                    self.scale_up()
                elif (predictions['predicted_cpu'] < self.scale_down_threshold and
                      predictions['predicted_memory'] < self.memory_threshold / 2 and
                      predictions['predicted_network_sent'] < self.bandwidth_threshold / 2 and
                      predictions['predicted_network_recv'] < self.bandwidth_threshold / 2):
                    self.scale_down()

            time.sleep(interval)


# Example usage
if __name__ == "__main__":
    scaler = AutoScaler()
    scaler.monitor()