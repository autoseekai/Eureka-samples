### **7. Simulation Execution and Data Generation**

The core of the simulation involves generating the learning trajectory for each of the `N` students over `T` time steps. This process is executed independently for Scenario A (Targeted Intervention) and Scenario B (General Population Intervention), using the identical initial population (`t=0`) for both.

The simulation begins with the instantiation of the student population as defined by the parameters in Section 6. A data structure is created to hold the state of each of the `N=1,000` students at `t=0`. This initial state includes a unique `student_id`, the assigned `initial_score` (drawn from the specified truncated normal distribution), and the student's intrinsic `base_learning_rate` (`LR_base_i`).

For each scenario, group assignments are made at `t=0`.
*   In **Scenario A**, the 25th percentile of the `initial_score` distribution is calculated. All students with scores at or below this threshold are assigned to the 'Treatment' group. All other students are assigned to the 'Control' group.
*   In **Scenario B**, a random sample of `250` students (equivalent to 25% of `N`) is drawn from the entire population to form the 'Treatment' group. The remaining `750` students constitute the 'Control' group.

The simulation then proceeds iteratively from `t=1` to `T=20`. For each time step `t`, a new score, `Score_i(t)`, is calculated for every student `i` based on their score at the previous time step, `Score_i(t-1)`.

The calculation for `Score_i(t)` depends on the student's group assignment:

1.  **Determine the effective Learning Rate, `LR_effective_i(t)`:**
    *   For any student `i` in the **Control Group** (in either scenario), the learning rate is constant:
        `LR_effective_i(t) = LR_base_i`
    *   For any student `i` in the **Treatment Group** (in either scenario), the learning rate is enhanced by the intervention's decaying boost. The time elapsed since the intervention began is `t-1`.
        `LR_effective_i(t) = LR_base_i + Boost * exp(-DecayRate * (t-1))`

2.  **Calculate the potential new score:** The score update is performed using the discrete-time logistic growth model:
    `PotentialScore_i(t) = Score_i(t-1) + LR_effective_i(t) * (MasteryCeiling - Score_i(t-1))`

3.  **Apply the Mastery Ceiling:** Student proficiency cannot exceed the maximum possible score. Therefore, the final score for the time step is capped at the `MasteryCeiling`:
    `Score_i(t) = min(PotentialScore_i(t), MasteryCeiling)`

This three-step process is repeated for every student across all 20 time steps.

The results of the entire simulation process for both scenarios must be stored in a single, long-format data table. This structure is essential for subsequent analysis and visualization. The table will contain one row for each student at each time step, resulting in `N * (T+1)` rows for each scenario. The required columns are:

*   `scenario`: A categorical variable indicating the simulation run ('A_Targeted' or 'B_General_RCT').
*   `student_id`: A unique identifier for each student (from 1 to 1,000).
*   `time_step`: An integer representing the time point (from 0 to 20).
*   `group`: A categorical variable indicating the student's assignment ('Treatment' or 'Control').
*   `base_lr`: The student's intrinsic baseline learning rate, `LR_base_i`.
*   `score`: The calculated proficiency score of the student at that specific time step.