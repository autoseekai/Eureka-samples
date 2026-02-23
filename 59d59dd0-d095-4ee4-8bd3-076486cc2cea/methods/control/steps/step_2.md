### **4. Population Generation and Group Assignment**

The simulation will be instantiated with a synthetic cohort of students whose initial academic proficiency levels are heterogeneous, mirroring a typical classroom or school-level distribution.

**Initial Population Characteristics:**
A cohort of `N` students will be generated. Each student `i` is assigned an initial score, `Score_i(0)`, representing their proficiency at the start of the simulation (`t=0`). These scores are drawn from a truncated normal distribution to ensure they are within a plausible range.

The procedure is as follows:
1.  Generate `N` values from a normal distribution with a specified mean (`μ_initial`) and standard deviation (`σ_initial`).
2.  Any generated score below 0 is set to 0.
3.  Any generated score above the `MasteryCeiling` is set to the `MasteryCeiling`.

This process creates an initial score distribution, `Score(0)`, that is centered around the population average but includes variability, with tails representing lower and higher-achieving students. Furthermore, to introduce realistic individual differences in learning capacity, each student `i` will be assigned a unique baseline learning rate, `LR_base_i`. These values will be drawn from a separate normal distribution with a mean `μ_LR` and a small standard deviation `σ_LR`, truncated at a minimum of zero to prevent negative learning rates.

**Definition of the 'Low-Achiever' Group:**
For the purpose of targeted intervention, we must operationally define the 'Low-Achiever' group. This group is identified based on their initial proficiency prior to any intervention. The 'Low-Achiever' group consists of all students whose initial score, `Score_i(0)`, falls at or below the 25th percentile of the `Score(0)` distribution for the entire cohort. This criterion establishes a clear, data-driven threshold for inclusion in the targeted intervention scenario. The size of this group will be approximately `0.25 * N`.

### **5. Simulation Scenarios**

To evaluate the differential impact of the intervention, we will execute two distinct simulation scenarios. Both scenarios will use the same initial population of `N` students, with identical `Score(0)` and `LR_base_i` values, to ensure a controlled comparison.

*   **Scenario A: Targeted Intervention.** In this scenario, the intervention is administered exclusively to the students identified as 'Low-Achievers'. These students form the **Treatment Group**. The remaining students (those with `Score(0)` above the 25th percentile) receive no intervention and form the **Control Group**. Their learning trajectory will be governed solely by their `LR_base_i`.

*   **Scenario B: General Population Intervention (RCT Simulation).** This scenario simulates a standard Randomized Controlled Trial (RCT) conducted on the general population. A **Treatment Group** is formed by randomly selecting a subset of students from the *entire* cohort of `N` students. The size of this randomly selected group will be identical to the size of the 'Low-Achiever' group from Scenario A (i.e., `~0.25 * N`). The remaining students in the cohort form the **Control Group**. This design allows us to measure the intervention's effect size when applied to a representative, rather than a targeted, sample of the student population.

### **6. Simulation Parameters**

The following parameters will be held constant across all simulation runs for both scenarios to ensure comparability of the results.

*   **Number of Students (`N`)**: 1,000
*   **Number of Time Steps (`T`)**: 20 (e.g., representing 20 weeks of instruction)
*   **Mastery Ceiling**: 100
*   **Initial Score Distribution Mean (`μ_initial`)**: 50
*   **Initial Score Distribution SD (`σ_initial`)**: 15
*   **Base Learning Rate Mean (`μ_LR`)**: 0.05
*   **Base Learning Rate SD (`σ_LR`)**: 0.01
*   **Intervention Boost (`Boost`)**: 0.15
*   **Intervention Decay Rate (`DecayRate`)**: 0.25