import sklearn
import importlib
import numpy as np
from omegaconf import DictConfig

def model_factory(
    name: str, params: dict,  import_module: str = "sklearn.linear_model", **kwargs
) -> sklearn.base.BaseEstimator:
    """Returns a scikit-learn model."""
    model_class = getattr(importlib.import_module(import_module), name)
    model = model_class(**params)  # Instantiates the model
    return model

def train_model(
        X_train: np.ndarray, y_train: np.ndarray, cfg: DictConfig
) -> sklearn.base.BaseEstimator:
    """Train a model."""
    model = model_factory(**cfg)
    model.fit(X_train, y_train)
    return model