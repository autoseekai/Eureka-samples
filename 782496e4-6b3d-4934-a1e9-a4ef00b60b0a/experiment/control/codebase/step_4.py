import pandas as pd
import numpy as np
import os

def run_intervention_simulation():
    """执行教育干预模拟，计算干预后分数并保存结果。

    该函数执行以下步骤：
    1.  加载诊断数据和原始数据。
    2.  获取 K 和 M 的全局最小/最大值用于标准化。
    3.  定义干预模型参数。
    4.  将低成就学生随机分配到五个实验组。
    5.  根据学生所在组和诊断类型，应用干预模型计算 K_post 和 M_post。
    6.  对干预后分数进行标准化。
    7.  计算干预后学业成就 A_post 和成就增益 Gain_Score。
    8.  将结果保存到 CSV 文件。
    """
    # 定义文件路径
    diagnosed_data_path = '/work_dir/data/diagnosed_student_data.csv'
    initial_data_path = '/work_dir/data/initial_student_data.csv'
    output_path = '/work_dir/data/intervention_results.csv'

    # 确保输出目录存在
    output_dir = os.path.dirname(output_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # 1. 加载数据
    diagnosed_df = pd.read_csv(diagnosed_data_path)
    initial_df = pd.read_csv(initial_data_path)

    # 2. 从 initial_student_data.csv 获取全局 K 和 M 的最小-最大值
    k_min = initial_df['K'].min()
    k_max = initial_df['K'].max()
    m_min = initial_df['M'].min()
    m_max = initial_df['M'].max()

    # 3. 定义干预参数
    delta_k = 0.2
    gamma = 1.0
    delta_m = 0.2
    delta_k_gen = 0.05
    delta_m_gen = 0.05

    # 4. 筛选出低成就学生
    low_achievers_mask = diagnosed_df['Diagnosis'].notna()
    low_achiever_indices = diagnosed_df[low_achievers_mask].index.to_numpy()

    # 5. 将低成就学生随机且均等地分配到五个实验组
    np.random.seed(42)  # for reproducibility
    np.random.shuffle(low_achiever_indices)
    groups = ['Control', 'General', 'Skill', 'Motivation', 'Matched']
    group_assignments = np.array_split(low_achiever_indices, len(groups))

    diagnosed_df['Group'] = pd.NA
    for i, group_name in enumerate(groups):
        diagnosed_df.loc[group_assignments[i], 'Group'] = group_name

    # 6. 初始化 K_post 和 M_post 列
    diagnosed_df['K_post'] = diagnosed_df['K']
    diagnosed_df['M_post'] = diagnosed_df['M']

    # 7. 遍历每个低成就学生，根据其所在的 'Group' 和 'Diagnosis' 应用干预模型
    # 使用向量化操作提高效率

    # General Intervention Group
    general_mask = diagnosed_df['Group'] == 'General'
    diagnosed_df.loc[general_mask, 'K_post'] += delta_k_gen
    diagnosed_df.loc[general_mask, 'M_post'] += delta_m_gen

    # Skill-only Intervention Group
    skill_mask = diagnosed_df['Group'] == 'Skill'
    diagnosed_df.loc[skill_mask, 'K_post'] += delta_k + gamma * diagnosed_df.loc[skill_mask, 'M']

    # Motivation-only Intervention Group
    motivation_mask = diagnosed_df['Group'] == 'Motivation'
    diagnosed_df.loc[motivation_mask, 'M_post'] += delta_m

    # Matched Intervention Group
    matched_group_mask = diagnosed_df['Group'] == 'Matched'
    k_deficit_mask = matched_group_mask & (diagnosed_df['Diagnosis'] == 'K-deficit')
    m_deficit_mask = matched_group_mask & (diagnosed_df['Diagnosis'] == 'M-deficit')
    both_deficit_mask = matched_group_mask & (diagnosed_df['Diagnosis'] == 'Both-deficit')

    # K-deficit in Matched group
    diagnosed_df.loc[k_deficit_mask, 'K_post'] += delta_k + gamma * diagnosed_df.loc[k_deficit_mask, 'M']

    # M-deficit in Matched group
    diagnosed_df.loc[m_deficit_mask, 'M_post'] += delta_m

    # Both-deficit in Matched group
    diagnosed_df.loc[both_deficit_mask, 'K_post'] += delta_k + gamma * diagnosed_df.loc[both_deficit_mask, 'M']
    diagnosed_df.loc[both_deficit_mask, 'M_post'] += delta_m

    # 8. 对 K_post 和 M_post 进行最小-最大标准化
    k_range = k_max - k_min
    m_range = m_max - m_min

    diagnosed_df['K_post_norm'] = ((diagnosed_df['K_post'] - k_min) / k_range).clip(0, 1)
    diagnosed_df['M_post_norm'] = ((diagnosed_df['M_post'] - m_min) / m_range).clip(0, 1)

    # 9. 计算干预后学业成就 A_post
    diagnosed_df['A_post'] = 0.5 * diagnosed_df['K_post_norm'] + 0.5 * diagnosed_df['M_post_norm']

    # 10. 计算成就增益 Gain_Score
    diagnosed_df['Gain_Score'] = diagnosed_df['A_post'] - diagnosed_df['A_pre']

    # 11. 保存更新后的 DataFrame
    diagnosed_df.to_csv(output_path, index=False)

    # 12. 打印确认信息和结果预览
    print(f"Intervention results successfully saved to {output_path}")
    print("\nPreview of the final data:")
    print(diagnosed_df.head())

if __name__ == '__main__':
    run_intervention_simulation()
