import hydra
from omegaconf import DictConfig, OmegaConf
from hydra.core.hydra_config import HydraConfig
from dataset.data_builder import training_data
from dataset.dimensionality_reduction import reduce_dimensionality
from models.sklearn_factory import train_model
from evaluator.r2_evaluator import evaluate_model
from sklearn.model_selection import train_test_split
from utils.mlflow_utils import log_params_from_omegaconf_dict
import numpy as np
import hashlib
import mlflow
import warnings
import os
import pickle
warnings.filterwarnings("ignore")

@hydra.main(version_base=None, config_path="config", config_name="config")
def my_app(cfg: DictConfig) -> None:
    
    mlflow.set_experiment(cfg.experiment_name)
    with mlflow.start_run():
        print("Config: ")
        print(OmegaConf.to_yaml(cfg))
        log_params_from_omegaconf_dict(cfg)
        save_file = cfg.dataset.get("save_to_file", None)
        
        if save_file is not None and os.path.exists(save_file):
            with open(save_file, 'rb') as f:
                print(f"Loading saved dataset from {save_file}")
                X_geno, Y_pheno = pickle.load(f)
        else:
            X_geno, Y_pheno = training_data(
                    **cfg.dataset.params
            ).gwas_filtered(cfg.dataset.gwas_p_value)
            
            if save_file is not None: 
                with open(save_file, 'wb') as f:
                    print(f"Saving dataset to {save_file}")
                    pickle.dump( (X_geno, Y_pheno), f)
                    
                
        X_train, X_val, y_train, y_val = train_test_split(
            X_geno, Y_pheno, test_size=0.20, random_state=42
        )
        
        dr_cfg = cfg.get("dimensionality_reduction", None)
        if dr_cfg is not None:
            X_train, X_val = reduce_dimensionality(X_train, X_val, dr_cfg)            

        model = train_model(X_train, y_train, cfg.model)
        results = evaluate_model(model, X_val, y_val)
        
        # mlflow log all results
        traits = list(Y_pheno.columns)
        data_shape = X_geno.shape
        for result, trait in zip(results, traits):
            mlflow.log_metric(f"R2_{trait}", result)
        mlflow.log_metric("R2_mean", results.mean())
        mlflow.log_metric("Num_Variants", data_shape[1])

        print("Data Shape:", data_shape, "\n")
        print("R2 Results:", results)
        print("------------------------------------------\n")

    return results.mean()
    
if __name__ == "__main__":
    mlflow.set_tracking_uri("http://narrows-gpu.sdsc.edu:5000")
    my_app()