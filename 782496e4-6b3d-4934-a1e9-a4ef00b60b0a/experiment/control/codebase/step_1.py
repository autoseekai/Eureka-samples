import os
import numpy as np
import pandas as pd

def min_max_scaler(data):
    """
    对一维 numpy 数组进行最小-最大标准化。

    Args:
        data (np.ndarray): 需要标准化的输入数组。

    Returns:
        np.ndarray: 标准化后，值域在 [0, 1] 的数组。
    """
    min_val = np.min(data)
    max_val = np.max(data)
    # 避免除以零的情况
    if max_val == min_val:
        return np.zeros_like(data)
    return (data - min_val) / (max_val - min_val)

def generate_initial_data(n_samples, mean, cov, alpha, beta):
    """
    生成模拟实验所需的初始学生数据集。

    该函数通过从多维正态分布中抽样，生成学生的初始知识（K）和动机（M）水平。
    随后，对这些原始值进行最小-最大标准化，并根据给定的权重计算初始学业成就（A_pre）。

    Args:
        n_samples (int): 模拟的学生数量。
        mean (list or np.ndarray): 多维正态分布的均值向量。
        cov (list or np.ndarray): 多维正态分布的协方差矩阵。
        alpha (float): 知识（K）在计算学业成就时的权重。
        beta (float): 动机（M）在计算学业成就时的权重。

    Returns:
        pd.DataFrame: 包含学生ID、K、M、K_norm、M_norm 和 A_pre 的 DataFrame。
    """
    initial_attributes = np.random.multivariate_normal(mean, cov, n_samples)
    k_initial = initial_attributes[:, 0]
    m_initial = initial_attributes[:, 1]

    k_norm = min_max_scaler(k_initial)
    m_norm = min_max_scaler(m_initial)

    a_pre = alpha * k_norm + beta * m_norm

    student_ids = np.arange(n_samples)
    data = {
        'student_id': student_ids,
        'K': k_initial,
        'M': m_initial,
        'K_norm': k_norm,
        'M_norm': m_norm,
        'A_pre': a_pre
    }
    df = pd.DataFrame(data)
    return df

if __name__ == '__main__':
    N = 10000
    MU = [0, 0]
    SIGMA = [[1, 0.2], [0.2, 1]]
    ALPHA = 0.6
    BETA = 0.4

    DATA_DIR = "/work_dir/data"
    CODE_DIR = "/work_dir/codebase"
    OUTPUT_FILE = os.path.join(DATA_DIR, "initial_student_data.csv")

    for path in [DATA_DIR, CODE_DIR]:
        if not os.path.exists(path):
            os.makedirs(path)

    student_data_df = generate_initial_data(
        n_samples=N,
        mean=MU,
        cov=SIGMA,
        alpha=ALPHA,
        beta=BETA
    )

    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 1000)

    print("Generated Initial Student Data Overview:")
    print(student_data_df.head())
    print("\nData Description:")
    print(student_data_df.describe())

    student_data_df.to_csv(OUTPUT_FILE, index=False)

    print("\n" + "Initial student data successfully generated and saved to: " + OUTPUT_FILE)
