from typing import Literal
import torch
import torch.nn as nn
import torch.nn.functional as F


class HypersphereHead(nn.Module):
    def __init__(self, num_class, embed_dim, temp=0.07):
        super().__init__()
        self.prototypes = nn.Parameter(torch.randn(num_class, embed_dim))
        self.temp: torch.Tensor
        self.register_buffer("temp", torch.tensor(temp))

    def forward(self, x):
        x = F.normalize(x, dim=-1)
        prototypes = F.normalize(self.prototypes, dim=-1)
        return (x @ prototypes.T) / self.temp


class GaussianHead(nn.Module):
    def __init__(self, num_class, embed_dim, temp=0.07):
        super().__init__()
        self.prototypes = nn.Parameter(torch.randn(num_class, embed_dim) * 0.1)
        self.temp: torch.Tensor
        self.register_buffer("temp", torch.tensor(temp))

    def forward(self, x):
        dist = torch.cdist(x, self.prototypes)
        return -dist / self.temp


class StudentHead(nn.Module):
    def __init__(self, num_class, embed_dim, alpha=1.0):
        super().__init__()
        self.prototypes = nn.Parameter(torch.randn(num_class, embed_dim))
        self.alpha: torch.Tensor
        self.register_buffer("alpha", torch.tensor(alpha))
        print("WARNING: StudentHead head returns probablity")

    def forward(self, x):
        l2_sq = torch.cdist(x, self.prototypes).pow(2)
        q = 1.0 + l2_sq / self.alpha
        q = q.pow(-(self.alpha + 1.0) / 2.0)
        q = q / q.sum(1, keepdim=True)
        return q


def with_model_head(
    model: nn.Module,
    head_type: Literal["hypersphere", "gaussian", "student", "linear"],
    num_class: int,
    embed_dim: int,
):
    if head_type == "hypersphere":
        model.fc = HypersphereHead(num_class=num_class, embed_dim=embed_dim)
        return model
    elif head_type == "gaussian":
        model.fc = GaussianHead(num_class=num_class, embed_dim=embed_dim)
        return model
    elif head_type == "student":
        model.fc = StudentHead(num_class=num_class, embed_dim=embed_dim)
        return model
    elif head_type == "linear":
        model.fc = nn.Linear(embed_dim, num_class, bias=True)
        return model
    else:
        raise NotImplementedError(f"Classifier not implemented: {head_type}")
