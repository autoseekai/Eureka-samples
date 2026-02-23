import os
import pandas as pd
import numpy as np
import scipy.stats as stats
import statsmodels.api as sm
from statsmodels.formula.api import ols
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_dummy_data(file_path):
    """Generates and saves dummy intervention results data to a CSV file.

    This function creates a pandas DataFrame simulating experimental data with three
    conditions: 'Control', 'Generic Intervention', and 'Diagnostic-Matched'.
    The 'Gain_Score' for each group is drawn from a normal distribution with
    different means to ensure the subsequent statistical tests yield meaningful
    results. The data is then saved to the specified CSV file.

    Args:
        file_path (str): The full path to the output CSV file.
    """
    np.random.seed(42)
    n_per_group = 50
    
    participant_ids = range(1, n_per_group * 3 + 1)
    
    control_scores = np.random.normal(loc=5, scale=4, size=n_per_group)
    generic_scores = np.random.normal(loc=12, scale=4.5, size=n_per_group)
    matched_scores = np.random.normal(loc=18, scale=5, size=n_per_group)
    
    conditions = ['Control'] * n_per_group + \
                 ['Generic Intervention'] * n_per_group + \
                 ['Diagnostic-Matched'] * n_per_group
                 
    gain_scores = np.concatenate([control_scores, generic_scores, matched_scores])
    
    data = {
        'Participant_ID': participant_ids,
        'Intervention_Condition': conditions,
        'Gain_Score': gain_scores
    }
    
    df = pd.DataFrame(data)
    df.to_csv(file_path, index=False)

def calculate_cohens_d(group1, group2):
    """Calculates Cohen's d for two independent groups.

    Cohen's d is an effect size used to indicate the standardized difference
    between two means. It is calculated as the difference between the means
    divided by the pooled standard deviation.

    Args:
        group1 (pd.Series or np.ndarray): Data for the first group.
        group2 (pd.Series or np.ndarray): Data for the second group.

    Returns:
        float: The calculated Cohen's d value.
    """
    n1, n2 = len(group1), len(group2)
    s1, s2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
    
    pooled_std = np.sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))
    
    mean1, mean2 = np.mean(group1), np.mean(group2)
    
    d = (mean1 - mean2) / pooled_std
    return d

def get_significance_stars(p_value):
    """Converts a p-value into a string of significance stars.

    Args:
        p_value (float): The p-value from a statistical test.

    Returns:
        str: A string representing the significance level ('***', '**', '*', 'ns').
    """
    if p_value < 0.001:
        return '***'
    elif p_value < 0.01:
        return '**'
    elif p_value < 0.05:
        return '*'
    else:
        return 'ns'

