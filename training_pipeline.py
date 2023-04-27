import hydra
from omegaconf import DictConfig, OmegaConf
from dataset.data_generator import training_set
from models.sklearn_factory import train_model
from evaluator.r2_evaluator import evaluate_model
from sklearn.model_selection import train_test_split
import numpy as np

@hydra.main(version_base=None, config_path="config", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    
    # For now, run on LD pruned r2=0.05 pre-filtered for uknown variants. Later, expand to the 
    # LD pruned r2=0.8 datatset.  Passing in the dataset pre-filtered for uknown SNPs is optional, 
    # but it really speeds up having to process from the LD pruned plink version everytime.  
    X_Geno, Y_Pheno = training_set(ds_pkl = 'dataset/ds_known.pkl')
    X_train, X_val, y_train, y_val = train_test_split(X_geno, Y_pheno, test_size=0.20, random_state=42)

    model = train_model(X_train, y_train, cfg.model)
    results = evaluate_model(model, X_val, y_val)
    print(results)


    
if __name__ == "__main__":
    my_app()