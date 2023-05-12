import hydra
from omegaconf import DictConfig, OmegaConf
from dataset.data_builder import training_data
from models.sklearn_factory import train_model
from evaluator.r2_evaluator import evaluate_model
from sklearn.model_selection import train_test_split
from utils.mlflow_utils import log_params_from_omegaconf_dict
import numpy as np
import hashlib
import mlflow

@hydra.main(version_base=None, config_path="config", config_name="config")
def my_app(cfg: DictConfig) -> None:
    mlflow.set_experiment("optuna_test")
    with mlflow.start_run():
        
        print("Config: ")
        print(OmegaConf.to_yaml(cfg))
        log_params_from_omegaconf_dict(cfg)

        X_geno, Y_pheno = training_data(**cfg.dataset.params).gwas_filtered(cfg.dataset.gwas_p_value)
        X_train, X_val, y_train, y_val = train_test_split(X_geno, Y_pheno, test_size=0.20, random_state=42)

        model = train_model(X_train, y_train, cfg.model)
        results = evaluate_model(model, X_val, y_val)
        
        # mlflow log all results
        for result, trait in zip(results, cfg.dataset.params.select_traits):
            print(result, trait)
            mlflow.log_metric(f"R2_{trait}", result)
        mlflow.log_metric("R2_mean", results.mean())
        
        print(results)

    return results.mean()
    
if __name__ == "__main__":
    mlflow.set_tracking_uri("http://narrows-gpu.sdsc.edu:5000")
    my_app()