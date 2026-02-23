import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def create_effect_size_plot(data_path: str, output_path: str):
    """Loads effect size data and creates a line plot of Cohen's d vs. Time.

    Args:
        data_path (str): The path to the input CSV file ('effect_size_results.csv').
        output_path (str): The path to save the output PNG plot.
    """
    df_effect = pd.read_csv(data_path)

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(10, 6))

    sns.lineplot(
        data=df_effect,
        x='time',
        y='cohen_d',
        hue='scenario',
        marker='o',
        ax=ax
    )

    ax.set_title("Effect Size (Cohen's d) Over Time by Scenario", fontsize=16)
    ax.set_xlabel("Time Step", fontsize=12)
    ax.set_ylabel("Cohen's d", fontsize=12)
    ax.legend(title='Scenario')
    ax.grid(True)

    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Effect size plot saved to {output_path}")


def create_learning_trajectories_plot(data_path: str, output_path: str):
    """Loads simulation data and plots average learning trajectories for subgroups.

    Args:
        data_path (str): The path to the input CSV file ('simulation_data.csv').
        output_path (str): The path to save the output PNG plot.
    """
    df_sim = pd.read_csv(data_path)

    avg_scores = df_sim.groupby(['time', 'scenario', 'group'])['score'].mean().reset_index()
    avg_scores['subgroup'] = avg_scores['scenario'] + ' - ' + avg_scores['group']

    sns.set_theme(style="whitegrid")
    fig, ax = plt.subplots(figsize=(12, 8))

    sns.lineplot(
        data=avg_scores,
        x='time',
        y='score',
        hue='subgroup',
        style='scenario',
        markers=True,
        dashes=False,
        ax=ax
    )

    ax.set_title('Average Learning Trajectories by Subgroup', fontsize=16)
    ax.set_xlabel('Time Step', fontsize=12)
    ax.set_ylabel('Average Score', fontsize=12)
    ax.legend(title='Subgroup')
    ax.grid(True)

    fig.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close(fig)
    print(f"Learning trajectories plot saved to {output_path}")


def main():
    """Main function to orchestrate the visualization of simulation results."""
    DATA_DIR = "/work_dir/data"
    PLOTS_DIR = "/work_dir/plots"

    EFFECT_SIZE_FILE = os.path.join(DATA_DIR, "effect_size_results.csv")
    SIMULATION_DATA_FILE = os.path.join(DATA_DIR, "simulation_data.csv")

    EFFECT_SIZE_PLOT_FILE = os.path.join(PLOTS_DIR, "effect_size_over_time.png")
    TRAJECTORIES_PLOT_FILE = os.path.join(PLOTS_DIR, "learning_trajectories.png")

    os.makedirs(PLOTS_DIR, exist_ok=True)

    print("Step 5: Visualizing simulation results.")

    create_effect_size_plot(
        data_path=EFFECT_SIZE_FILE,
        output_path=EFFECT_SIZE_PLOT_FILE
    )

    create_learning_trajectories_plot(
        data_path=SIMULATION_DATA_FILE,
        output_path=TRAJECTORIES_PLOT_FILE
    )

    print("Visualization step complete.")


if __name__ == '__main__':
    main()
