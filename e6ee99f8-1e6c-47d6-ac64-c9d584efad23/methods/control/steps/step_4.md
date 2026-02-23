### **Methodology: Survival Analysis of Peer Influence**

This section outlines the statistical framework for quantifying the influence of identified first-movers on their network peers. We will employ survival analysis, specifically the Cox Proportional Hazards model, to analyze the "time to follow"—the duration between a first-mover's action and a subsequent similar action by a connected peer. This approach allows for the rigorous testing of hypotheses concerning the speed and drivers of informational cascades.

#### **1. Defining the At-Risk Population and Observation Period**

For each of the nine identified first-mover events (one for each of the three transaction types across three economic shocks), a specific at-risk population must be constructed for analysis.

*   **At-Risk Peer Group:** For a given first-mover event, initiated by `FirstMover_ID` on day `T_min`, the at-risk peer group is defined as the set of all investors who share a direct connection (an edge) with the `FirstMover_ID` in the relevant co-investment network graph (`G_GFC`, `G_Eurozone`, or `G_COVID`).
*   **Exclusion Criterion:** Any investor within this peer group who has already performed the same type of transaction within the event window *before or on the same day* as the first-mover (`Relative_Day <= T_min`) is excluded from the at-risk population for that specific analysis. They are not "at risk" of following because they have already acted.
*   **Observation Period:** For each investor in the at-risk peer group, the observation period begins at `T_min`, the moment of the first-mover's action. The period ends either when the peer performs the action or at the close of the event window (`T+90`), whichever comes first.

#### **2. Statistical Framework: The Cox Proportional Hazards Model**

To model the rate at which peers follow a first-mover, a Cox Proportional Hazards (CPH) model will be estimated. This semi-parametric model is ideally suited for this research question for two primary reasons:
1.  It effectively models the instantaneous rate (or "hazard") of an event's occurrence (a peer following the action) over time.
2.  It correctly handles right-censored data, which is critical as many peers in the at-risk group may not perform the action by the end of the observation window. These observations are not discarded but contribute valuable information to the model.

The CPH model takes the form:
`h(t | X) = h₀(t) * exp(β₁X₁ + β₂X₂ + ... + βₚXₚ)`

Where:
*   `h(t | X)` is the hazard rate at time `t` for an investor with a given set of covariates `X`.
*   `h₀(t)` is the baseline hazard function, representing the hazard for an individual with all covariates equal to zero. The CPH model does not estimate this component directly.
*   `X₁...Xₚ` are the explanatory covariates (e.g., first-mover's performance score, peer's own characteristics).
*   `β₁...βₚ` are the regression coefficients to be estimated. The exponentiated coefficient, `exp(β)`, is the Hazard Ratio (HR). An HR > 1 for a covariate indicates that an increase in that variable is associated with a higher rate of the event occurring (i.e., faster following).

#### **3. Model Specification: Dependent Variable and Covariates**

For each of the nine first-mover events, a separate CPH model will be fitted. The data for each model will be structured as follows:

*   **Dependent Variable:** The outcome is defined by two components for each peer in the at-risk group:
    *   **Time (`T_follow`):** The number of days from the first-mover's action (`T_min`) to the peer's subsequent similar action. `T_follow = Peer_Action_Day - T_min`.
    *   **Event Status (`Event`):** A binary indicator where `Event = 1` if the peer performs the similar action before the end of the event window (`T+90`). `Event = 0` if the peer does not perform the action by `T+90` (the observation is censored). The time for censored observations is set to `90 - T_min`.

*   **Primary Explanatory Covariates:** These variables are designed to test the core hypotheses (H1b, H2, H3).
    *   **`FirstMover_PS`:** The Performance Score of the first-mover who initiated the cascade. This is the central variable for testing H1b. A positive and significant coefficient `β` for this variable would indicate that a more successful leader prompts a higher rate of following among their peers.
    *   **`Peer_PS`:** The peer's own Performance Score. This controls for the possibility that an investor's actions are driven by their own capabilities and financial health, rather than influence.
    *   **`Portfolio_Overlap`:** A continuous variable measuring the similarity between the first-mover's and the peer's investment portfolios in the pre-event lookback period. This can be calculated using the Jaccard similarity index of their shared fund (`Fund_ID`) investments. A higher overlap may indicate a stronger information channel.

*   **Control Covariates:**
    *   **`Peer_Centrality`:** The degree centrality of the peer investor in the co-investment network. This controls for the peer's own network position and general access to information.
    *   **`Peer_AUM` (if available):** The peer investor's Assets Under Management as a proxy for scale and institutional capacity.

The analysis of the estimated coefficients (`β`) and their corresponding hazard ratios (`exp(β)`) across the nine distinct models will allow us to determine whether the first-mover's historical success is a statistically significant predictor of the speed and likelihood of peer-following behavior during economic crises.