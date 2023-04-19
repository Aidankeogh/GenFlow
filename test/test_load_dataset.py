from omegaconf import OmegaConf
import unittest
from dataset.load_dataset import load_dataset

class TestLoadDataset(unittest.TestCase):

    def test_load_dataset(self):
        pass
        #cfg = OmegaConf.load("config/dataset/loco_clean.yaml")
        #X_geno, y_pheno = load_dataset(cfg)
        #print(X_geno.shape, y_pheno.shape)

if __name__ == '__main__':
    unittest.main()