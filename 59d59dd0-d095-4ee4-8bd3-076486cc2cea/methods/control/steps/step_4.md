### **8. Execution of Scenario B: General Population RCT Simulation**

This section details the execution of the second simulation arm, which models a traditional Randomized Controlled Trial (RCT) applied to the general student population. The primary objective is to generate a parallel dataset that serves as a benchmark for the effect size observed in a non-targeted intervention.

#### **8.1 Population Replication and Random Assignment**

To ensure a valid comparison, the simulation for Scenario B must begin with the exact same initial student population generated for Scenario A. This is achieved by re-initializing the simulation using the identical random seed used to generate the `N=1,000` students at `t=0`. Consequently, every student `i` in Scenario B starts with the same `initial_score` (`Score_i(0)`) and `base_learning_rate` (`LR_base_i`) as their counterpart in Scenario A. This control ensures that any divergence in outcomes between the two scenarios can be attributed exclusively to the difference in the intervention targeting strategy (low-achiever specific vs. random general population) rather than any underlying differences in the student cohorts themselves.

Following the population generation, group assignment is performed as follows:
1.  **Determine Treatment Group Size**: The number of students to be assigned to the treatment group is set to be equal to the size of the 'Low-Achiever' treatment group from Scenario A (i.e., the number of students whose initial scores fell at or below the 25th percentile, which is approximately 250).
2.  **Random Sampling**: A 'Treatment Group' is formed by drawing a random sample of this predetermined size from the *entire* population of 1,000 students. This procedure ensures that the treatment group is, on average, representative of the overall population's distribution of initial scores and learning rates.
3.  **Control Group Assignment**: The 'Control Group' consists of all remaining students who were not randomly selected for the treatment.

#### **8.2 Iterative Score Calculation Over Time**

The simulation proceeds iteratively from `t=1` to `T=20`. At each time step, the score for every student is updated according to their group assignment and the core learning model.

For each student `i` and each time step `t`, the score `Score_i(t)` is computed via a three-step process:

1.  **Determine Effective Learning Rate**: The student's effective learning rate, `LR_effective_i(t)`, is calculated.
    *   For a student in the randomly selected **Treatment Group**, the learning rate incorporates the decaying boost from the intervention:
        `LR_effective_i(t) = LR_base_i + Boost * exp(-DecayRate * (t-1))`
    *   For a student in the **Control Group**, the learning rate is simply their static baseline rate:
        `LR_effective_i(t) = LR_base_i`

2.  **Calculate Score Update**: The potential new score is calculated using the student's score from the previous time step and their effective learning rate.
    `PotentialScore_i(t) = Score_i(t-1) + LR_effective_i(t) * (MasteryCeiling - Score_i(t-1))`

3.  **Apply Mastery Ceiling Constraint**: The final score is capped at the `MasteryCeiling` to prevent scores from exceeding the maximum possible value. This constraint is crucial as it affects not only high-achieving students but also any student in the treatment group who experiences rapid growth.
    `Score_i(t) = min(PotentialScore_i(t), MasteryCeiling)`

#### **8.3 Data Structuring and Storage**

The output from this simulation run must be meticulously recorded and stored in the same long-format data table used for Scenario A. For each student at each time step (from `t=0` to `t=20`), a new row is generated. The `scenario` column for all data points generated in this run will be populated with the identifier 'B_General_RCT'. The `group` column will reflect the student's assignment to either the 'Treatment' or 'Control' group based on the random sampling process. All other columns (`student_id`, `time_step`, `base_lr`, `score`) will be populated as in the previous scenario. This unified data structure is essential for the subsequent comparative analysis, enabling a direct, time-point-by-time-point evaluation of the intervention's impact under different targeting strategies.