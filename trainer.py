import lightning as L
import torch
import torch.nn as nn
import hydra
from omegaconf import DictConfig, OmegaConf
from torch import Tensor
from models.cross_attention import CrossAttentionModel
from torch import optim
from torchmetrics import Accuracy

class OmicsTrainer(L.LightningModule):
    def __init__(self, 
            model: nn.Module,
            config: DictConfig) -> None:
        super(OmicsTrainer, self).__init__()
        self.config = config
        self.model = model(**config.model)
        self.loss_fn = nn.CrossEntropyLoss()
        self.accuracy = Accuracy(task="multiclass", num_classes=10)
        self.train_accuracy = Accuracy(task="multiclass", num_classes=10)

    def forward(self, x: Tensor, **kwargs) -> Tensor:
        return self.model(x, **kwargs)

    def training_step(self, batch: Tensor, batch_idx: int) -> Tensor:
        x, y = batch
        x = x.view(-1, self.config.model.n_tasks * 28 * 28, 1)
        output = self.model(x)
        output = output.view(-1, 10)
        loss = self.loss_fn(output, y)

        self.log("train_loss", loss,prog_bar=True)
        self.train_accuracy(output, y)
        self.log('train_acc', self.train_accuracy, prog_bar=True, on_epoch=True)
        return loss
    
    def validation_step(self, batch: Tensor, batch_idx: int) -> Tensor:
        x, y = batch
        x = x.view(-1, self.config.model.n_tasks * 28 * 28, 1)
        output = self.model(x)
        output = output.view(-1, 10)
        loss = self.loss_fn(output, y)

        self.log("val_loss", loss, prog_bar=True)
        self.accuracy(output, y)
        self.log('val_acc', self.accuracy, prog_bar=True, on_epoch=True)
    
    def configure_optimizers(self):
        # access the saved hyperparameters
        opt = optim.SGD(self.parameters(), lr=self.config.hparams.lr)
        return opt 

cfg = OmegaConf.create(
    {
        "model": {
            "d_model": 32,
            "n_classes": 10,
            "n_tasks": 4
        },
        "hparams":{
            "lr": 0.1
        }
    }
)

model = OmicsTrainer(model=CrossAttentionModel, config=cfg)
from datasets.mnist_datamodule import MnistDataModule

trainer = L.Trainer()
trainer.fit(model, MnistDataModule(batch_size=32))