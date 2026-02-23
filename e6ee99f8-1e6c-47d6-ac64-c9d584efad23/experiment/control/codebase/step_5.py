import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import glob
import os
from datetime import datetime
from lifelines import KaplanMeierFitter

DATA_DIR = '/work_dir/data'
PLOT_DIR = '/work_dir/plots'


def create_correlation_heatmap():
    """Creates and saves a correlation matrix heatmap.

    This function visualizes the relationships among demographic attributes,
    investment choices, and transaction behaviors.
    """
    print("Step 5: Creating correlation matrix heatmap...")
    try:
        investors_df = pd.read_csv(os.path.join(DATA_DIR, 'investors.csv'))
        commitments_df = pd.read_csv(os.path.join(DATA_DIR, 'commitments.csv'))
        cash_flows_df = pd.read_csv(os.path.join(DATA_DIR, 'cash_flows.csv'))

        # Process transaction data
        total_called = cash_flows_df[cash_flows_df['TransactionType'] == 'Capital Call'].groupby('InvestorID')['Amount'].sum().rename('Total_Called')
        total_distributed = cash_flows_df[cash_flows_df['TransactionType'] == 'Distribution'].groupby('InvestorID')['Amount'].sum().rename('Total_Distributed')

        # Process commitment data
        num_commitments = commitments_df.groupby('InvestorID').size().rename('Num_Commitments')

        # Merge data
        df_corr = investors_df.join(num_commitments, on='InvestorID').join(total_called, on='InvestorID').join(total_distributed, on='InvestorID')
        df_corr.fillna(0, inplace=True)

        # One-hot encode RiskAppetite
        df_corr = pd.get_dummies(df_corr, columns=['RiskAppetite'], prefix='RiskAppetite')

        # Select columns for correlation
        cols_for_corr = ['Age', 'AUM', 'Network_Degree', 'Num_Commitments', 'Total_Called', 'Total_Distributed', 'RiskAppetite_High', 'RiskAppetite_Medium', 'RiskAppetite_Low']
        corr_matrix = df_corr[cols_for_corr].corr()

        # Plot heatmap
        plt.figure(figsize=(12, 10))
        sns.heatmap(corr_matrix, annot=True, fmt='.2f', cmap='coolwarm', linewidths=.5)
        plt.title('Correlation Matrix of Key Variables')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        plot_filename = os.path.join(PLOT_DIR, 'correlation_heatmap_1_' + timestamp + '.png')
        plt.savefig(plot_filename, dpi=300)
        plt.close()
        print('Plot saved to: ' + plot_filename)

    except FileNotFoundError as e:
        print('Error creating correlation heatmap: ' + str(e))
    except Exception as e:
        print('An unexpected error occurred during heatmap creation: ' + str(e))


def consolidate_cph_outputs():
    """Consolidates CPH model outputs into a single regression table.

    Reads all coxph_summary_*.csv files, combines them, and saves the result.
    """
    print("\nStep 5: Consolidating CPH model outputs...")
    try:
        summary_files = glob.glob(os.path.join(DATA_DIR, 'coxph_summary_*.csv'))
        if not summary_files:
            print("No CPH summary files found to consolidate.")
            return

        all_summaries = []
        for f in summary_files:
            scenario = os.path.basename(f).replace('coxph_summary_', '').replace('.csv', '')
            df = pd.read_csv(f)
            df['Scenario'] = scenario
            all_summaries.append(df)

        if not all_summaries:
            print("No data to consolidate after processing files.")
            return

        consolidated_df = pd.concat(all_summaries, ignore_index=True)
        consolidated_df.set_index(['Scenario', 'covariate'], inplace=True)

        output_path = os.path.join(DATA_DIR, 'consolidated_cph_results.csv')
        consolidated_df.to_csv(output_path)

        print('Consolidated CPH results saved to: ' + output_path)
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
            print("--- Consolidated CPH Regression Table ---")
            print(consolidated_df)

    except Exception as e:
        print('An unexpected error occurred during CPH consolidation: ' + str(e))


def create_forest_plot():
    """Generates a forest plot of hazard ratios from the consolidated CPH results."""
    print("\nStep 5: Generating forest plot...")
    try:
        consolidated_path = os.path.join(DATA_DIR, 'consolidated_cph_results.csv')
        if not os.path.exists(consolidated_path):
            print("Consolidated CPH results file not found. Skipping forest plot.")
            return

        df = pd.read_csv(consolidated_path)

        plt.figure(figsize=(12, 8))
        y_ticks = []
        y_pos = []
        for i, row in df.iterrows():
            y = len(df) - 1 - i
            y_pos.append(y)
            y_ticks.append(row['Scenario'] + ' - ' + row['covariate'])
            plt.plot([row['exp(coef) lower 95%'], row['exp(coef) upper 95%']], [y, y], 'b-')
            plt.plot(row['exp(coef)'], y, 'bo')

        plt.axvline(x=1, color='r', linestyle='--')
        plt.yticks(y_pos, y_ticks)
        plt.xlabel('Hazard Ratio (exp(coef))')
        plt.title('Forest Plot of Hazard Ratios Across Scenarios')
        plt.grid(axis='y', linestyle=':')
        plt.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        plot_filename = os.path.join(PLOT_DIR, 'forest_plot_cph_1_' + timestamp + '.png')
        plt.savefig(plot_filename, dpi=300)
        plt.close()
        print('Plot saved to: ' + plot_filename)

    except Exception as e:
        print('An unexpected error occurred during forest plot generation: ' + str(e))


