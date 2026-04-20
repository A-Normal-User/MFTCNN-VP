## Language Selection
- [English](README.md)
- [Chinese](README_CN.md)

## Pre-print Paper
The pre-print paper describing the MFTCNN-VP model can be found on ChemRxiv: [Multi-Fidelity Thermodynamically Consistent Neural Networks for Vapor Pressure Prediction of Petroleum Hydrocarbons](https://chemrxiv.org/doi/full/10.26434/chemrxiv.15002200/v1).

BiBTeX entry for citation:
```bibtex
@article{Li2026MFTCNNVP,
    author = {Xurui Li  and Zhiguo Gan  and Jiaming Zhang  and Hongxi Zeng  and Zheng Liu  and Diannan Lu },
    title = {Multi-Fidelity Thermodynamically Consistent Neural Networks for Vapor Pressure Prediction of Petroleum Hydrocarbons},
    journal = {ChemRxiv},
    volume = {2026},
    number = {0420},
    pages = {},
    year = {2026},
    doi = {10.26434/chemrxiv.15002200/v1},
    URL = {https://chemrxiv.org/doi/abs/10.26434/chemrxiv.15002200/v1},
    eprint = {https://chemrxiv.org/doi/pdf/10.26434/chemrxiv.15002200/v1}
}
```

## Introduction
In chemical research, industrial applications, and environmental management, vapor pressure is a vital physical property. It directly affects the volatility, boiling point, and thermodynamic behavior of substances. The accurate prediction of vapor pressure is essential for designing chemical processes, evaluating environmental risks, and developing new materials. However, traditional vapor pressure prediction methods often rely on extensive experimental data and complex theoretical models, making it difficult for them to adapt to diverse chemical spaces.

To address this issue, we propose a Multi-Fidelity Thermodynamically Consistent Neural Network (MFTCNN-VP) to predict the vapor pressure of compounds. This model integrates multi-fidelity learning with thermodynamic consistency constraints. It can ensure that the predicted results obey thermodynamic laws while maintaining high prediction accuracy.

We evaluated the performance of MFTCNN-VP on a test set containing 40 new hydrocarbon compounds and compared it with existing vapor pressure prediction methods. The results indicate that MFTCNN-VP outperforms traditional methods on the test set, demonstrating higher accuracy and better thermodynamic consistency.

## Usage of MFTCNN-VP
1. Clone the repository
    ```bash
    git clone https://github.com/A-Normal-User/MFTCNN-VP.git
    cd MFTCNN-VP
    ```
2. Install dependencies
    ```bash
    pip3 install -r requirements.txt
    ```
3. Run the thermodynamic consistency test code on the test set
    ```bash
    python3 test/Thermodynamic_consistency_test.py
    ```
4. Run the code to plot the vapor pressure curve for a specified substance in the test set
    ```bash
    jupyter notebook test/draw.ipynb
    ```

## Performance Comparison on the Test Set
| Usage             | $R^2$           | RMSE(Pa)          | MAE(Pa)         | AARD(\%)        | Source          |
|---|---|---|---|---|---|
| MFTCNN-VP         | **0.9965** | **2,704.58** | **867.08** | **2.0936** | |
| MFTCNN-VP (prior) | 0.9304          | 1,1978.20         | 7,891.52        | 18.9577         | |
| GRAPPA            | 0.9558          | 9,959.35          | 4,919.18        | 10.831          | [GRAPPA](https://github.com/marco-hoffmann/GRAPPA) |
| mfp-sum Wagner EE | 0.9563          | 9,825.88          | 6,474.98        | 14.249          | [chemprop_VP](https://github.com/fatcat0322/chemprop_VP) |


## File Descriptions
*   `database`: Contains all feature vectors and temperature labels for the test set.
    *   `HC459_testset.csv`: Contains the feature vectors and critical point information of the test set.
    *   `testset_exp.xlsx`: Contains all temperature labels from the experimental data of the test set.
    *   `mean_std.xlsx`: The mean and standard deviation used for Z-score standardization.
*   `model`: Contains the trained model parameter files.
*   `test`: Contains the test code and test results.
    *   `draw.ipynb`: Test code used to plot the vapor pressure curve for a specified substance in the test set.
    *   `Thermodynamic_consistency_test.py`: Code for conducting the thermodynamic consistency test on the test set.
    *   `model.py`: Code for the model structure.