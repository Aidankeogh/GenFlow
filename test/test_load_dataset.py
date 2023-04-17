from omegaconf import OmegaConf
import unittest
from datasets.load_dataset import load_dataset

class TestTrainer(unittest.TestCase):

    def test_trainer(self):
        cfg = OmegaConf.load("config/dataset/loco_clean.yaml")
        X_geno, y_pheno = load_dataset(cfg)
        print(X_geno.shape, y_pheno.shape)

if __name__ == '__main__':
    unittest.main()