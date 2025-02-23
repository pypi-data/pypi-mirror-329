import numpy as np
from sklearn.linear_model import LinearRegression


class Predictor:
    def __init__(self):
        pass

    def train_predictor(self, history):
        if len(history) < 2:
            return history[-1] if history else 0

        X = np.arange(len(history)).reshape(-1, 1)
        y = np.array(history)
        model = LinearRegression().fit(X, y)
        return model.predict([[len(history)]])[0]

    def predict(self, cpu_history, memory_history, network_sent_history, network_recv_history):
        return {
            "predicted_cpu": self.train_predictor(cpu_history),
            "predicted_memory": self.train_predictor(memory_history),
            "predicted_network_sent": self.train_predictor(network_sent_history),
            "predicted_network_recv": self.train_predictor(network_recv_history)
        }
