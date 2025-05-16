import unittest
import numpy as np
from lorenz_attractor import lorenz_series

class TestLorenzSeries(unittest.TestCase):

    def test_time_goes_forward(self):
        data = lorenz_series(1, 1, 1)
        times = data[:, 0]
        step_sizes = np.diff(times)

        self.assertTrue(np.allclose(step_sizes, 0.01), "Час має змінюватися з однаковим кроком 0.01")

    def test_chaos_behavior(self):
        first = lorenz_series(1, 1, 1)
        second = lorenz_series(1.0001, 1, 1)

        differences = np.linalg.norm(first - second, axis=1)

        self.assertGreater(differences[-1], 1, "Система повинна розходитися через хаос")

if __name__ == '__main__':
    unittest.main()