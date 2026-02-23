import pandas as pd
import numpy as np
import networkx as nx
from lifelines import CoxPHFitter
from datetime import timedelta
import os


DATA_DIR = "/work_dir/data"
RESULTS_DIR = DATA_DIR
os.makedirs(RESULTS_DIR, exist_ok=True)

INVESTORS_FILE = os.path.join(DATA_DIR, "investors.csv")
FUNDS_FILE = os.path.join(DATA_DIR, "funds.csv")
COMMITMENTS_FILE = os.path.join(DATA_DIR, "commitments.csv")
CASH_FLOWS_FILE = os.path.join(DATA_DIR, "cash_flows.csv")
FIRST_MOVERS_FILE = os.path.join(DATA_DIR, "first_movers.csv")
ECONOMIC_CONDITIONS_FILE = os.path.join(DATA_DIR, "economic_conditions.csv")

def get_shock_periods(econ_conditions_df):
    """
    Identifies the start and end dates of economic shocks.

    Args:
        econ_conditions_df (pd.DataFrame): DataFrame with economic conditions data.

    Returns:
        dict: A dictionary mapping shock names to (start_date, end_date) tuples.
    """
    shock_periods = {}
    econ_conditions_df['Date'] = pd.to_datetime(econ_conditions_df['Date'])
    for shock_name in ['GFC', 'Eurozone', 'COVID-19']:
        shock_df = econ_conditions_df[econ_conditions_df['Shock'] == shock_name]
        if not shock_df.empty:
            shock_periods[shock_name] = (shock_df['Date'].min(), shock_df['Date'].max())
    return shock_periods

def build_investor_network(commitments_df):
    """
    Builds an undirected graph of investors based on shared fund commitments.

    Args:
        commitments_df (pd.DataFrame): DataFrame with commitment data.

    Returns:
        nx.Graph: A NetworkX graph where nodes are investors and edges represent
                  co-investment in the same fund.
    """
    G = nx.Graph()
    all_investors = pd.unique(commitments_df['InvestorID'])
    G.add_nodes_from(all_investors)

    grouped_by_fund = commitments_df.groupby('FundID')['InvestorID'].apply(list)
    for investors_in_fund in grouped_by_fund:
        for i in range(len(investors_in_fund)):
            for j in range(i + 1, len(investors_in_fund)):
                G.add_edge(investors_in_fund[i], investors_in_fund[j])
    return G

