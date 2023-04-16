import unittest

from datasets.mnist_datamodule import MnistDataModule

class TestDataset(unittest.TestCase):

    def setUp(self):
        self.dataset = MnistDataModule(batch_size=32)
        self.dataset.setup()

    def test_dataset(self):
        self.train_loader = self.dataset.train_dataloader()
        x, y = next(iter(self.train_loader))
        self.assertEqual(x.shape, (32, 1, 28, 28))
        self.assertTrue(y.shape, (32))

if __name__ == '__main__':
    unittest.main()