import hydra
from omegaconf import DictConfig, OmegaConf
from dataset.dimensionality_reduction import reduce_dimensionality
from models.sklearn_factory import train_model
from evaluator.r2_evaluator import evaluate_model
import numpy as np

@hydra.main(version_base=None, config_path="config", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    #TODO: Load dataset
    X_train = np.random.rand(1000, 500)
    X_val = np.random.rand(100, 500)
    y_train = np.random.rand(1000)
    y_val = np.random.rand(100)

    X_train_reduced, X_val_reduced = reduce_dimensionality(X_train, X_val, cfg.dataset.dimensionality_reduction)
    model = train_model(X_train_reduced, y_train, cfg.model)
    results = evaluate_model(model, X_val_reduced, y_val)
    print(results)


    
if __name__ == "__main__":
    my_app()