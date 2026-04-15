
## 语言选择
- [English](README.md)
- [中文](README_CN.md)

## 简介
在化学研究、工业应用和环境治理中，蒸气压是一个重要的物理性质参数，直接影响着物质的挥发性、沸点和热力学行为。准确预测蒸气压对于设计化工过程、评估环境风险和开发新材料具有重要意义。然而，传统的蒸气压预测方法往往依赖于大量的实验数据和复杂的理论模型，难以适应多样化的化学空间。
为了解决这一问题，我们提出了一种多保真度热力学一致神经网络（MFTCNN-VP），用于预测化合物的蒸气压。该模型结合了多保真度学习和热力学一致性约束，能够在保持高预测精度的同时，确保预测结果符合热力学规律。
我们在一个包含40种新烃类化合物的测试集上评估了MFTCNN-VP的性能，并与现有的蒸气压预测方法进行了比较。结果表明，MFTCNN-VP在测试集上的表现优于传统方法，具有更高的准确性和更好的热力学一致性。

## 使用MFTCNN-VP
1. 克隆仓库
    ```bash
    git clone https://github.com/A-Normal-User/MFTCNN-VP.git
    cd MFTCNN-VP
    ```
2. 安装依赖
    ```bash
    pip3 install -r requirements.txt
    ```
3. 运行测试集上热力学一致性测试代码
    ```bash
    python3 test/Thermodynamic_consistency_test.py
    ```
4. 运行测试集上指定物质的蒸气压曲线绘制代码
    ```bash
    jupyter notebook test/draw.ipynb
    ```

## 测试集性能指标对比
| Usage             | $R^2$           | RMSE(Pa)          | MAE(Pa)         | AARD(\%)        | Source          |
|---|---|---|---|---|---|
| MFTCNN-VP         | **0.9965** | **2,704.58** | **867.08** | **2.0936** | |
| MFTCNN-VP (prior) | 0.9304          | 1,1978.20         | 7,891.52        | 18.9577         | |
| GRAPPA            | 0.9558          | 9,959.35          | 4,919.18        | 10.831          | [GRAPPA](https://github.com/marco-hoffmann/GRAPPA) |
| mfp-sum Wagner EE | 0.9563          | 9,825.88          | 6,474.98        | 14.249          | [chemprop_VP](https://github.com/fatcat0322/chemprop_VP) |


## 文件说明
*   `database`: 包含全部测试集的特征向量，以及测试集的温度标签。
    *   `HC459_testset.csv`: 包含测试集的特征向量和临界点信息。
    *   `testset_exp.xlsx`: 包含测试集实验数据的全部温度标签。
    *   `mean_std.xlsx`: Z-score标准化的均值和标准差。
*   `model`: 包含训练好的模型参数文件。
*   `test`: 包含测试代码和测试结果。
    *   `draw.ipynb`: 测试代码，用于绘制测试集上指定物质的蒸气压曲线。
    *   `Thermodynamic_consistency_test.py`: 对测试集进行热力学一致性测试的代码。
    *   `model.py`: 模型结构的代码。