import os
import pandas as pd
import numpy as np
import datetime

def generate_investor_profiles(num_investors, seed):
    """
    Generates a DataFrame of simulated investor profiles.

    Args:
        num_investors (int): The number of investors to generate.
        seed (int): The random seed for reproducibility.

    Returns:
        pd.DataFrame: A DataFrame containing investor profiles with columns:
                      'investor_id', 'age', 'initial_net_worth_m',
                      'risk_tolerance', and 'liquidity_needs'.
    """
    np.random.seed(seed)
    investor_ids = np.arange(1, num_investors + 1)
    ages = np.random.randint(35, 71, size=num_investors)
    net_worths = np.round(np.random.lognormal(mean=2.5, sigma=0.8, size=num_investors) + 5, 2)
    risk_tolerances = np.random.choice(
        ['Low', 'Medium', 'High'],
        size=num_investors,
        p=[0.2, 0.5, 0.3]
    )
    liquidity_needs = np.random.choice(
        ['Low', 'Medium', 'High'],
        size=num_investors,
        p=[0.4, 0.4, 0.2]
    )

    investors_df = pd.DataFrame({
        'investor_id': investor_ids,
        'age': ages,
        'initial_net_worth_m': net_worths,
        'risk_tolerance': risk_tolerances,
        'liquidity_needs': liquidity_needs
    })
    return investors_df

def generate_fund_information(num_funds, start_date_str, seed):
    """
    Generates a DataFrame of simulated private equity fund information.

    Args:
        num_funds (int): The number of funds to generate.
        start_date_str (str): The simulation start date ('YYYY-MM-DD').
        seed (int): The random seed for reproducibility.

    Returns:
        pd.DataFrame: A DataFrame containing fund information with columns:
                      'fund_id', 'vintage_year', 'strategy', 'target_size_m'.
    """
    np.random.seed(seed)
    fund_ids = np.arange(1, num_funds + 1)
    start_year = pd.to_datetime(start_date_str).year
    vintage_years = np.random.randint(start_year - 3, start_year + 4, size=num_funds)
    strategies = np.random.choice(
        ['Buyout', 'Venture Capital', 'Growth Equity', 'Real Estate', 'Infrastructure'],
        size=num_funds
    )
    target_sizes = np.round(np.random.lognormal(mean=6, sigma=1, size=num_funds), 0)

    funds_df = pd.DataFrame({
        'fund_id': fund_ids,
        'vintage_year': vintage_years,
        'strategy': strategies,
        'target_size_m': target_sizes
    })
    return funds_df

def simulate_economic_conditions(start_date_str, end_date_str, stress_periods):
    """
    Simulates a time series of economic conditions, including stress periods.

    Args:
        start_date_str (str): The simulation start date ('YYYY-MM-DD').
        end_date_str (str): The simulation end date ('YYYY-MM-DD').
        stress_periods (list of tuples): A list where each tuple contains
                                          the start and end date of a stress
                                          period, e.g., [('YYYY-MM-DD', 'YYYY-MM-DD')].

    Returns:
        pd.DataFrame: A DataFrame with 'date', 'economic_index', and
                      'is_stress_period' columns, indexed by date.
    """
    dates = pd.to_datetime(pd.date_range(start=start_date_str, end=end_date_str, freq='D'))
    economic_df = pd.DataFrame(index=dates)
    economic_df['economic_index'] = 100.0
    economic_df['is_stress_period'] = False

    for start, end in stress_periods:
        economic_df.loc[start:end, 'is_stress_period'] = True

    # Simulate index values
    daily_returns = np.random.normal(loc=0.0003, scale=0.01, size=len(economic_df))
    stress_returns = np.random.normal(loc=-0.001, scale=0.025, size=len(economic_df))
    
    returns = np.where(economic_df['is_stress_period'], stress_returns, daily_returns)
    
    economic_df['economic_index'] = 100 * (1 + pd.Series(returns, index=dates)).cumprod()
    
    return economic_df.resample('Q').last()

