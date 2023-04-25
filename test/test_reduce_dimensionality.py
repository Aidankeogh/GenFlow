from omegaconf import OmegaConf
import unittest
from dataset.dimensionality_reduction import reduce_dimensionality
import numpy as np

class TestReduceDimensionality(unittest.TestCase):

    def test_reduce_dimensionality(self):
        cfg = OmegaConf.create(
            {
                "name": "PCA",
                "params": {
                    "n_components": 25
                }
            }
        )
        X_train = np.random.rand(1000, 500)
        X_val = np.random.rand(100, 500)
        X_train_reduced, X_val_reduced = reduce_dimensionality(X_train, X_val, cfg)
        self.assertEqual(X_train_reduced.shape, (1000, 25))
        self.assertEqual(X_val_reduced.shape, (100, 25))

if __name__ == '__main__':
    unittest.main()