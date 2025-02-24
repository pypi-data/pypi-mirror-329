import torch.nn as nn
import torch.nn.functional as F


class FC1Module(nn.Module):
    """1 layer fc module. also be called MLP Head"""

    def __init__(
        self,
        in_features: int,
        out_features: int,
    ) -> None:
        super().__init__()
        self.fc = nn.Linear(in_features, out_features)

    def forward(self, x):
        x = self.fc(x)
        return x


class FcModule(nn.Module):
    def __init__(
        self,
        in_features: int,
        out_features: int,
        activate_func: str = "relu",
    ):
        super().__init__()
        self.encoder1 = nn.Linear(in_features, 256)
        self.encoder2 = nn.Linear(256, 128)
        self.encoder3 = nn.Linear(128, out_features)

        if activate_func == "sigmoid":
            self.ac_func = F.sigmoid
        else:
            self.ac_func = F.relu

    def forward(self, x):
        x = self.encoder1(x)
        x = self.ac_func(x)
        x = self.encoder2(x)
        x = self.ac_func(x)
        x = self.encoder3(x)
        return x
