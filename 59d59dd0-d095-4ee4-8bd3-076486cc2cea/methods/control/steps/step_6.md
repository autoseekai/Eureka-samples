### **Methodology**

This study employs a computational simulation to investigate the hypothesis that educational interventions targeting foundational skills produce larger effect sizes when administered to low-achieving students compared to a general student population. The simulation models individual student learning trajectories over time, incorporating a temporary, decaying boost to learning rates for treated students, all constrained by a mastery ceiling. The methodology is designed to generate data for two distinct scenarios—a targeted intervention and a general population randomized controlled trial (RCT)—to allow for a direct comparison of the resulting effect size dynamics.

#### **Simulation Model**

The model is founded on a discrete-time logistic growth equation, which posits that a student's score gain in a given time step is proportional to their remaining potential for growth. The score for student `i` at time `t+1` is updated from their score at time `t` as follows:

`Score_i(t+1) = Score_i(t) + LR_effective_i(t) * (MasteryCeiling - Score_i(t))`

Here, `MasteryCeiling` is the maximum achievable score (fixed at 100), and `(MasteryCeiling - Score_i(t))` represents the learning potential. The `LR_effective_i(t)` is the student's effective learning rate at time `t`, which is the key dynamic component.

For untreated students, the learning rate is their constant baseline learning rate, `LR_base_i`. For treated students, the intervention provides a temporary enhancement that decays exponentially over time. The effective learning rate for a treated student `i` at time `t` (where `t=1` is the first step post-intervention) is given by:

`LR_effective_i(t) = LR_base_i + Boost * exp(-DecayRate * (t-1))`

The parameters are defined as:
*   **`LR_base_i`**: The student's intrinsic baseline learning rate.
*   **`Boost`**: The initial magnitude of the learning rate increase from the intervention.
*   **`DecayRate`**: The rate at which the intervention's effect diminishes over time.

#### **Experimental Design**

The simulation will be populated with a cohort of `N=1,000` students over `T=20` time steps. Each student is characterized by an initial score, `Score_i(0)`, drawn from a truncated normal distribution (μ=50, σ=15), and a unique baseline learning rate, `LR_base_i`, drawn from a normal distribution (μ=0.05, σ=0.01).

Two distinct experimental scenarios will be executed using this identical initial population:

*   **Scenario A: Targeted Intervention.** The 'Low-Achiever' group is defined as all students whose initial score `Score_i(0)` falls at or below the 25th percentile of the initial score distribution. In this scenario, these low-achievers constitute the **Treatment Group**. All other students form the **Control Group** and receive no intervention.

*   **Scenario B: General Population Intervention.** This scenario simulates a standard RCT. A **Treatment Group** is formed by randomly selecting a number of students from the entire population equal to the size of the low-achiever group in Scenario A (~250 students). The remaining students form the **Control Group**.

The following parameters are held constant across both scenarios: `MasteryCeiling=100`, `Boost=0.15`, and `DecayRate=0.25`.

#### **Simulation Procedure**

Data generation involves executing the simulation for both scenarios. For each scenario, group assignments are made at `t=0`. The simulation then iterates from `t=1` to `t=20`, calculating a new score for each student at each time step.

1.  **Group Assignment**: In Scenario A, students are assigned to Treatment/Control groups based on the 25th percentile `Score(0)` threshold. In Scenario B, students are assigned to Treatment/Control groups via random sampling from the full cohort.
2.  **Iterative Score Calculation**: For each time step `t` from 1 to 20, and for each student `i`:
    a.  The `LR_effective_i(t)` is determined based on the student's group assignment and the elapsed time.
    b.  The `Score_i(t)` is calculated using the logistic growth equation.
    c.  The final score is capped at the `MasteryCeiling`: `Score_i(t) = min(Score_i(t), MasteryCeiling)`.
3.  **Data Storage**: The results for both scenarios are compiled into a single long-format data table. Each row represents a single student at a single time step and includes columns for `scenario`, `student_id`, `time_step`, `group`, `base_lr`, and `score`.

#### **Analysis and Visualization**

The analysis will focus on quantifying and comparing the treatment effect over time for both scenarios.

1.  **Effect Size Calculation**: The primary outcome is the effect size, measured by Cohen's d at each time step `t` from 1 to 20 for each scenario. It is calculated as the difference in mean scores between the treatment and control groups, divided by their pooled standard deviation. This yields two time-series of effect sizes: one for the targeted intervention (Scenario A) and one for the general population RCT (Scenario B).

2.  **Visualization**:
    *   **Primary Plot**: An 'Effect Size vs. Time' line plot will be generated, displaying the two Cohen's d trajectories on the same axes for direct comparison. This plot is intended to visualize the central hypothesis, showing when and by how much the effect sizes differ.
    *   **Secondary Plot**: An 'Average Score vs. Time' line plot will visualize the raw learning trajectories for the four key subgroups (Treatment/Control for both Scenario A and B). This provides context for the "catch-up" growth and ceiling effects that drive the effect size dynamics.

3.  **Hypothesis Evaluation**: The hypothesis that targeted interventions on low-achievers yield larger effects will be evaluated by identifying and comparing the peak Cohen's d value achieved in Scenario A against the peak value achieved in Scenario B. A substantially larger peak effect size in Scenario A will provide support for the hypothesis.