import numpy as np
import pandas as pd
from scipy.stats import truncnorm
import os


def get_truncated_normal(mean=0, sd=1, low=0, upp=10):
    """Creates a truncated normal distribution object."""
    return truncnorm(
        (low - mean) / sd, (upp - mean) / sd, loc=mean, scale=sd
    )


def generate_population(n, score_dist, lr_dist):
    """Generates the initial student population.

    Args:
        n (int): The number of students in the population.
        score_dist (scipy.stats.rv_continuous): Distribution for initial scores.
        lr_dist (numpy.random.normal): Distribution for baseline learning rates.

    Returns:
        pandas.DataFrame: A DataFrame containing the initial population, with columns
                          ['student_id', 'initial_score', 'lr_base'].
    """
    student_ids = np.arange(n)
    initial_scores = score_dist.rvs(n)
    lr_bases = lr_dist.rvs(n)
    
    population_df = pd.DataFrame({
        'student_id': student_ids,
        'initial_score': initial_scores,
        'lr_base': lr_bases
    })
    return population_df


def calculate_effective_lr(t, lr_base, is_treated, boost, decay_rate):
    """Calculates the effective learning rate for a student at a given time step.

    Args:
        t (int): The current time step (starting from 1).
        lr_base (float): The student's baseline learning rate.
        is_treated (bool): True if the student is in the treatment group.
        boost (float): The initial boost to the learning rate for treated students.
        decay_rate (float): The rate at which the boost effect decays.

    Returns:
        float: The effective learning rate for the current time step.
    """
    if is_treated:
        return lr_base + boost * np.exp(-decay_rate * (t - 1))
    else:
        return lr_base


def update_score(current_score, effective_lr, mastery_ceiling):
    """Updates a student's score based on the logistic growth equation.

    Args:
        current_score (float): The student's score at the current time step.
        effective_lr (float): The student's effective learning rate for this time step.
        mastery_ceiling (float): The maximum possible score.

    Returns:
        float: The updated score for the next time step.
    """
    return current_score + effective_lr * (mastery_ceiling - current_score)


def run_simulation(initial_population_df, group_assignments, t_steps, mastery_ceiling, boost, decay_rate):
    """Runs the full simulation over T time steps.

    Args:
        initial_population_df (pandas.DataFrame): DataFrame with initial student data.
        group_assignments (dict): A dictionary mapping student_id to 'treatment' or 'control'.
        t_steps (int): The total number of time steps for the simulation.
        mastery_ceiling (float): The maximum possible score.
        boost (float): The intervention boost parameter.
        decay_rate (float): The intervention decay rate parameter.

    Returns:
        pandas.DataFrame: A DataFrame containing the score trajectory for each student over time.
    """
    n_students = len(initial_population_df)
    scores = np.zeros((n_students, t_steps + 1))
    scores[:, 0] = initial_population_df['initial_score']

    for t in range(1, t_steps + 1):
        for i in range(n_students):
            student_id = initial_population_df.loc[i, 'student_id']
            lr_base = initial_population_df.loc[i, 'lr_base']
            is_treated = (group_assignments.get(student_id) == 'treatment')
            
            effective_lr = calculate_effective_lr(t, lr_base, is_treated, boost, decay_rate)
            
            current_score = scores[i, t - 1]
            new_score = update_score(current_score, effective_lr, mastery_ceiling)
            scores[i, t] = new_score

    time_columns = ['t_' + str(i) for i in range(t_steps + 1)]
    results_df = pd.DataFrame(scores, columns=time_columns)
    final_df = pd.concat([initial_population_df, results_df], axis=1)
    
    return final_df


if __name__ == '__main__':
    # This block is for demonstration and verification of the functions.
    # It does not produce any output files in this step.

    # --- Confirmed Simulation Parameters ---
    N = 1000
    T = 20
    MASTERY_CEILING = 100.0
    
    # Initial Score Distribution
    SCORE_MEAN = 50.0
    SCORE_STD = 15.0
    
    # Baseline Learning Rate Distribution
    LR_MEAN = 0.05
    LR_STD = 0.01
    
    # Intervention Dynamics
    BOOST = 0.15
    DECAY_RATE = 0.25

    # --- Setup Distributions ---
    score_distribution = get_truncated_normal(mean=SCORE_MEAN, sd=SCORE_STD, low=0, upp=MASTERY_CEILING)
    lr_distribution = np.random.normal(loc=LR_MEAN, scale=LR_STD, size=N)
    # A simple wrapper for the numpy array to make the interface consistent for generate_population
    class NormalWrapper:
        def __init__(self, data):
            self.data = data
            self.index = 0
        def rvs(self, size):
            sample = self.data[self.index:self.index + size]
            self.index += size
            return sample

    lr_dist_wrapped = NormalWrapper(lr_distribution)

    # --- Generate Population ---
    population = generate_population(N, score_distribution, lr_dist_wrapped)
    print("Generated Population Head:")
    print(population.head())
    print("\nPopulation Description:")
    print(population.describe())

    # --- Assign Groups (Placeholder) ---
    # In a real experiment, this would be based on a condition (e.g., low-achievers).
    # Here, we just assign the first half to treatment for demonstration.
    assignments = {i: 'treatment' if i < N / 2 else 'control' for i in range(N)}

    # --- Run Simulation ---
    simulation_results = run_simulation(
        initial_population_df=population,
        group_assignments=assignments,
        t_steps=T,
        mastery_ceiling=MASTERY_CEILING,
        boost=BOOST,
        decay_rate=DECAY_RATE
    )

    print("\nSimulation Results Head:")
    print(simulation_results.head())
    
    # --- Save the code file ---
    # The framework handles saving the code to the specified path.
    # This part is illustrative of where the file is intended to be saved.
    file_path = "/work_dir/codebase/step_2.py"
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    # The file content is written by the calling framework, not this script.
    print("\nCode structure prepared for saving to " + file_path)
