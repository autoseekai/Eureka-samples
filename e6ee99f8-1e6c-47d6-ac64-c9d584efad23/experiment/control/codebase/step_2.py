import pandas as pd
import networkx as nx
from itertools import combinations

DATA_DIR = '/work_dir/data/'

SHOCKS = {
    'GFC': '2008-09-15',
    'Eurozone': '2011-08-05',
    'COVID-19': '2020-03-11'
}

BEHAVIORS = ['Capital Call', 'Distribution', 'Any']


def load_data(data_dir):
    """Loads all necessary CSV files into pandas DataFrames.

    Args:
        data_dir (str): The directory path where the data files are located.

    Returns:
        tuple: A tuple of pandas DataFrames for investors, funds, commitments,
               and cash flows.
    """
    investors_df = pd.read_csv(data_dir + 'investors.csv')
    funds_df = pd.read_csv(data_dir + 'funds.csv')
    commitments_df = pd.read_csv(data_dir + 'commitments.csv')
    cash_flows_df = pd.read_csv(data_dir + 'cash_flows.csv')

    commitments_df['Commitment_Date'] = pd.to_datetime(commitments_df['Commitment_Date'])
    cash_flows_df['Transaction_Date'] = pd.to_datetime(cash_flows_df['Transaction_Date'])

    return investors_df, funds_df, commitments_df, cash_flows_df

def build_co_investment_network(commitments_df, investors_df, shock_date):
    """Constructs a co-investment network for a given shock event.

    An edge exists between two investors if they invested in the same fund
    within a five-year lookback period before the shock date.

    Args:
        commitments_df (pd.DataFrame): DataFrame of commitment data.
        investors_df (pd.DataFrame): DataFrame of investor data.
        shock_date (pd.Timestamp): The date of the economic shock.

    Returns:
        nx.Graph: A networkx graph representing the co-investment network.
    """
    lookback_start_date = shock_date - pd.DateOffset(years=5)
    
    relevant_commitments = commitments_df[
        (commitments_df['Commitment_Date'] >= lookback_start_date) &
        (commitments_df['Commitment_Date'] < shock_date)
    ]

    fund_investors = relevant_commitments.groupby('Fund_ID')['Investor_ID'].apply(list)

    G = nx.Graph()
    G.add_nodes_from(investors_df['Investor_ID'])

    for investor_list in fund_investors:
        if len(investor_list) > 1:
            for investor1, investor2 in combinations(investor_list, 2):
                G.add_edge(investor1, investor2)
    
    return G

def find_first_mover(transactions_df, investors_df, shock_date, behavior):
    """Identifies the first mover for a given shock and transaction behavior.

    Args:
        transactions_df (pd.DataFrame): Merged DataFrame of cash flows and commitments.
        investors_df (pd.DataFrame): DataFrame of investor data for tie-breaking.
        shock_date (pd.Timestamp): The date of the economic shock.
        behavior (str): The transaction behavior to analyze ('Capital Call',
                        'Distribution', or 'Any').

    Returns:
        str: The Investor_ID of the identified first mover, or None if no
             transactions occurred after the shock.
    """
    post_shock_tx = transactions_df[transactions_df['Transaction_Date'] > shock_date].copy()

    if behavior != 'Any':
        post_shock_tx = post_shock_tx[post_shock_tx['Transaction_Type'] == behavior]

    if post_shock_tx.empty:
        return None

    first_action_date = post_shock_tx['Transaction_Date'].min()
    
    tied_movers = post_shock_tx[post_shock_tx['Transaction_Date'] == first_action_date]

    tied_movers_details = pd.merge(
        tied_movers, 
        investors_df[['Investor_ID', 'total_committed']], 
        on='Investor_ID'
    )

    sorted_movers = tied_movers_details.sort_values(
        by=['total_committed', 'Transaction_Amount'], 
        ascending=[False, False]
    )

    first_mover_id = sorted_movers.iloc[0]['Investor_ID']
    
    return first_mover_id

def main():
    """Main function to execute the first-mover analysis.
    
    Loads data, identifies first movers for each scenario, finds consistent
    first movers, and prints the results.
    """ 
    investors_df, funds_df, commitments_df, cash_flows_df = load_data(DATA_DIR)

    transactions_df = pd.merge(
        cash_flows_df, 
        commitments_df[['Commitment_ID', 'Investor_ID']], 
        on='Commitment_ID'
    )

    results = []
    networks = {}

    for shock_name, shock_date_str in SHOCKS.items():
        shock_date = pd.to_datetime(shock_date_str)
        
        networks['G_' + shock_name] = build_co_investment_network(
            commitments_df, investors_df, shock_date
        )

        for behavior in BEHAVIORS:
            first_mover_id = find_first_mover(
                transactions_df, 
                investors_df, 
                shock_date, 
                behavior
            )
            results.append({
                'Shock': shock_name,
                'Behavior': behavior,
                'FirstMover_ID': first_mover_id
            })

    results_df = pd.DataFrame(results)

    print('--- First Mover Identification Results ---')
    print(results_df.to_string())
    print('\n')

    first_mover_shocks = {}
    for index, row in results_df.iterrows():
        investor_id = row['FirstMover_ID']
        if pd.notna(investor_id):
            if investor_id not in first_mover_shocks:
                first_mover_shocks[investor_id] = set()
            first_mover_shocks[investor_id].add(row['Shock'])

    consistent_movers = []
    for investor_id, shock_set in first_mover_shocks.items():
        if len(shock_set) == len(SHOCKS):
            consistent_movers.append(investor_id)

    print('--- Consistent First Movers ---')
    if consistent_movers:
        for mover_id in consistent_movers:
            print(mover_id)
    else:
        print('No consistent first movers found.')

if __name__ == '__main__':
    main()
