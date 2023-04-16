import importlib
import sklearn

def get_model(
    model_name: str, import_module: str, model_params: dict
) -> sklearn.base.BaseEstimator:
    """Returns a scikit-learn model."""
    model_class = getattr(importlib.import_module(import_module), model_name)
    model = model_class(**model_params)  # Instantiates the model
    return model

def create_dataset(config):

def train_model(config, dataset):
    model = get_model(config.model_name, config.import_module, config.model_params)
    model.fit(dataset.genotype, dataset.phenotype)
    return model

def evaluate_model(config, model, dataset):

def log_to_mlflow(config, model, )