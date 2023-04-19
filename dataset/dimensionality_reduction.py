import sklearn
import importlib
import numpy as np
from omegaconf import DictConfig

def reducer_factory(
        name: str, params: dict, import_module: str="sklearn.decomposition", **kwargs
    ):
    """Returns a scikit-learn model."""
    model_class = getattr(importlib.import_module(import_module), name)
    model = model_class(**params)  # Instantiates the model
    return model

def reduce_dimensionality(
        X_train: np.ndarray, X_val: np.ndarray, cfg: DictConfig
    ):  
    """Reduce dimensionality of the genotype matrix."""
    reducer = reducer_factory(**cfg)
    X_train_reduced = reducer.fit_transform(X_train)
    X_val_reduced = reducer.transform(X_val)

    return X_train_reduced, X_val_reduced