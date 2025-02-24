import typing as t
import torch.nn as nn
from torch.utils.data import DataLoader
from pydantic import BaseModel


class TrainSet(BaseModel):
    loader: t.Callable[[], DataLoader]
    model: t.Callable[[], nn.Module]
