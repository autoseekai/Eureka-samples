### **Methodology: First-Mover Identification and Consistency Classification**

This section specifies the computational algorithm designed to systematically identify the "first-mover" for each defined transaction behavior within each economic shock window. It also establishes the criteria for classifying an investor as a "consistent first-mover" across the series of analyzed events.

#### **1. First-Mover Identification Algorithm**

The following step-by-step procedure will be executed to pinpoint the initiating investor for a given behavior in a specific crisis period.

**Inputs:**
*   **Event-Specific Transaction Datasets:** Three distinct datasets, one for each shock (`GFC`, `Eurozone`, `COVID`), containing all classified transactions (`Significant Secondary Sale`, `New Relationship Commitment`, `Default Event`). Each record includes `Investor_ID`, `Transaction_Type`, `Relative_Day`, and `Transaction_Amount`.
*   **Investor Performance Scores:** The pre-calculated `PS_i` (Performance Score) for each `Investor_ID` at the start of each of the three event windows.

**Procedure:**
The algorithm will be run independently for each combination of the three economic shocks and the three defined transaction types (a total of 9 iterations).

1.  **Initialization:**
    *   Select one economic shock event window (e.g., `GFC`).
    *   Select one transaction type (e.g., `Significant Secondary Sale`).
    *   Create a temporary data subset containing only transactions that match the selected event and type.

2.  **Identify Earliest Action Day:**
    *   From the temporary data subset, find the minimum value of `Relative_Day`. This value, `T_min`, represents the first day within the event window that the specified transaction type occurred.

3.  **Isolate Potential First-Movers:**
    *   Filter the temporary data subset to create a "Candidates List" containing all transactions that occurred on `T_min`.

4.  **Apply Tie-Breaking Protocol:**
    *   **Condition A (Single Actor):** If the "Candidates List" contains only one transaction, the corresponding `Investor_ID` is declared the First-Mover.
    *   **Condition B (Multiple Actors):** If the "Candidates List" contains multiple transactions (i.e., several investors acted on the same day `T_min`), the tie is resolved based on historical performance.
        *   Retrieve the pre-calculated `PS_i` for each `Investor_ID` in the "Candidates List" for the current event window.
        *   The investor with the highest `PS_i` is designated as the First-Mover. This rule is based on the hypothesis that the investor with the strongest historical track record is the true informational leader, even in cases of chronologically simultaneous actions.
        *   In the rare event of an identical `PS_i` score among top candidates, the tie will be broken by selecting the investor with the larger `Transaction_Amount`.

5.  **Record Output:**
    *   The identified `Investor_ID` is recorded as the First-Mover for the specific combination of event and transaction type. This process is repeated until a First-Mover has been identified for all 9 event-transaction scenarios. The results will be stored in a summary table, `FirstMoverResults`, with columns `[Event, TransactionType, FirstMover_ID]`.

#### **2. Classification of Consistent First-Movers**

After the identification algorithm has been executed for all scenarios, the `FirstMoverResults` table will be analyzed to identify investors who exhibit leadership behavior repeatedly.

**Definition of Consistency:**
An investor is classified as a **"Consistent First-Mover"** if they are identified as the First-Mover for the *same transaction type* in **at least two of the three** analyzed economic shock events (GFC, Eurozone Crisis, COVID-19).

**Classification Procedure:**
1.  Group the `FirstMoverResults` table by `TransactionType` and `FirstMover_ID`.
2.  Count the number of occurrences for each `(TransactionType, FirstMover_ID)` pair.
3.  Any pair with a count of 2 or greater identifies a Consistent First-Mover. The corresponding `FirstMover_ID` is added to a final list, `ConsistentFirstMovers`, noting the specific behavior (e.g., "Investor 123 is a Consistent First-Mover for Significant Secondary Sales"). This list of consistently leading investors forms the primary subject for the subsequent cascade and influence analysis.