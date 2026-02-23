### **9. Analysis of Simulation Outcomes**

The analysis phase is designed to quantify and visualize the differential impact of the intervention under the two distinct targeting strategies. The primary goal is to evaluate the magnitude and temporal dynamics of the treatment effect in both Scenario A and Scenario B.

#### **9.1 Primary Outcome Measure: Cohen's d Effect Size**

The principal outcome measure for this study is the effect size, calculated at each time point `t > 0`. We will use Cohen's d, a standardized measure of the difference between two group means, to quantify the intervention's impact. This allows for a standardized comparison of effect magnitudes across different time points and between the two scenarios.

For each scenario (A and B) and for each time step `t` from 1 to 20, Cohen's d will be calculated using the following formula:

`d(t) = (Mean_Score_Treatment(t) - Mean_Score_Control(t)) / Pooled_SD(t)`

Where:
*   `Mean_Score_Treatment(t)` is the average score of the treatment group at time `t`.
*   `Mean_Score_Control(t)` is the average score of the control group at time `t`.
*   `Pooled_SD(t)` is the pooled standard deviation of the scores of the treatment and control groups at time `t`. It is calculated as:
    `sqrt(((n_treat - 1) * SD_treat(t)^2 + (n_ctrl - 1) * SD_ctrl(t)^2) / (n_treat + n_ctrl - 2))`
    where `n` is the number of students and `SD` is the standard deviation for the respective group at time `t`.

This calculation will produce two time-series of effect sizes, one for the targeted intervention and one for the general population RCT.

#### **9.2 Primary Visualization: Effect Size Trajectories**

The central output of the analysis will be a line plot of 'Effect Size vs. Time'. This visualization is critical for illustrating the dynamic nature of the intervention's impact. The plot will be constructed as follows:
*   **X-axis**: Time Step, ranging from `t=1` to `t=20`.
*   **Y-axis**: Cohen's d Effect Size.
*   **Lines**: The plot will contain two distinct lines, each clearly labeled:
    1.  **Targeted Intervention (Scenario A)**: This line will plot the sequence of Cohen's d values calculated for Scenario A at each time step.
    2.  **General Population (Scenario B)**: This line will plot the sequence of Cohen's d values calculated for Scenario B at each time step.

This visualization will directly compare how the measured effect size evolves over time under the two different targeting strategies.

#### **9.3 Secondary Visualization: Learning Trajectories**

To provide context for the effect size dynamics, a secondary visualization will plot the raw learning trajectories of the different groups. This line plot of 'Average Score vs. Time' will display the underlying data that drives the effect size calculations.
*   **X-axis**: Time Step, ranging from `t=0` to `t=20`.
*   **Y-axis**: Average Score.
*   **Lines**: The plot will display four separate lines, representing the mean score of each subgroup over time:
    1.  Scenario A: Treatment Group (Targeted Low-Achievers)
    2.  Scenario A: Control Group (Non-Low-Achievers)
    3.  Scenario B: Treatment Group (Random Sample)
    4.  Scenario B: Control Group (Random Sample)

This plot is essential for visualizing the "catch-up" phenomenon in Scenario A and the influence of the mastery ceiling on different groups.

#### **9.4 Hypothesis Evaluation**

The final step of the analysis is the direct test of the project's central hypothesis. Using the data generated for the primary visualization, the analysis must explicitly identify the peak effect size for each scenario.
1.  For the Scenario A effect size trajectory, find the maximum Cohen's d value and the time point `t_peak_A` at which it occurs.
2.  For the Scenario B effect size trajectory, find the maximum Cohen's d value and the time point `t_peak_B` at which it occurs.

The evaluation will consist of a direct comparison of these peak values. The hypothesis—that interventions on low-achievers yield larger effect sizes—will be supported if the peak effect size observed in Scenario A is substantially greater than the peak effect size observed in Scenario B.