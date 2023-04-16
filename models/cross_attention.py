import torch
import torch.nn as nn
import torch.nn.functional as F
from torch import Tensor
import math

class PositionalEncoding(nn.Module):

    def __init__(self, d_model: int, max_len: int = 5000):
        super().__init__()

        position = torch.arange(max_len).unsqueeze(1)
        div_term = torch.exp(torch.arange(0, d_model, 2) * (-math.log(10000.0) / d_model))
        pe = torch.zeros(max_len, 1, d_model)
        pe[:, 0, 0::2] = torch.sin(position * div_term)
        pe[:, 0, 1::2] = torch.cos(position * div_term)
        self.register_buffer('pe', pe)

    def forward(self, x: Tensor) -> Tensor:
        x = x + self.pe[:x.size(0)]
        return x


class FF_block(nn.Module):
    def __init__(self, d_model: int):
        super().__init__()
        self.fc1 = nn.Linear(d_model, d_model)
        self.norm = nn.LayerNorm(d_model)
        self.fc2 = nn.Linear(d_model, d_model)
    
    def forward(self, x: Tensor) -> Tensor:
        x = self.fc1(x)
        x = F.relu(x)
        x = self.norm(x)
        x = self.fc2(x)
        return x


class CrossAttentionModel(nn.Module):
    def __init__(self, d_model: int, n_tasks: int, num_heads = 4, n_classes=10):
        super().__init__()

        self.embedder = nn.Sequential(
            nn.Linear(1, d_model), 
            PositionalEncoding(d_model)
        )  
        queries = torch.randn(1, n_tasks, d_model)
        self.register_parameter('queries', nn.Parameter(queries))
        self.mh_attention = nn.MultiheadAttention(d_model, num_heads, batch_first=True)
        self.key = FF_block(d_model)
        self.value = FF_block(d_model)

        self.cls_head = nn.Linear(d_model, n_classes)
    
    def forward(self, x: Tensor) -> Tensor:
        x = self.embedder(x)
        key = self.key(x)
        value = self.value(x)

        queries = self.queries.repeat(x.shape[0], 1, 1)
        x, _ = self.mh_attention(queries, key, value)
        x = self.cls_head(x)
        x = F.softmax(x, dim=-1)
        return x