def plot_survival_curves():
    """Generates and plots survival curves for a representative scenario.

    This function stratifies the population by a key variable ('Network_Degree')
    and plots Kaplan-Meier survival estimates for each group.
    """
    print("\nStep 5: Generating survival curves for Eurozone_Any scenario...")
    scenario = 'Eurozone_Any'
    stratify_by = 'Network_Degree'

    try:
        # Load necessary data
        investors_df = pd.read_csv(os.path.join(DATA_DIR, 'investors.csv'))
        cash_flows_df = pd.read_csv(os.path.join(DATA_DIR, 'cash_flows.csv'), parse_dates=['Date'])
        first_movers_df = pd.read_csv(os.path.join(DATA_DIR, 'first_movers.csv'), parse_dates=['T0'])

        # Get T0 for the scenario
        t0_row = first_movers_df[(first_movers_df['Shock'] == 'Eurozone') & (first_movers_df['Behavior'] == 'Any')]
        if t0_row.empty:
            print('T0 for scenario ' + scenario + ' not found. Skipping survival curve plot.')
            return
        t0 = t0_row.iloc[0]['T0']

        # Identify at-risk population (investors who haven't acted by T0)
        active_before_t0 = set(cash_flows_df[cash_flows_df['Date'] < t0]['InvestorID'])
        all_investors = set(investors_df['InvestorID'])
        at_risk_investors = list(all_investors - active_before_t0)

        # Find first action after T0 for the at-risk population
        subsequent_actions = cash_flows_df[(cash_flows_df['Date'] >= t0) & (cash_flows_df['InvestorID'].isin(at_risk_investors))].copy()
        first_actions = subsequent_actions.loc[subsequent_actions.groupby('InvestorID')['Date'].idxmin()]

        # Prepare survival data
        survival_data = investors_df[investors_df['InvestorID'].isin(at_risk_investors)].copy()
        survival_data = survival_data.merge(first_actions[['InvestorID', 'Date']], on='InvestorID', how='left')
        survival_data.rename(columns={'Date': 'Event_Date'}, inplace=True)

        end_of_study = cash_flows_df['Date'].max()
        survival_data['Event'] = np.where(pd.notna(survival_data['Event_Date']), 1, 0)
        survival_data['Duration'] = (survival_data['Event_Date'].fillna(end_of_study) - t0).dt.days

        # Stratify by the chosen variable
        median_val = survival_data[stratify_by].median()
        survival_data['Group'] = np.where(survival_data[stratify_by] > median_val, 'High ' + stratify_by, 'Low ' + stratify_by)

        # Plot Kaplan-Meier curves
        plt.figure(figsize=(10, 7))
        ax = plt.subplot(111)
        kmf_high = KaplanMeierFitter()
        kmf_low = KaplanMeierFitter()

        high_group = survival_data[survival_data['Group'] == 'High ' + stratify_by]
        low_group = survival_data[survival_data['Group'] == 'Low ' + stratify_by]

        kmf_high.fit(high_group['Duration'], event_observed=high_group['Event'], label='High ' + stratify_by)
        kmf_high.plot_survival_function(ax=ax)

        kmf_low.fit(low_group['Duration'], event_observed=low_group['Event'], label='Low ' + stratify_by)
        kmf_low.plot_survival_function(ax=ax)

        plt.title('Survival Function for ' + scenario + ' Scenario by ' + stratify_by)
        plt.xlabel('Days Since First Mover Action (T0)')
        plt.ylabel('Survival Probability (No Action Taken)')
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        plot_filename = os.path.join(PLOT_DIR, 'survival_curves_1_' + timestamp + '.png')
        plt.savefig(plot_filename, dpi=300)
        plt.close()
        print('Plot saved to: ' + plot_filename)

    except FileNotFoundError as e:
        print('Error plotting survival curves: ' + str(e))
    except Exception as e:
        print('An unexpected error occurred during survival curve plotting: ' + str(e))


if __name__ == '__main__':
    if not os.path.exists(PLOT_DIR):
        os.makedirs(PLOT_DIR)

    create_correlation_heatmap()
    consolidate_cph_outputs()
    create_forest_plot()
    plot_survival_curves()

    print("\nStep 5: All visualizations and tables generated.")
