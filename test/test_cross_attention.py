import unittest
from models.cross_attention import CrossAttentionModel
import torch

class TestModel(unittest.TestCase):

    def setUp(self):
        self.model = CrossAttentionModel(d_model=32, n_classes=5, n_tasks=10)

    def test_model(self):
        self.assertTrue(self.model is not None)
        
        x = self.model(torch.randn(32, 10, 1))

        self.assertEqual(x.shape, (32, 10, 5))

if __name__ == '__main__':
    unittest.main()