def generate_commitments(investors_df, funds_df, start_date_str, seed):
    """
    Generates investment commitments from investors to funds.

    Args:
        investors_df (pd.DataFrame): DataFrame of investor profiles.
        funds_df (pd.DataFrame): DataFrame of fund information.
        start_date_str (str): The simulation start date ('YYYY-MM-DD').
        seed (int): The random seed for reproducibility.

    Returns:
        pd.DataFrame: A DataFrame of commitments with columns: 'investor_id',
                      'fund_id', 'commitment_date', 'commitment_amount_m'.
    """
    np.random.seed(seed)
    commitments = []
    risk_map = {'Low': 0.05, 'Medium': 0.1, 'High': 0.15}
    
    start_date = pd.to_datetime(start_date_str)
    
    for _, investor in investors_df.iterrows():
        num_investments = np.random.randint(1, 5)
        funds_to_invest = np.random.choice(funds_df['fund_id'], num_investments, replace=False)
        
        for fund_id in funds_to_invest:
            base_alloc = risk_map[investor['risk_tolerance']]
            allocation_pct = np.random.normal(loc=base_alloc, scale=0.02)
            commitment_amount = max(0.1, round(investor['initial_net_worth_m'] * allocation_pct, 2))
            
            fund_vintage = funds_df[funds_df['fund_id'] == fund_id]['vintage_year'].iloc[0]
            
            # Commitments happen around the fund's vintage year
            commitment_year = fund_vintage + np.random.randint(-1, 2)
            commitment_month = np.random.randint(1, 13)
            commitment_day = np.random.randint(1, 29)
            commitment_date = pd.to_datetime(str(commitment_year) + '-' + str(commitment_month) + '-' + str(commitment_day))
            
            if commitment_date < start_date:
                commitment_date = start_date + pd.DateOffset(days=np.random.randint(0, 365))

            commitments.append({
                'investor_id': investor['investor_id'],
                'fund_id': fund_id,
                'commitment_date': commitment_date,
                'commitment_amount_m': commitment_amount
            })
            
    return pd.DataFrame(commitments)

def simulate_fund_lifecycle(commitments_df, economic_df, end_date_str, seed):
    """
    Simulates cash flows and NAV history for each commitment over its life.

    Args:
        commitments_df (pd.DataFrame): DataFrame of investment commitments.
        economic_df (pd.DataFrame): DataFrame of quarterly economic conditions.
        end_date_str (str): The simulation end date ('YYYY-MM-DD').
        seed (int): The random seed for reproducibility.

    Returns:
        tuple: A tuple containing two DataFrames:
               - cash_flows_df (pd.DataFrame): All capital calls and distributions.
               - nav_history_df (pd.DataFrame): Quarterly NAV for each investment.
    """
    np.random.seed(seed)
    cash_flows = []
    nav_history = []
    end_date = pd.to_datetime(end_date_str)

    for _, commitment in commitments_df.iterrows():
        total_commitment = commitment['commitment_amount_m']
        commitment_date = commitment['commitment_date']
        
        capital_called = 0
        current_nav = 0
        
        # Fund life is typically 10-12 years
        fund_end_date = min(end_date, commitment_date + pd.DateOffset(years=12))
        
        simulation_quarters = pd.date_range(start=commitment_date, end=fund_end_date, freq='Q')

        for quarter_end_date in simulation_quarters:
            years_since_commit = (quarter_end_date - commitment_date).days / 365.25
            eco_info = economic_df.asof(quarter_end_date)
            eco_index = eco_info['economic_index']
            is_stress = eco_info['is_stress_period']
            
            # 1. Capital Calls (Investment Period: Years 0-5)
            if years_since_commit <= 5 and capital_called < total_commitment:
                # Higher call probability in early years
                if np.random.rand() < (0.8 / (1 + years_since_commit)):
                    remaining_commitment = total_commitment - capital_called
                    call_pct = np.random.uniform(0.05, 0.20)
                    call_amount = min(remaining_commitment, call_pct * total_commitment)
                    
                    if call_amount > 0.01:
                        capital_called += call_amount
                        current_nav += call_amount
                        cash_flows.append({
                            'investor_id': commitment['investor_id'],
                            'fund_id': commitment['fund_id'],
                            'date': quarter_end_date,
                            'type': 'Capital Call',
                            'amount_m': -call_amount
                        })

            # 2. NAV Growth
            if current_nav > 0:
                base_growth = np.random.normal(0.03, 0.015) # Quarterly growth
                eco_multiplier = (eco_index / 100.0)
                if is_stress:
                    eco_multiplier *= 0.5 # Amplify negative effect in stress
                
                growth_rate = base_growth * eco_multiplier
                current_nav *= (1 + growth_rate)

            # 3. Distributions (Harvesting Period: Years 4-12)
            if years_since_commit > 4 and current_nav > 0:
                # Higher distribution probability in later years
                if np.random.rand() < (0.6 * ((years_since_commit - 4) / 8)):
                    dist_pct = np.random.uniform(0.02, 0.10)
                    
                    # Reduce distributions in stress periods
                    eco_multiplier = (eco_index / 100.0) if not is_stress else (eco_index / 100.0) * 0.25
                    
                    dist_amount = current_nav * dist_pct * eco_multiplier
                    
                    if dist_amount > 0.01:
                        current_nav -= dist_amount
                        cash_flows.append({
                            'investor_id': commitment['investor_id'],
                            'fund_id': commitment['fund_id'],
                            'date': quarter_end_date,
                            'type': 'Distribution',
                            'amount_m': dist_amount
                        })
            
            # Record NAV at end of quarter
            nav_history.append({
                'investor_id': commitment['investor_id'],
                'fund_id': commitment['fund_id'],
                'date': quarter_end_date,
                'nav_m': max(0, current_nav) # NAV cannot be negative
            })

    cash_flows_df = pd.DataFrame(cash_flows)
    nav_history_df = pd.DataFrame(nav_history)
    
    return cash_flows_df, nav_history_df


