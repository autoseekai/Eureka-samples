import os
import pandas as pd
import numpy as np

def create_directories_if_not_exist(path):
    """确保给定文件路径的目录存在。

    Args:
        path (str): 文件的完整路径。
    """
    dir_name = os.path.dirname(path)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def load_data(file_path):
    """从CSV文件加载数据到pandas DataFrame。

    Args:
        file_path (str): 输入的CSV文件路径。

    Returns:
        pd.DataFrame: 加载后的数据框。
    """
    print("Loading data from: " + file_path)
    return pd.read_csv(file_path)

def filter_low_achievers(df, column_name, percentile_threshold):
    """根据指定列的百分位数筛选数据框。

    Args:
        df (pd.DataFrame): 原始数据框。
        column_name (str): 用于筛选的列名。
        percentile_threshold (float): 用于定义筛选边界的百分位数 (0到1之间)。

    Returns:
        tuple[pd.DataFrame, float]: 一个包含筛选后数据框和阈值的元组。
    """
    threshold_value = df[column_name].quantile(percentile_threshold)
    print("Calculated " + str(percentile_threshold * 100) + "th percentile for '" + column_name + "' is: " + str(threshold_value))
    low_achievers_df = df[df[column_name] <= threshold_value].copy()
    return low_achievers_df, threshold_value

def calculate_and_print_stats(df, columns):
    """计算并打印指定列的均值和标准差。

    Args:
        df (pd.DataFrame): 数据框。
        columns (list): 需要计算统计数据的列名列表。

    Returns:
        dict: 包含均值和标准差的字典。
    """
    stats = {}
    print("\n--- Statistics for Low-Achieving Students ---")
    for col in columns:
        mean_val = df[col].mean()
        std_val = df[col].std()
        stats[col] = {'mean': mean_val, 'std': std_val}
        print("Feature '" + col + "':")
        print("  Mean: " + str(mean_val))
        print("  Standard Deviation: " + str(std_val))
    print("--------------------------------------------\n")
    return stats

def diagnose_student(row, k_mean, m_mean):
    """根据学生的知识和动机水平进行诊断分类。

    Args:
        row (pd.Series): 代表单个学生数据的一行。
        k_mean (float): 低成就学生群体的K_norm均值。
        m_mean (float): 低成就学生群体的M_norm均值。

    Returns:
        str: 学生的诊断分类结果。
    """
    is_k_below_mean = row['K_norm'] < k_mean
    is_m_below_mean = row['M_norm'] < m_mean

    if is_k_below_mean and not is_m_below_mean:
        return "知识短板型"
    elif is_m_below_mean and not is_k_below_mean:
        return "动机短板型"
    else:
        return "混合短板型"

def save_data(df, file_path):
    """将DataFrame保存到CSV文件，不包含索引。

    Args:
        df (pd.DataFrame): 待保存的数据框。
        file_path (str): 输出的CSV文件路径。
    """
    create_directories_if_not_exist(file_path)
    df.to_csv(file_path, index=False)
    print("Successfully saved updated data to: " + file_path)

def main():
    """主执行函数，完成学生诊断分类任务。"""
    input_path = '/work_dir/data/initial_student_data.csv'
    output_path = '/work_dir/data/diagnosed_student_data.csv'

    # 1. 读取数据
    student_df = load_data(input_path)

    # 2. 筛选低成就学生
    low_achievers_df, _ = filter_low_achievers(student_df, 'A_pre', 0.2)

    # 3. 计算并打印低成就学生群体的统计数据
    stats = calculate_and_print_stats(low_achievers_df, ['K_norm', 'M_norm'])
    k_norm_mean = stats['K_norm']['mean']
    m_norm_mean = stats['M_norm']['mean']

    # 4. & 5. 对低成就学生进行诊断并更新DataFrame
    student_df['Diagnosis'] = np.nan
    diagnosis_results = low_achievers_df.apply(
        lambda row: diagnose_student(row, k_norm_mean, m_norm_mean), axis=1
    )
    student_df.loc[low_achievers_df.index, 'Diagnosis'] = diagnosis_results

    # 6. 保存更新后的DataFrame
    save_data(student_df, output_path)

    # 7. 打印新DataFrame的前几行
    print("\n--- Head of the Diagnosed Student DataFrame ---")
    print(student_df.head())
    print("---------------------------------------------")

if __name__ == '__main__':
    main()
