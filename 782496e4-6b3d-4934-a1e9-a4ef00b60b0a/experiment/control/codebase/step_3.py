import os
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

def generate_heterogeneity_plot(csv_path, plot_path):
    """加载学生数据，生成并保存在知识与动机潜在空间中的异质性分布散点图。

    该函数首先加载所有学生的数据作为背景，然后在其上突出显示被诊断为
    低成就的学生。低成就学生根据其诊断类别（'知识短板', '动机短板', '混合短板'）
    使用不同的颜色和标记进行区分，以便于观察他们在二维潜在空间中的分布模式。

    Args:
        csv_path (str): 包含学生数据的 CSV 文件路径。
        plot_path (str): 生成的图表要保存的 PNG 文件路径。

    Returns:
        None
    """
    try:
        matplotlib.rcParams['font.sans-serif'] = ['SimHei']
        matplotlib.rcParams['axes.unicode_minus'] = False
    except Exception:
        print("警告：未找到 'SimHei' 字体，中文标签可能无法正常显示。请安装该字体或更换为其他支持中文的字体。")

    df = pd.read_csv(csv_path)

    diagnosed_df = df[df['Diagnosis'].notna()].copy()

    fig, ax = plt.subplots(figsize=(12, 9))

    ax.scatter(
        x=df['K_norm'],
        y=df['M_norm'],
        color='#D3D3D3',
        s=15,
        alpha=0.4,
        label='全部学生'
    )

    palette = {
        '知识短板': '#1f77b4',
        '动机短板': '#ff7f0e',
        '混合短板': '#2ca02c'
    }

    markers = {
        '知识短板': 'o',
        '动机短板': 'X',
        '混合短板': 's'
    }

    sns.scatterplot(
        data=diagnosed_df,
        x='K_norm',
        y='M_norm',
        hue='Diagnosis',
        style='Diagnosis',
        palette=palette,
        markers=markers,
        s=100,
        ax=ax,
        zorder=3
    )

    ax.set_title('学生在知识与动机潜在空间中的异质性分布', fontsize=18, fontweight='bold')
    ax.set_xlabel('知识潜在能力 (K_norm)', fontsize=14)
    ax.set_ylabel('动机潜在水平 (M_norm)', fontsize=14)

    legend = ax.get_legend()
    legend.set_title('诊断类别')
    for text in legend.get_texts():
        text.set_fontsize(12)
    legend.get_title().set_fontsize(14)

    plt.tight_layout()

    output_dir = os.path.dirname(plot_path)
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    fig.savefig(plot_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    plot_filename = os.path.basename(plot_path)
    print('图表 ' + plot_filename + ' 已成功保存，展示了学生在知识与动机空间的分布情况。')

if __name__ == '__main__':
    """脚本执行入口。

    定义数据输入和图表输出路径，并调用绘图函数生成可视化结果。
    """
    INPUT_CSV_PATH = '/work_dir/data/diagnosed_student_data.csv'
    OUTPUT_PLOT_PATH = '/work_dir/plots/figure1_heterogeneity.png'

    generate_heterogeneity_plot(csv_path=INPUT_CSV_PATH, plot_path=OUTPUT_PLOT_PATH)
