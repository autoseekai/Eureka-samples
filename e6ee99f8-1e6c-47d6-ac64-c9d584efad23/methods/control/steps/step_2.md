### **Methodology: Data Processing and Metric Construction**

This section details the procedures for processing the raw data into an analyzable format. The methodology is organized into four core components: (1) filtering and classifying transaction behaviors, (2) mapping transactions onto event-relative timelines, (3) constructing the co-investment network graphs, and (4) formulating a quantitative metric for historical investment success.

#### **1. Data Filtering and Transaction Classification Procedure**

The initial step involves filtering the raw transactional dataset to isolate the three specific, high-signal behaviors defined in Step 1. The raw data is assumed to contain fields such as `Investor_ID`, `GP_ID`, `Fund_ID`, `Transaction_Date`, `Transaction_Type`, `Transaction_Amount`, and `Commitment_Amount`.

*   **Secondary Market Sale (Liquidation Signal):**
    1.  Isolate all records where `Transaction_Type` is 'Secondary Sale'.
    2.  For each of these sale transactions, retrieve the corresponding `Investor_ID` and `Fund_ID`.
    3.  Join this data with a fund commitment table to access the total `Commitment_Amount` for that specific investor-fund pair.
    4.  Calculate the sale's significance: `Significance_Ratio = Transaction_Amount / Commitment_Amount`.
    5.  Retain only those transactions where `Significance_Ratio > 0.15`. These are classified as "Significant Secondary Sales."

*   **New Fund Commitment (Allocation Signal):**
    1.  Isolate all records where `Transaction_Type` is 'New Commitment'.
    2.  For each commitment, query the historical transaction database for the given `Investor_ID` to check for any prior commitments to funds managed by the same `GP_ID` within the three years preceding the `Transaction_Date`.
    3.  A transaction is classified as a "New Relationship Commitment" if no such prior relationship exists.
    4.  Additionally, fund-level metadata (`Fund_Strategy`, `Fund_Vintage_Year`) will be used to identify commitments to new strategies (e.g., an investor historically focused on 'Buyout' committing to a 'Venture Growth' fund). This classification will be appended to the transaction record.

*   **Default on a Capital Call (Distress Signal):**
    1.  Isolate all records where `Transaction_Type` is 'Capital Call Default'.
    2.  These events are inherently significant and require no further quantitative filtering. Each instance will be directly classified as a "Default Event."

#### **2. Event-Relative Transaction Timeline Construction**

To analyze behavior in the context of market shocks, all classified transactions must be mapped to a relative timeline centered on each event's T=0 date.

1.  **Define Event Anchors:**
    *   **GFC:** T=0 is September 15, 2008.
    *   **Eurozone Crisis:** T=0 is May 10, 2010.
    *   **COVID-19 Pandemic:** T=0 is March 11, 2020.
2.  **Filter by Event Window:** For each of the three economic shocks, create a separate transaction subset. This subset will include all classified transactions from the previous step whose `Transaction_Date` falls within the [T-30, T+90] day window for that specific shock.
3.  **Calculate Relative Timestamp:** For every transaction within each event window, compute a relative day value: `Relative_Day = Transaction_Date - T_event_date`. This converts the absolute date into an integer value from -30 to +90, standardizing the timeline across all three events and facilitating sequence analysis.

#### **3. Co-investment Network Graph Construction**

A dynamic network will be constructed for each of the three economic shocks to represent the relational structure of investors leading up to the event. The network is an undirected graph where nodes are investors and edges signify a shared investment history.

1.  **Define Lookback Periods:** For each event's T=0 date, a five-year historical lookback period is established (e.g., for the GFC, the period is September 15, 2003, to September 14, 2008).
2.  **Node Identification:** All unique `Investor_ID` entities in the dataset are designated as nodes.
3.  **Edge Creation:** An edge is established between two nodes (Investor A, Investor B) if, within the specified five-year lookback period, they meet either of the following conditions:
    *   **Shared Fund:** Both `Investor_ID`s appear as Limited Partners in the same `Fund_ID`.
    *   **Shared Direct Deal:** Both `Investor_ID`s appear as participants in the same direct co-investment vehicle or syndicate.
4.  **Graph Generation:** This process will be repeated three times, generating three distinct adjacency lists (or matrices): `G_GFC`, `G_Eurozone`, and `G_COVID`. This captures the evolution of the co-investment network over time.

#### **4. Formulation of Historical Investment Success Metric**

To test hypotheses relating leader influence to past performance, a composite "Performance Score" (PS) will be calculated for each investor at the start of each event window. This score synthesizes both realized and unrealized performance.

1.  **Data Requirement:** The calculation requires historical cash flow data (contributions, distributions) and periodic Net Asset Value (NAV) for each investor's private equity portfolio.
2.  **Metric Components:**
    *   **Realized IRR (rIRR):** The net Internal Rate of Return calculated using all cash flows from fully realized investments over the five-year lookback period preceding T=0.
    *   **Total Value to Paid-In (TVPI):** The TVPI multiple (Residual Value + Distributions) / Paid-in Capital, calculated for the entire portfolio (realized and unrealized assets) as of T-31 (one day before the event window begins).
3.  **Normalization:** Both rIRR and TVPI will be calculated for every investor in the sample. To make the metrics comparable, their distributions will be standardized using a z-score transformation: `Z(x) = (x - μ) / σ`, where μ and σ are the mean and standard deviation of the metric across all investors for that period.
4.  **Composite Score Formulation:** The final Performance Score for investor *i* is a weighted average of the normalized components:
    *   `PS_i = (0.5 * Z(rIRR_i)) + (0.5 * Z(TVPI_i))`
    *   The equal weighting (0.5) assigns the same importance to demonstrated ability to generate cash returns (rIRR) and the current market-perceived quality of their standing portfolio (TVPI). This score will be calculated for each investor as of the day before each of the three event windows begins.