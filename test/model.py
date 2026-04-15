import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np

class Residual_std_gelu(nn.Module):  #@save
    def __init__(self, input_View):
        super().__init__()
        self.Res = nn.Sequential(
            nn.Linear(input_View, input_View),
            nn.GELU(),
            nn.Linear(input_View, input_View),
            nn.GELU(),
            )

    def forward(self, X):
        return self.Res(X) + X

class Residual_1_3_gelu(nn.Module):  #@save
    def __init__(self, input_View):
        super().__init__()
        self.L1 = nn.Sequential(
            nn.Linear(input_View, input_View),
            nn.GELU(),
            )
        self.L2 = nn.Sequential(
            nn.Linear(input_View, input_View),
            nn.GELU(),
            nn.Linear(input_View, input_View),
            nn.GELU(),
            nn.Linear(input_View, input_View),
            nn.GELU(),
            )
    def forward(self, X):
        X = self.L1(X)
        Y = self.L2(X)
        return Y + X

# Neural Network
class Net(nn.Module):
    def __init__(self):
        super(Net, self).__init__()
        # 处理分子指纹
        self.mole = nn.Sequential(
            nn.Linear(44, 64),
            Residual_std_gelu(64),
        )
        # 处理温度
        self.temp = nn.Sequential(
            nn.Linear(1, 64),
            nn.GELU(),
            nn.Linear(64, 64),
            nn.GELU(),
            nn.Linear(64, 64),
            nn.GELU(),
        )
        # 压力计算
        self.pressure = nn.Sequential(
            Residual_1_3_gelu(128),
            Residual_1_3_gelu(128),
            nn.Linear(128, 1),
        )
    def forward(self, feature, temperature):
        return self.pressure(
            torch.cat(
                (
                    self.mole(feature),
                    self.temp(temperature),
                ),
                     dim=1))