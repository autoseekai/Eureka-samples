### **Methodology**

This section details the complete empirical framework designed to identify first-movers within private equity co-investment networks and to quantify their influence on peer transaction behavior during periods of economic crisis. The methodology is presented as a sequence of procedural steps, from hypothesis formulation to the final econometric model specification.

#### **1. Hypothesis and Operational Definitions**

##### **1.1. Research Hypotheses**
The empirical analysis is structured to test the following hypotheses:
*   **Primary Hypothesis (H1):** The existence and influence of consistent first-movers are functions of their historical performance.
    *   **H1a (Consistency of Leadership):** A statistically small and identifiable subset of investors consistently initiates significant transactions before their network peers during distinct major economic shocks.
    *   **H1b (Influence via Success):** The probability of network peers executing a similar transaction following a first-mover's action is positively and significantly correlated with the first-mover’s historical investment performance.
*   **Secondary Hypothesis (H2 - Cascade Velocity):** The time lag between a first-mover’s transaction and the median time of subsequent, similar transactions by their network peers is inversely proportional to the first-mover's historical investment performance.
*   **Secondary Hypothesis (H3 - Cascade Magnitude):** The aggregate volume of capital in following transactions, as a percentage of followers’ assets under management (AUM), is positively correlated with the historical investment performance of the first-mover.

##### **1.2. Operational Definition of Major Economic Shocks**
The analysis is anchored around three distinct market-wide stress events, with T=0 defined as the event date:
*   **Global Financial Crisis (GFC):** T=0 is September 15, 2008 (Lehman Brothers bankruptcy filing).
*   **Eurozone Sovereign Debt Crisis Peak:** T=0 is May 10, 2010 (Announcement of the first Greek bailout package).
*   **COVID-19 Pandemic Market Crash:** T=0 is March 11, 2020 (WHO declaration of a global pandemic).

##### **1.3. Event Window Specification**
For each shock, transaction data are analyzed within a 121-day window defined as **[T-30 days, T+90 days]**. The pre-event period (T-30 to T-1) establishes a baseline, while the post-event period (T=0 to T+90) captures decision-making and execution lags inherent to private markets.

##### **1.4. Co-investment Network Construction**
For each economic shock, an undirected graph is constructed where nodes are investors (LPs) and an edge exists between two nodes if, in the five-year period preceding T=0, they have either invested in the same private equity fund or participated in the same direct co-investment deal.

##### **1.5. Definition of Analyzed Transaction Behaviors**
Three discrete, high-signal transaction types are analyzed:
*   **Secondary Market Sale (Liquidation Signal):** The sale of an LP interest in a fund representing over 15% of the investor's total commitment to that fund.
*   **New Fund Commitment (Allocation Signal):** A commitment to a fund managed by a GP with whom the investor has no relationship in the prior three years, or a commitment to a new fund strategy deviating from the investor's established pattern.
*   **Default on a Capital Call (Distress Signal):** The failure to meet a formal capital call from a GP.

#### **2. Data Preparation and Network Construction**

##### **2.1. Data Filtering and Transaction Classification**
Raw transactional data are processed to isolate and classify the defined behaviors.
*   **Secondary Market Sales:** Transactions where `Transaction_Type` is 'Secondary Sale' are filtered. The ratio of `Transaction_Amount` to total `Commitment_Amount` for the specific investor-fund pair is calculated, and only sales where this ratio exceeds 0.15 are retained.
*   **New Fund Commitments:** Transactions where `Transaction_Type` is 'New Commitment' are cross-referenced against the investor's three-year history with the specified `GP_ID`. Commitments to new GPs or to new fund strategies (identified via metadata) are classified as allocation signals.
*   **Capital Call Defaults:** Records where `Transaction_Type` is 'Capital Call Default' are classified directly without further filtering.

##### **2.2. Event-Relative Transaction Timeline Construction**
All classified transactions are mapped to a relative timeline for each shock. The `Transaction_Date` is used to filter transactions into the [T-30, T+90] window for each of the three events. A relative day value is computed for each transaction: `Relative_Day = Transaction_Date - T_event_date`, standardizing the timeline from -30 to +90.

##### **2.3. Co-investment Network Graph Construction**
Three distinct network graphs (`G_GFC`, `G_Eurozone`, `G_COVID`) are generated. For each event, a five-year lookback period is defined. An edge is created between any two investor nodes that appear as LPs in the same `Fund_ID` or as participants in the same direct deal within that lookback period, resulting in three separate adjacency lists.

##### **2.4. Formulation of Historical Investment Success Metric**
A composite "Performance Score" (PS) is calculated for each investor at the start of each event window.
1.  **Metric Components:** Based on historical cash flow and NAV data from the five years preceding T=0, two metrics are calculated: Realized IRR (`rIRR`) on fully exited investments and Total Value to Paid-In (`TVPI`) for the entire portfolio as of T-31.
2.  **Normalization:** Both `rIRR` and `TVPI` distributions are standardized using z-scores: `Z(x) = (x - μ) / σ`.
3.  **Composite Score:** The final `PS_i` for investor *i* is a weighted average: `PS_i = (0.5 * Z(rIRR_i)) + (0.5 * Z(TVPI_i))`. This score is calculated for each investor prior to each of the three event windows.

