### **Methodological Framework: Hypotheses and Operational Definitions**

This section outlines the foundational definitions and hypotheses that will guide the empirical analysis of investor behavior within private equity networks during periods of economic distress.

#### **1. Research Hypotheses**

The study is designed to test a primary hypothesis and two secondary hypotheses concerning leadership and peer effects in private equity transaction behavior.

*   **Primary Hypothesis (H1):** The existence of consistent first-movers and their influence is a function of past performance. This can be broken into two testable components:
    *   **H1a (Consistency of Leadership):** A statistically small and identifiable subset of investors consistently initiates significant transactions (e.g., secondary sales, new commitments) before their network peers during distinct major economic shocks.
    *   **H1b (Influence via Success):** The probability of network peers executing a similar transaction following a first-mover's action is positively and significantly correlated with the first-mover’s historical investment performance (e.g., realized IRR, TVPI).

*   **Secondary Hypothesis (H2):** The speed of the informational cascade is modulated by the perceived quality of the initial signal.
    *   **H2 (Cascade Velocity):** The time lag between a first-mover’s transaction and the median time of subsequent, similar transactions by their network peers is inversely proportional to the first-mover's historical investment performance. A more successful leader prompts a faster follower response.

*   **Secondary Hypothesis (H3):** The magnitude of the network response is a function of the leader's credibility.
    *   **H3 (Cascade Magnitude):** The aggregate volume of capital involved in following transactions, measured as a percentage of the followers’ assets under management (AUM), is positively correlated with the historical investment performance of the first-mover.

#### **2. Operational Definition of Major Economic Shocks**

To ensure the analysis captures reactions to exogenous, market-wide stress events, the following periods are designated as "major economic shocks." The date specified (T=0) serves as the anchor for each event window.

*   **Global Financial Crisis (GFC):**
    *   **Event:** Lehman Brothers Holdings Inc. files for Chapter 11 bankruptcy protection.
    *   **Date (T=0):** September 15, 2008.
    *   **Rationale:** This event triggered a severe, global liquidity crisis and a fundamental repricing of risk, directly impacting private equity portfolio valuations and fundraising capabilities.

*   **Eurozone Sovereign Debt Crisis Peak:**
    *   **Event:** The announcement of the first Greek bailout package and the creation of the European Financial Stability Facility (EFSF).
    *   **Date (T=0):** May 10, 2010.
    *   **Rationale:** This marked a peak in systemic risk concerns within the European Union, a key market for many private equity funds, creating significant uncertainty around currency stability and regional economic growth.

*   **COVID-19 Pandemic Market Crash:**
    *   **Event:** The World Health Organization (WHO) declares COVID-19 a global pandemic, coinciding with a sharp global equity market downturn and emergency central bank actions.
    *   **Date (T=0):** March 11, 2020.
    *   **Rationale:** This event represents a unique, non-financial, exogenous shock that caused unprecedented global economic shutdowns, supply chain disruptions, and uncertainty, impacting all sectors of the economy relevant to private equity investments.

#### **3. Event Window Specification**

For each economic shock, transaction data will be analyzed within a precisely defined event window of 121 days.

*   **Definition:** The window is defined as **[T-30 days, T+90 days]**, where T=0 is the date of the economic shock.
*   **Rationale:**
    *   **Pre-Event Period (T-30 to T-1):** This 30-day period serves as a baseline to establish normal transaction patterns and investor activity immediately preceding the shock.
    *   **Post-Event Period (T=0 to T+90):** This 90-day (approximately one fiscal quarter) period provides a sufficient timeframe to capture the decision-making and transaction execution lags inherent in the private equity market. Unlike public markets, private capital decisions involving due diligence, legal documentation, and capital calls require weeks or months to execute, making a 90-day window essential for observing potential cascade effects.

#### **4. Co-investment Network Construction**

The co-investment network will be constructed as a series of undirected graphs, one for each economic shock.

*   **Nodes:** Each node represents a distinct Limited Partner (LP) or investment entity within the dataset.
*   **Edges (Connections):** An edge exists between two nodes (Investor A and Investor B) if they meet at least one of the following criteria in the five-year period preceding the event date (T):
    1.  **Shared Fund Investment:** Both investors are LPs in the same private equity fund.
    2.  **Shared Direct Investment:** Both investors participated as co-investors in the same direct deal or syndicate.
*   **Rationale:** This definition establishes a network based on shared investment experiences and due diligence. The five-year lookback period ensures that the connections represent relevant and recent relationships, reflecting a common pool of information and shared exposure to specific General Partners (GPs) and strategies. The network is reconstructed for each shock to capture its dynamic nature over time.

#### **5. Definition of Analyzed Transaction Behaviors**

To identify first-mover actions and subsequent follower behavior, we will focus on discrete, significant, and discretionary investment decisions. The following transaction types will be coded from the raw data:

*   **Secondary Market Sale (Liquidation Signal):** The sale of an LP’s interest in a private equity fund on the secondary market. A transaction will be classified as a significant liquidation signal if the interest sold represents more than 15% of the investor's total commitment to that particular fund.
*   **New Fund Commitment (Allocation Signal):** A legally binding commitment of capital to a new private equity fund. To filter for strategic shifts, this is defined as a commitment to a fund managed by a GP with whom the investor has not invested in the prior three years, or a commitment to a new fund strategy (e.g., distressed debt, venture) that constitutes a deviation from the investor's established allocation pattern.
*   **Default on a Capital Call (Distress Signal):** The failure of an LP to provide capital when formally requested by a GP. This is a rare but extremely strong negative signal regarding the investor's liquidity position and market outlook.