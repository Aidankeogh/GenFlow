import torch
import lightning
import sklearn
import hydra
from omegaconf import DictConfig, OmegaConf
import importlib
from sklearn.linear_model import LogisticRegression

# print(torch.__version__)
# print(lightning.__version__)
# print(sklearn.__version__)

# linear = importlib.import_module("sklearn.linear_model")
# LR = getattr(linear, "LogisticRegression")
# print(LR, LogisticRegression)

@hydra.main(version_base=None, config_path="config", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    
my_app()