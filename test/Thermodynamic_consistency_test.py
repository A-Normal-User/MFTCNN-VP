import matplotlib.pyplot as plt
from model import Net
import numpy as np
import pandas as pd
from scipy.constants import R
import torch
import torch.nn as nn
import torch.nn.functional as F
import scipy
torch.set_num_threads(18)
# 随机数种子
seed = 218105633
torch.manual_seed(seed)
np.random.seed(seed)
# 训练的物质数量
count_substance = 459
# 每个物质的数据量
count_data = 1000

# # 测试的物质
substance = [
    "3,6-methano-1,4-cyclohexadiene", # P
    "1,3,5-cycloheptatriene",
    "1-butylcyclopentene",
    "1-methylcyclohexene",
    "2-methyltetradecane",
    "4-methylcyclohexene",
    "cyclopentacycloheptene",
    'cis-2,2-dimethyl-3-hexene',
    'trans-2,2-dimethyl-3-hexene',
    'cis-3-decene',
    'trans-3-decene',
    'cis-4,4-dimethyl-2-pentene',
    'trans-tert-butyl-2-methylethylene',
    'cis-3-nonene',
    'trans-3-nonene',
    'cis-4-decene',
    'cis-5-decene',
    'trans-4-decene',
    'trans-5-decene',
    'cis-perhydroindene',
    'trans-perhydroindene',
    '1,3-di-tert-butylbenzene',
    '1,1,4,7-tetramethylindan',
    '1-methyl-2-butylacetylene',
    'cyclobutane, methylene-',
    '.beta.-myrcene',
    '(.+-.)-3-carene',
    '1,3-bis(1,1-dimethylethyl)-5-methylbenzene',
    'spiro[2.2]pentane',
    '1,1\'-bicyclopentyl',
    '1-ethyl-2-phenylbenzene',
    'bicyclo[4.2.0]octane',
    '1H-indene, octahydro-, trans-',
    '1-cyclohexylhexane',
    '1,2-dihydronaphthalene',
    '8,9,10-trinorcarane',
    '4,7-methano-1H-indene, octahydro-, (3a.alpha.,4.beta.,7.beta.,7a.alpha.)-',
    'bicyclo[6.1.0]nonane',
    '1,2-diisopropylbenzene',
    '1-ethyl-2,4,6-trimethylbenzene',
]
model_name = [
    1131796,
    8017474,
    18094361,
    26318864,
    28378614,
    157564161,
    218105633,
    609641183,
    1228297609,
    4227255766
]
model = []
for i in range(len(model_name)):
    model.append(Net())
    model[i].load_state_dict(torch.load(f'../model/model_{model_name[i]}.pt', weights_only=True))
    model[i].eval()
    model[i] = model[i].double()
    model[i] = torch.jit.script(model[i])
mean_std = pd.read_csv('../database/mean_std.csv')
mean = mean_std['mean'].values
std = mean_std['std'].values
filterdata = pd.read_csv('../database/HC459_testset.csv')
# 读取实验数据
expdata = pd.read_csv('../database/testset_exp.csv')
# 选出substance中的物种
filterdata = filterdata[filterdata['Name'].isin(substance)]
subdata = filterdata
# 给出为True的行的下标
subdata.reset_index(drop=True, inplace=True)

Q = []
B = np.log(100000)
count_sign = 0
for i in range(len(subdata)):
    database = np.zeros((1000, 45), dtype=np.double)
    feature = subdata.iloc[i, 2:46].values
    feature = (feature - mean) / std
    exp = expdata[expdata['name'] == subdata.loc[i, 'Name']]
    exp_T = exp['temperature'].values
    Tlower = exp_T.min()
    Tupper = subdata.loc[i, 'TC']
    # 读取临界温度和临界压力
    Tc = subdata.loc[i, 'TC']
    Pc = subdata.loc[i, 'PC']
    # 生成Tr数据
    T = np.linspace(Tlower, Tupper, 1000, dtype=np.double) 
    database[:, 0:44] = feature
    database[:, 44] = T / Tc
    # 预测
    y_pred = []
    with torch.no_grad():
        database = torch.from_numpy(database).double()
        for j in range(len(model_name)):
            y_pred.append(model[j](database[:, 0:44], database[:, 44:45]).numpy().flatten())
    y_pred = np.array(y_pred, dtype=np.double)
    # 计算平均值
    y_hat = np.mean(y_pred, axis=0)
    # print(y_hat)
    # 计算标准差
    # y_std = np.std(y_pred, axis=0, ddof=1)
    # 计算平均值
    A = np.log(Pc) - B
    log_pred = y_hat * A + B
    p_pred = log_pred
    # 计算p_pred关于T的导数
    W = R * T * T * np.gradient(p_pred, T)
    dW_dT = np.gradient(W, T)
    d2W_dT2 = np.gradient(dW_dT, T)
    d2W_dT2 = d2W_dT2[3:-3]  # 去除边界效应
    T = T[3:-3]  # 去除边界效应
    F = (np.abs(d2W_dT2) - d2W_dT2) / 2
    # 做F关于T的梯形积分
    integral = scipy.integrate.trapezoid((F) ** 2, T)
    Q.append(integral)
    dW_dT = dW_dT[3:-3]
    if np.any(np.diff(np.sign(dW_dT))):
        # print(f'{subdata.iloc[i, 0]} has zero crossing in dW/dT')
        count_sign += 1
    print(f'{subdata.iloc[i, 0]}: {integral}')

Q = np.array(Q)
print((f'Q = {Q.tolist()};'))  
print(f'Q: {Q.mean()}, count_sign: {count_sign}')
