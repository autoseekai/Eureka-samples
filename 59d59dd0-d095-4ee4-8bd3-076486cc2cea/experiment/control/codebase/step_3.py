import os
import numpy as np
import pandas as pd
from scipy.stats import truncnorm

def generate_initial_population(n_students, score_mean, score_std, score_min, score_max, lr_mean, lr_std, seed):
    """Generates the initial population of students.

    Args:
        n_students (int): The number of students in the population.
        score_mean (float): The mean of the initial score distribution.
        score_std (float): The standard deviation of the initial score distribution.
        score_min (float): The minimum possible initial score.
        score_max (float): The maximum possible initial score.
        lr_mean (float): The mean of the baseline learning rate distribution.
        lr_std (float): The standard deviation of the baseline learning rate distribution.
        seed (int): The random seed for reproducibility.

    Returns:
        pd.DataFrame: A DataFrame containing the initial state of the population,
                      with columns 'student_id', 'initial_score', and 'lr_base'.
    """
    np.random.seed(seed)

    # Define bounds for the truncated normal distribution
    a = (score_min - score_mean) / score_std
    b = (score_max - score_mean) / score_std

    initial_scores = truncnorm.rvs(
        a, b, loc=score_mean, scale=score_std, size=n_students
    )

    learning_rates = np.random.normal(loc=lr_mean, scale=lr_std, size=n_students)
    # Ensure learning rates are non-negative
    learning_rates[learning_rates < 0] = 0

    population_df = pd.DataFrame({
        'student_id': range(n_students),
        'initial_score': initial_scores,
        'lr_base': learning_rates
    })

    return population_df

def run_simulation(initial_df, t_steps, mastery_ceiling, boost, decay_rate):
    """Runs the learning simulation over a given number of time steps.

    The initial_df must contain 'student_id', 'initial_score', 'lr_base', and 'group' columns.

    Args:
        initial_df (pd.DataFrame): DataFrame with the initial state and group assignments.
        t_steps (int): The number of time steps to simulate.
        mastery_ceiling (float): The maximum possible score (100%).
        boost (float): The initial boost applied to the learning rate for the treatment group.
        decay_rate (float): The rate at which the boost effect decays over time.

    Returns:
        pd.DataFrame: A long-format DataFrame with simulation results, including
                      'student_id', 'time', 'score', and 'group'.
    """
    records = []

    # Initial state at t=0
    scores = initial_df['initial_score'].values.copy()
    lr_base = initial_df['lr_base'].values
    is_treatment = (initial_df['group'] == 'Treatment').values

    # Store t=0 results
    for i in range(len(initial_df)):
        records.append({
            'student_id': initial_df['student_id'].iloc[i],
            'time': 0,
            'score': scores[i],
            'group': initial_df['group'].iloc[i]
        })

    # Simulate for t > 0
    for t in range(1, t_steps + 1):
        # Calculate effective learning rate for all students
        time_decay_factor = np.exp(-decay_rate * (t - 1))
        treatment_effect = boost * time_decay_factor
        effective_lr = lr_base + np.where(is_treatment, treatment_effect, 0)

        # Update scores
        scores += effective_lr * (mastery_ceiling - scores)
        scores = np.clip(scores, 0, mastery_ceiling)

        # Store results for the current time step
        for i in range(len(initial_df)):
            records.append({
                'student_id': initial_df['student_id'].iloc[i],
                'time': t,
                'score': scores[i],
                'group': initial_df['group'].iloc[i]
            })

    return pd.DataFrame(records)

if __name__ == '__main__':
    # 1. Regenerate Initial Population
    N_STUDENTS = 1000
    T_STEPS = 20
    MASTERY_CEILING = 100.0
    SCORE_MEAN = 50.0
    SCORE_STD = 15.0
    LR_BASE_MEAN = 0.05
    LR_BASE_STD = 0.01
    BOOST = 0.15
    DECAY_RATE = 0.25
    SEED = 42

    initial_population = generate_initial_population(
        n_students=N_STUDENTS,
        score_mean=SCORE_MEAN,
        score_std=SCORE_STD,
        score_min=0,
        score_max=MASTERY_CEILING,
        lr_mean=LR_BASE_MEAN,
        lr_std=LR_BASE_STD,
        seed=SEED
    )

    # 2. Execute Scenario A (Targeted Intervention)
    low_achiever_threshold = initial_population['initial_score'].quantile(0.25)
    
    pop_scenario_a = initial_population.copy()
    pop_scenario_a['group'] = np.where(
        pop_scenario_a['initial_score'] <= low_achiever_threshold,
        'Treatment',
        'Control'
    )

    results_targeted = run_simulation(
        initial_df=pop_scenario_a,
        t_steps=T_STEPS,
        mastery_ceiling=MASTERY_CEILING,
        boost=BOOST,
        decay_rate=DECAY_RATE
    )
    results_targeted['scenario'] = 'Targeted'

    # 3. Execute Scenario B (General Population RCT)
    num_treatment_a = (pop_scenario_a['group'] == 'Treatment').sum()
    
    pop_scenario_b = initial_population.copy()
    
    # Randomly assign the same number of students to treatment
    treatment_ids = pop_scenario_b.sample(
        n=num_treatment_a, random_state=123
    ).index

    pop_scenario_b['group'] = 'Control'
    pop_scenario_b.loc[treatment_ids, 'group'] = 'Treatment'

    results_general = run_simulation(
        initial_df=pop_scenario_b,
        t_steps=T_STEPS,
        mastery_ceiling=MASTERY_CEILING,
        boost=BOOST,
        decay_rate=DECAY_RATE
    )
    results_general['scenario'] = 'General Population'

    # 4. Combine and Save
    combined_results = pd.concat([results_targeted, results_general], ignore_index=True)

    output_dir = '/work_dir/data/'
    output_path = os.path.join(output_dir, 'simulation_data.csv')

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    combined_results.to_csv(output_path, index=False)

    print('--- Combined Simulation Data ---')
    print(combined_results.head())
    print('\nShape of the combined DataFrame: ' + str(combined_results.shape))
