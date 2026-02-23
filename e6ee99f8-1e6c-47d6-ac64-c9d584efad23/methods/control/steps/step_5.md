### **Methodology: Model Specification for Cascade Analysis**

To empirically test the hypothesis that the historical success of a first-mover drives peer-following behavior (H1b), the Cox Proportional Hazards (CPH) model introduced in the previous section will be specified with a primary independent variable and a set of essential control variables. The goal is to isolate the effect of the first-mover’s reputation, as proxied by their `Performance Score`, on the hazard rate of a peer executing a similar transaction.

#### **1. Full Model Specification**

For each of the nine first-mover events, a CPH model will be estimated. The hazard function `h(t)` for a peer investor to follow the first-mover's action at time `t` is specified as:

`h(t | X) = h₀(t) * exp(β₁*FirstMover_PS + β₂*Peer_PS + β₃*Portfolio_Overlap + β₄*FirstMover_Txn_Size_Norm + β₅*Market_Volatility + β₆*Peer_Centrality)`

The estimation of this model for each cascade event will yield the coefficients (`β`) that quantify the impact of each variable on the instantaneous probability of a peer following the action, conditional on them not having followed yet.

#### **2. Primary Independent Variable: First-Mover Success**

*   **`FirstMover_PS`**: This variable represents the pre-calculated `Performance Score` of the identified first-mover for the specific event window. It is the central variable of interest in the model. The primary objective is to estimate its coefficient, `β₁`, and test its statistical significance. A positive and statistically significant `β₁` would imply that a higher `Performance Score` for the first-mover is associated with an increased hazard rate for their peers. The corresponding Hazard Ratio, `exp(β₁)`, would quantify this effect: for each one-unit increase in the first-mover's `Performance Score`, the rate of peer-following increases by `(exp(β₁) - 1) * 100%`. This would provide direct evidence in support of hypothesis H1b, suggesting that peer actions are influenced by the perceived quality and historical success of the leader.

#### **3. Control Variables**

To isolate the effect of `FirstMover_PS` and mitigate the risk of omitted variable bias, the following control variables must be included in the model. These controls account for alternative explanations for the observed peer behavior.

*   **`Peer_PS`**: The peer's own `Performance Score`. This is a critical control to distinguish influence from homophily or independent action. It is plausible that high-performing peers act similarly not because they are following, but because their own high-quality analysis leads them to the same conclusion. Including this variable allows us to separate the effect of being influenced from the effect of simply being a skilled investor.

*   **`Portfolio_Overlap`**: The Jaccard similarity index of fund investments between the first-mover and the peer, calculated over the five-year lookback period. This controls for the strength of the informational tie. A higher portfolio overlap implies that the two investors share more common information channels (e.g., same GPs, same fund reports). A significant coefficient on this variable would suggest that the *structure* of the network channel is important, independent of the leader's reputation.

*   **`FirstMover_Txn_Size_Norm`**: The size of the first-mover's transaction, normalized by the first-mover's total AUM or total commitments to that asset class. This controls for the strength of the initial signal. A larger, more significant transaction may be more likely to be noticed and acted upon, irrespective of the actor's historical performance. Normalization is crucial to ensure comparability across investors of different scales.

*   **`Market_Volatility`**: A measure of general market stress during the period of the first-mover's action. This will be operationalized as the average value of the CBOE Volatility Index (VIX) over the five trading days leading up to and including the day of the first-mover's transaction (`T_min`). This variable controls for the possibility that cascades are driven by broad market panic rather than specific informational signals from a leader.

*   **`Peer_Centrality`**: The degree centrality of the peer investor within the co-investment network graph for that period. This controls for the peer's own embeddedness and general access to information. A highly central peer may receive information from many sources, and their action to "follow" may be a response to a different signal entirely.

#### **4. Required Output for Hypothesis Validation**

The successful execution of this analysis requires the generation of a standard regression output table for each of the nine fitted CPH models. This table will serve as the primary evidence for evaluating the research hypotheses. The table must contain the following columns for each variable in the model:

| Variable                     | Coefficient (β) | Hazard Ratio (exp(β)) | Std. Error (SE) | z-value | p-value (P>|z|) |
| ---------------------------- | --------------- | --------------------- | --------------- | ------- | ---------------- |
| `FirstMover_PS`              |                 |                       |                 |         |                  |
| `Peer_PS`                    |                 |                       |                 |         |                  |
| `Portfolio_Overlap`          |                 |                       |                 |         |                  |
| `FirstMover_Txn_Size_Norm`   |                 |                       |                 |         |                  |
| `Market_Volatility`          |                 |                       |                 |         |                  |
| `Peer_Centrality`            |                 |                       |                 |         |                  |

The key result for validating H1b is a `p-value` for `FirstMover_PS` that is below the conventional significance threshold (e.g., p < 0.05) and a `Coefficient (β)` that is positive. This combination would provide statistically significant evidence that a first-mover's historical success positively predicts the rate at which their network peers follow their actions during economic shocks.