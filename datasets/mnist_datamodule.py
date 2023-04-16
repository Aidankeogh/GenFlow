# Mnist but it loads data in as 

from torch.utils.data import DataLoader
from torchvision.datasets import MNIST
from torch.utils.data import random_split
from torchvision import transforms
from torch import Tensor
import lightning as L

class MnistDataModule(L.LightningDataModule):
    def __init__(self, batch_size=32, data_dir='data') -> None:
        super().__init__()
        self.batch_size = batch_size
        self.data_dir = data_dir

    def setup(self, stage: str = None):
        mnist_transform = transforms.Compose([
                               transforms.ToTensor(),
                               transforms.Normalize(
                                 (0.1307,), (0.3081,))
                             ])
        self.mnist_test = MNIST(self.data_dir, train=False, transform=mnist_transform)
        mnist_full = MNIST(self.data_dir, train=True, transform=mnist_transform)
        self.mnist_train, self.mnist_val = random_split(mnist_full, [55000, 5000])

    def train_dataloader(self):
        return DataLoader(
            self.mnist_train, 
            batch_size=self.batch_size,
            shuffle=True)

    def val_dataloader(self):
        return DataLoader(
            self.mnist_val, 
            batch_size=self.batch_size,
            shuffle=False)

    def test_dataloader(self):
        return DataLoader(
            self.mnist_test, 
            batch_size=self.batch_size,
            shuffle=False)