def run_cox_model_for_scenario(scenario, cash_flows_df, investors_df, G, shock_periods):
    """
    Prepares data for a single first-mover scenario and fits a Cox model.

    Args:
        scenario (pd.Series): A row from the first_movers_df.
        cash_flows_df (pd.DataFrame): DataFrame with all cash flow transactions.
        investors_df (pd.DataFrame): DataFrame with investor attributes.
        G (nx.Graph): The investor network graph.
        shock_periods (dict): A dictionary of shock period dates.
    """
    shock = scenario['Shock']
    behavior = scenario['Behavior']
    first_mover_id = scenario['FirstMover_ID']
    
    scenario_name = str(shock) + "_" + str(behavior).replace(" ", "_")
    print("--- Processing Scenario: " + scenario_name + " ---")

    if pd.isna(first_mover_id):
        print("Skipping scenario " + scenario_name + " due to no first mover identified.")
        return

    first_mover_id = int(first_mover_id)

    shock_start, shock_end = shock_periods.get(shock, (None, None))
    if not shock_start:
        print("Warning: Shock period for '" + shock + "' not found. Skipping.")
        return

    fm_actions = cash_flows_df[
        (cash_flows_df['InvestorID'] == first_mover_id) &
        (cash_flows_df['Date'] >= shock_start) &
        (cash_flows_df['Date'] <= shock_end)
    ]

    if behavior != 'Any':
        fm_actions = fm_actions[fm_actions['TransactionType'] == behavior]

    if fm_actions.empty:
        print("Warning: First mover " + str(first_mover_id) + " has no actions for behavior '" + behavior + "' during '" + shock + "'. Skipping.")
        return

    t0 = fm_actions['Date'].min()
    t_end = t0 + timedelta(days=90)
    print("First mover action date (T0): " + str(t0.date()))

    if first_mover_id not in G:
        print("Warning: First mover " + str(first_mover_id) + " not in the network. Skipping.")
        return
        
    peers = list(G.neighbors(first_mover_id))
    
    actions_on_or_before_t0 = cash_flows_df[cash_flows_df['Date'] <= t0]
    actors_on_or_before_t0 = set(actions_on_or_before_t0['InvestorID'].unique())
    
    at_risk_peers = [p for p in peers if p not in actors_on_or_before_t0]
    
    if not at_risk_peers:
        print("No peers at risk for this scenario. Skipping.")
        return
    print("At-risk population size: " + str(len(at_risk_peers)))

    survival_data = []
    for peer_id in at_risk_peers:
        peer_actions_after_t0 = cash_flows_df[
            (cash_flows_df['InvestorID'] == peer_id) &
            (cash_flows_df['Date'] > t0) &
            (cash_flows_df['Date'] <= t_end)
        ]
        
        if behavior != 'Any':
            peer_actions_after_t0 = peer_actions_after_t0[peer_actions_after_t0['TransactionType'] == behavior]

        if not peer_actions_after_t0.empty:
            event_date = peer_actions_after_t0['Date'].min()
            time_to_event = (event_date - t0).days
            event = 1
        else:
            time_to_event = 90
            event = 0
            
        survival_data.append({'InvestorID': peer_id, 'Time': time_to_event, 'Event': event})

    if not survival_data:
        print("No survival data generated. Skipping.")
        return

    survival_df = pd.DataFrame(survival_data)

    degrees = pd.DataFrame(G.degree(), columns=['InvestorID', 'Network_Degree'])
    analysis_df = pd.merge(survival_df, investors_df, on='InvestorID', how='left')
    analysis_df = pd.merge(analysis_df, degrees, on='InvestorID', how='left')
    
    categorical_cols = ['RiskAppetite', 'ExperienceLevel', 'InvestmentPhilosophy']
    analysis_df = pd.get_dummies(analysis_df, columns=categorical_cols, drop_first=True, dummy_na=False)
    
    covariates = ['Age', 'AUM', 'Network_Degree'] + [c for c in analysis_df.columns if any(cat in c for cat in categorical_cols)]
    
    final_model_columns = ['Time', 'Event']
    for cov in covariates:
        if cov in analysis_df.columns:
            analysis_df[cov] = pd.to_numeric(analysis_df[cov], errors='coerce')
            final_model_columns.append(cov)

    analysis_df.dropna(subset=final_model_columns, inplace=True)
    
    if analysis_df.shape[0] < 2 or analysis_df['Event'].sum() == 0:
        print("Not enough data or no events observed to fit the model. Found " + str(analysis_df.shape[0]) + " data points and " + str(analysis_df['Event'].sum()) + " events.")
        return

    cph = CoxPHFitter()
    try:
        cph.fit(analysis_df[final_model_columns], duration_col='Time', event_col='Event', step_size=0.1)
        
        summary = cph.summary
        output_path = os.path.join(RESULTS_DIR, "coxph_summary_" + scenario_name + ".csv")
        summary.to_csv(output_path)
        print("CoxPH model fitted. Summary saved to: " + output_path)
        print("Model Summary for " + scenario_name + ":")
        print(summary)
        
    except Exception as e:
        print("Error fitting CoxPH model for scenario " + scenario_name + ": " + str(e))


def main():
    """
    Main function to execute the survival analysis for all first-mover scenarios.
    """
    print("Step 4: Starting Survival Analysis using Cox Proportional Hazards Model.")
    
    try:
        investors_df = pd.read_csv(INVESTORS_FILE)
        commitments_df = pd.read_csv(COMMITMENTS_FILE)
        cash_flows_df = pd.read_csv(CASH_FLOWS_FILE, parse_dates=['Date'])
        first_movers_df = pd.read_csv(FIRST_MOVERS_FILE)
        econ_conditions_df = pd.read_csv(ECONOMIC_CONDITIONS_FILE)
    except FileNotFoundError as e:
        print("Error: Could not find a required data file. " + str(e))
        return

    shock_periods = get_shock_periods(econ_conditions_df)
    investor_network = build_investor_network(commitments_df)
    
    for index, scenario in first_movers_df.iterrows():
        run_cox_model_for_scenario(scenario, cash_flows_df, investors_df, investor_network, shock_periods)

    print("\nStep 4: Survival Analysis Complete.")


if __name__ == '__main__':
    main()
