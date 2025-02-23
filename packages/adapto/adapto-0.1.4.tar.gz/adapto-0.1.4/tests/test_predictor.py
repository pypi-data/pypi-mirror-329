import unittest
from adapto.predictor import Predictor

class TestPredictor(unittest.TestCase):
    def setUp(self):
        self.predictor = Predictor()

    def test_prediction_with_data(self):
        cpu_history = [10, 20, 30, 40, 50]
        predicted_cpu = self.predictor.train_predictor(cpu_history)
        self.assertIsInstance(predicted_cpu, float)

    def test_prediction_with_empty_data(self):
        predicted_cpu = self.predictor.train_predictor([])
        self.assertEqual(predicted_cpu, 0)

if __name__ == '__main__':
    unittest.main()
