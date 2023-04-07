import torch
import lightning
import sklearn
import hydra
from omegaconf import DictConfig, OmegaConf

print(torch.__version__)
print(lightning.__version__)
print(sklearn.__version__)


@hydra.main(version_base=None, config_path="config", config_name="config")
def my_app(cfg: DictConfig) -> None:
    print(OmegaConf.to_yaml(cfg))
    
my_app()