def main():
    """Main function to execute the statistical analysis and visualization pipeline.

    This function orchestrates the entire process: setting up directories,
    generating dummy data, loading it, performing descriptive statistics, ANOVA,
    t-tests, calculating effect sizes, visualizing the results with a box plot,
    and saving all outputs to respective files.
    """
    data_dir = '/work_dir/data'
    plot_dir = '/work_dir/plots'
    code_dir = '/work_dir/codebase'
    
    os.makedirs(data_dir, exist_ok=True)
    os.makedirs(plot_dir, exist_ok=True)
    os.makedirs(code_dir, exist_ok=True)
    
    input_csv_path = os.path.join(data_dir, 'intervention_results.csv')
    output_txt_path = os.path.join(data_dir, 'statistical_analysis_results.txt')
    output_png_path = os.path.join(plot_dir, 'figure2_gain_scores.png')

    create_dummy_data(input_csv_path)
    
    df = pd.read_csv(input_csv_path)
    
    results_string = """Statistical Analysis of Intervention Gain Scores\n"""
    results_string += "==================================================\n\n"
    
    print("--- Descriptive Statistics ---")
    desc_stats = df.groupby('Intervention_Condition')['Gain_Score'].agg(['mean', 'std', 'count'])
    print(desc_stats)
    results_string += "1. Descriptive Statistics:\n"
    results_string += desc_stats.to_string() + "\n\n"
    
    print("\n--- One-Way ANOVA ---")
    model = ols('Gain_Score ~ C(Intervention_Condition)', data=df).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(anova_table)
    results_string += "2. One-Way ANOVA Results:\n"
    results_string += anova_table.to_string() + "\n\n"
    
    group_dm = df[df['Intervention_Condition'] == 'Diagnostic-Matched']['Gain_Score']
    group_gi = df[df['Intervention_Condition'] == 'Generic Intervention']['Gain_Score']
    group_c = df[df['Intervention_Condition'] == 'Control']['Gain_Score']
    
    print("\n--- Independent T-Tests ---")
    results_string += "3. Independent Samples T-Tests:\n"
    
    ttest_dm_vs_gi = stats.ttest_ind(group_dm, group_gi)
    print("Diagnostic-Matched vs. Generic Intervention: t=" + str(ttest_dm_vs_gi.statistic) + ", p=" + str(ttest_dm_vs_gi.pvalue))
    results_string += "- Diagnostic-Matched vs. Generic Intervention: t=" + str(ttest_dm_vs_gi.statistic) + ", p=" + str(ttest_dm_vs_gi.pvalue) + "\n"
    
    ttest_dm_vs_c = stats.ttest_ind(group_dm, group_c)
    print("Diagnostic-Matched vs. Control: t=" + str(ttest_dm_vs_c.statistic) + ", p=" + str(ttest_dm_vs_c.pvalue))
    results_string += "- Diagnostic-Matched vs. Control: t=" + str(ttest_dm_vs_c.statistic) + ", p=" + str(ttest_dm_vs_c.pvalue) + "\n\n"
    
    print("\n--- Cohen's d Effect Size ---")
    results_string += "4. Cohen's d Effect Size:\n"
    
    cohen_d_dm_vs_gi = calculate_cohens_d(group_dm, group_gi)
    print("Diagnostic-Matched vs. Generic Intervention: d=" + str(cohen_d_dm_vs_gi))
    results_string += "- Diagnostic-Matched vs. Generic Intervention: d=" + str(cohen_d_dm_vs_gi) + "\n"
    
    cohen_d_dm_vs_c = calculate_cohens_d(group_dm, group_c)
    print("Diagnostic-Matched vs. Control: d=" + str(cohen_d_dm_vs_c))
    results_string += "- Diagnostic-Matched vs. Control: d=" + str(cohen_d_dm_vs_c) + "\n"
    
    with open(output_txt_path, 'w') as f:
        f.write(results_string)
    print("\nStatistical results saved to " + output_txt_path)

    matplotlib.rcParams['text.usetex'] = False
    fig, ax = plt.subplots(figsize=(10, 7))
    
    group_order = ['Control', 'Generic Intervention', 'Diagnostic-Matched']
    data_to_plot = [group_c, group_gi, group_dm]
    
    ax.boxplot(data_to_plot, labels=group_order, patch_artist=True)
    
    ax.set_title('Comparison of Gain Scores Across Intervention Conditions')
    ax.set_xlabel('Intervention Condition')
    ax.set_ylabel('Gain Score')
    ax.tick_params(axis='x', rotation=15)
    
    y_max = df['Gain_Score'].max()
    y_range = df['Gain_Score'].max() - df['Gain_Score'].min()
    bar_height_step = y_range * 0.1
    
    comparisons = [
        (1, 3, ttest_dm_vs_c.pvalue), 
        (2, 3, ttest_dm_vs_gi.pvalue)
    ]
    
    bar_y_start = y_max + bar_height_step * 0.5
    
    for i, (x1, x2, p) in enumerate(comparisons):
        if p < 0.05:
            y = bar_y_start + i * bar_height_step
            h = bar_height_step * 0.2
            ax.plot([x1, x1, x2, x2], [y, y + h, y + h, y], lw=1.5, c='black')
            ax.text((x1 + x2) * 0.5, y + h, get_significance_stars(p), ha='center', va='bottom', color='black', fontsize=14)

    ax.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(output_png_path, dpi=300)
    print("Plot saved to " + output_png_path)

if __name__ == '__main__':
    main()
