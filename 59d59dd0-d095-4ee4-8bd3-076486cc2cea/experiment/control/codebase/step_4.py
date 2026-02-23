import pandas as pd
import numpy as np
import os

def cohens_d(treatment_scores, control_scores):
    """
    Calculates Cohen's d for independent samples.

    Cohen's d is an effect size used to indicate the standardised difference
    between two means. It is defined as the difference between two means
    divided by a pooled standard deviation for the data.

    Args:
        treatment_scores (pd.Series or np.array): Scores for the treatment group.
        control_scores (pd.Series or np.array): Scores for the control group.

    Returns:
        float: The calculated Cohen's d value. Returns 0.0 if the pooled
               standard deviation is zero, and np.nan if a group is empty.
    """
    n_treatment = len(treatment_scores)
    n_control = len(control_scores)

    if n_treatment == 0 or n_control == 0:
        return np.nan

    mean_treatment = np.mean(treatment_scores)
    mean_control = np.mean(control_scores)

    # ddof=1 for sample standard deviation
    std_treatment = np.std(treatment_scores, ddof=1)
    std_control = np.std(control_scores, ddof=1)

    # Handle cases where std is NaN (e.g., only one sample in a group)
    if np.isnan(std_treatment) or np.isnan(std_control):
        return np.nan

    # Calculate pooled standard deviation
    # The denominator for the pooled standard deviation is n_treatment + n_control - 2
    denominator = n_treatment + n_control - 2
    if denominator <= 0:
        return np.nan

    pooled_std = np.sqrt(
        ((n_treatment - 1) * std_treatment**2 + (n_control - 1) * std_control**2) / denominator
    )

    if pooled_std == 0:
        return 0.0

    d = (mean_treatment - mean_control) / pooled_std
    return d

def analyze_effect_sizes(data_path, output_path):
    """
    Loads simulation data, calculates Cohen's d for each time step and scenario,
    saves the results, and prints a verification summary.

    Args:
        data_path (str): The path to the input CSV file ('simulation_data.csv').
        output_path (str): The path to save the resulting effect size CSV file.
    """
    df = pd.read_csv(data_path)

    def calculate_d_for_group(group):
        treatment = group[group['group'] == 'Treatment']['score']
        control = group[group['group'] == 'Control']['score']
        return cohens_d(treatment, control)

    effect_sizes = df.groupby(['scenario', 'time_step']).apply(calculate_d_for_group)

    effect_size_df = effect_sizes.reset_index(name='cohens_d')

    effect_size_df.to_csv(output_path, index=False)
    print("Effect size data saved to " + output_path)
    print("\n--- Verification of Effect Sizes ---")

    scenarios = effect_size_df['scenario'].unique()
    for scenario in scenarios:
        scenario_df = effect_size_df[effect_size_df['scenario'] == scenario]
        if not scenario_df.empty:
            max_d_row = scenario_df.loc[scenario_df['cohens_d'].idxmax()]
            max_d = max_d_row['cohens_d']
            time_step = max_d_row['time_step']
            print("Scenario '" + scenario + "': Max Cohen's d = " + str(max_d) + " at time step " + str(int(time_step)))
        else:
            print("No data found for scenario: " + scenario)

if __name__ == '__main__':
    input_file_path = '/work_dir/data/simulation_data.csv'
    output_file_path = '/work_dir/data/effect_size_results.csv'

    os.makedirs('/work_dir/data', exist_ok=True)

    analyze_effect_sizes(input_file_path, output_file_path)