if __name__ == '__main__':
    # --- Configuration ---
    DATA_DIR = '/work_dir/data'
    
    NUM_INVESTORS = 200
    NUM_FUNDS = 25
    START_DATE = '2010-01-01'
    END_DATE = '2023-12-31'
    
    # Define periods of economic stress
    STRESS_PERIODS = [
        ('2015-06-01', '2016-06-30'), # Example: Oil price shock / China slowdown
        ('2020-02-01', '2020-08-31')  # Example: COVID-19 shock
    ]
    
    # Use a fixed seed for reproducibility
    RANDOM_SEED = 42

    # --- Execution ---
    print("Step 1: Data Simulation Started.")
    
    # Create data directory if it doesn't exist
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
        print("Created directory: " + DATA_DIR)

    # 1. Generate Investor Profiles
    investors = generate_investor_profiles(NUM_INVESTORS, seed=RANDOM_SEED)
    investors_path = os.path.join(DATA_DIR, 'investors.csv')
    investors.to_csv(investors_path, index=False)
    print("Generated " + str(len(investors)) + " investor profiles.")

    # 2. Generate Fund Information
    funds = generate_fund_information(NUM_FUNDS, START_DATE, seed=RANDOM_SEED + 1)
    funds_path = os.path.join(DATA_DIR, 'funds.csv')
    funds.to_csv(funds_path, index=False)
    print("Generated " + str(len(funds)) + " fund profiles.")

    # 3. Simulate Economic Conditions
    economic_conditions = simulate_economic_conditions(START_DATE, END_DATE, STRESS_PERIODS)
    economic_path = os.path.join(DATA_DIR, 'economic_conditions.csv')
    economic_conditions.to_csv(economic_path)
    print("Simulated quarterly economic conditions from " + START_DATE + " to " + END_DATE + ".")

    # 4. Generate Commitments
    commitments = generate_commitments(investors, funds, START_DATE, seed=RANDOM_SEED + 2)
    commitments_path = os.path.join(DATA_DIR, 'commitments.csv')
    commitments.to_csv(commitments_path, index=False)
    print("Generated " + str(len(commitments)) + " investment commitments.")

    # 5. Simulate Fund Lifecycles (Cash Flows and NAV)
    cash_flows, nav_history = simulate_fund_lifecycle(commitments, economic_conditions, END_DATE, seed=RANDOM_SEED + 3)
    cash_flows_path = os.path.join(DATA_DIR, 'cash_flows.csv')
    nav_history_path = os.path.join(DATA_DIR, 'nav_history.csv')
    cash_flows.to_csv(cash_flows_path, index=False)
    nav_history.to_csv(nav_history_path, index=False)
    print("Simulated " + str(len(cash_flows)) + " cash flow transactions.")
    print("Simulated " + str(len(nav_history)) + " quarterly NAV records.")

    # --- Summary Output ---
    print("\n--- Simulation Summary ---")
    total_committed = commitments['commitment_amount_m'].sum()
    print("Total Capital Committed: $" + str(round(total_committed, 2)) + "M")
    
    capital_calls = cash_flows[cash_flows['type'] == 'Capital Call']['amount_m'].sum()
    print("Total Capital Called: $" + str(round(abs(capital_calls), 2)) + "M")
    
    distributions = cash_flows[cash_flows['type'] == 'Distribution']['amount_m'].sum()
    print("Total Distributions: $" + str(round(distributions, 2)) + "M")
    
    final_nav = nav_history.sort_values('date').groupby(['investor_id', 'fund_id']).last()['nav_m'].sum()
    print("Final Total NAV at " + END_DATE + ": $" + str(round(final_nav, 2)) + "M")
    
    print("\nData saved to '" + DATA_DIR + "' directory:")
    print("- " + os.path.basename(investors_path))
    print("- " + os.path.basename(funds_path))
    print("- " + os.path.basename(economic_path))
    print("- " + os.path.basename(commitments_path))
    print("- " + os.path.basename(cash_flows_path))
    print("- " + os.path.basename(nav_history_path))
    
    print("\nStep 1: Data Simulation Complete.")
