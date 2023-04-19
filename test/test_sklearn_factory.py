from omegaconf import OmegaConf
import unittest
from models.sklearn_factory import train_model
import numpy as np

class TestSklearnFactory(unittest.TestCase):

    def test_sklearn_factory(self):
        cfg = OmegaConf.create({
            "name": "LinearRegression",
            "import_module": "sklearn.linear_model",
            "params": {
                "fit_intercept": True
            }
        })
        X_train = np.random.rand(1000, 500)
        y_train = np.random.rand(1000)
        model = train_model(X_train, y_train, cfg)
        self.assertEqual(model.coef_.shape, (500,))


if __name__ == '__main__':
    unittest.main()