#### **3. First-Mover Identification Algorithm**

##### **3.1. Identification Procedure**
The following algorithm is executed independently for each of the nine event-transaction scenarios (3 shocks × 3 behaviors).
1.  **Select Scenario:** Choose one economic shock (e.g., `GFC`) and one transaction type (e.g., `Significant Secondary Sale`).
2.  **Find Earliest Action:** Within the corresponding data subset, identify the minimum `Relative_Day`, denoted `T_min`.
3.  **Isolate Candidates:** Filter for all transactions that occurred on `T_min`.
4.  **Apply Tie-Breaking Protocol:**
    *   If only one transaction occurred on `T_min`, that `Investor_ID` is the First-Mover.
    *   If multiple transactions occurred on `T_min`, retrieve the `PS_i` for each candidate investor. The investor with the highest `PS_i` is designated the First-Mover. If `PS_i` scores are identical, the tie is broken by the largest `Transaction_Amount`.
5.  **Record Output:** The identified `FirstMover_ID` is recorded for each scenario.

##### **3.2. Consistency Classification**
An investor is classified as a **"Consistent First-Mover"** if identified as the First-Mover for the *same transaction type* in at least two of the three economic shock events. These investors are the primary subjects for the subsequent influence analysis.

#### **4. Cascade Analysis using Survival Modeling**

##### **4.1. Defining the At-Risk Population**
For each identified first-mover event, the at-risk population consists of all investors directly connected to the `FirstMover_ID` in the relevant co-investment network graph. Investors who performed the same transaction on or before `T_min` are excluded. The observation period for each peer begins at `T_min` and ends when they follow the action or at day T+90 (censoring).

##### **4.2. Statistical Framework: Cox Proportional Hazards Model**
A Cox Proportional Hazards (CPH) model is used to estimate the rate at which peers follow a first-mover. The model is specified as `h(t | X) = h₀(t) * exp(β₁X₁ + ... + βₚXₚ)`, where `h(t | X)` is the hazard rate at time `t` given covariates `X`, and `h₀(t)` is the non-parametric baseline hazard. This framework correctly handles right-censored data for peers who do not act within the event window.

##### **4.3. Dependent Variable Specification**
The outcome for each peer in the at-risk group is defined by two components:
*   **Time (`T_follow`):** The number of days from the first-mover's action to the peer's action (`Peer_Action_Day - T_min`).
*   **Event Status (`Event`):** A binary indicator, `1` if the peer follows the action before T+90, and `0` if the observation is censored at the end of the window.

#### **5. Econometric Framework for Hypothesis Testing**

##### **5.1. Full Model Specification**
For each of the nine first-mover events, a CPH model is estimated. The hazard function `h(t)` for a peer investor to follow the action is specified as:

`h(t | X) = h₀(t) * exp(β₁*FirstMover_PS + β₂*Peer_PS + β₃*Portfolio_Overlap + β₄*FirstMover_Txn_Size_Norm + β₅*Market_Volatility + β₆*Peer_Centrality)`

##### **5.2. Variable Definitions**
*   **`FirstMover_PS` (Primary Independent Variable):** The Performance Score of the first-mover. A positive and significant `β₁` supports H1b, indicating that a more successful leader increases the rate of following.
*   **`Peer_PS` (Control):** The peer's own Performance Score, to control for homophily and independent skilled action.
*   **`Portfolio_Overlap` (Control):** The Jaccard similarity index of fund investments between the first-mover and the peer, to control for the strength of the information channel.
*   **`FirstMover_Txn_Size_Norm` (Control):** The first-mover's transaction amount, normalized by AUM, to control for the strength of the initial signal.
*   **`Market_Volatility` (Control):** The average VIX value in the 5 days leading up to `T_min`, to control for general market panic.
*   **`Peer_Centrality` (Control):** The degree centrality of the peer in the network, to control for the peer's own informational access.

##### **5.3. Required Output for Hypothesis Validation**
The analysis will produce a regression output table for each of the nine fitted CPH models. Validation of H1b requires a `p-value` < 0.05 and a positive `Coefficient (β)` for the `FirstMover_PS` variable. This table will report the Coefficient (β), Hazard Ratio (exp(β)), Standard Error (SE), z-value, and p-value for each variable.

| Variable                     | Coefficient (β) | Hazard Ratio (exp(β)) | Std. Error (SE) | z-value | p-value (P>|z|) |
| ---------------------------- | --------------- | --------------------- | --------------- | ------- | ---------------- |
| `FirstMover_PS`              |                 |                       |                 |         |                  |
| `Peer_PS`                    |                 |                       |                 |         |                  |
| `Portfolio_Overlap`          |                 |                       |                 |         |                  |
| `FirstMover_Txn_Size_Norm`   |                 |                       |                 |         |                  |
| `Market_Volatility`          |                 |                       |                 |         |                  |
| `Peer_Centrality`            |                 |                       |                 |         |                  |