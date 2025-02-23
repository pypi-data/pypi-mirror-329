import unittest
from adapto.scaler import AutoScaler

class TestAutoScaler(unittest.TestCase):
    def test_default_thresholds(self):
        scaler = AutoScaler()
        self.assertEqual(scaler.cpu_threshold, 75)
        self.assertEqual(scaler.memory_threshold, 75)

if __name__ == '__main__':
    unittest.main()