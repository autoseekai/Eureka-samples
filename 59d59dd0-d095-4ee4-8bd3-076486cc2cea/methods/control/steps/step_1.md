### **1. Conceptual Model of Student Learning**

The foundation of this simulation is a dynamic model of student learning that captures individual growth trajectories over discrete time steps. We conceptualize learning not as a linear accumulation of knowledge, but as a process of closing the gap between current proficiency and a state of mastery. This is best represented by a discrete-time logistic growth model, often referred to as an S-curve. This model inherently accounts for the principle of diminishing returns, where the rate of learning is fastest when a student is far from mastery and slows as they approach it.

The core equation governing a student's score progression from one time step (`t`) to the next (`t+1`) is defined as:

`Score(t+1) = Score(t) + LearningRate * (MasteryCeiling - Score(t))`

In this formulation, the term `(MasteryCeiling - Score(t))` represents the remaining "potential for growth." The `LearningRate` parameter acts as a proportional constant that determines how much of that potential is realized in a single time step.

### **2. Model Parameters and Definitions**

To operationalize the simulation, we define the following parameters:

*   **`Score(t)`**: This variable represents a student's measured academic proficiency at a given time step `t`. Scores are continuous and bounded by `0` and the `MasteryCeiling`. This serves as the primary outcome variable in our model.

*   **`MasteryCeiling`**: This is a constant representing the maximum possible score or proficiency level within the educational domain being modeled (e.g., 100 on a standardized test). It acts as the asymptote for the logistic growth function, ensuring that scores cannot increase indefinitely. For this simulation, it is fixed at 100.

*   **`LearningRate`**: This is the most critical dynamic parameter, representing the efficiency with which a student converts their potential for growth into actual score gains. It is not a fixed attribute but is composed of a baseline individual trait and a time-dependent component influenced by the intervention.

*   **`t`**: This represents the discrete time steps of the simulation. Each step can be conceptualized as a unit of learning, such as a week or a month, over which instruction and practice occur and scores can change. The intervention's effects are modeled as a function of time elapsed since its application.

### **3. Mathematical Formulation of the Intervention Effect**

The central hypothesis is that the educational intervention provides a temporary boost to a student's learning efficiency. We model this by defining the `LearningRate` as a function of time for students in the treatment group. For an untreated student, the learning rate is simply their baseline rate, `LR_base`. For a treated student, the learning rate at time `t` post-intervention is enhanced by a boost that decays exponentially over time.

The full equation for the learning rate of a treated student is:

`LearningRate(t) = LR_base + Boost * exp(-DecayRate * t)`

The components of this equation are:

*   **`LR_base`**: The student's intrinsic or baseline learning rate. This parameter captures the stable, underlying differences in learning speed between individuals in the absence of the specific intervention.

*   **`Boost`**: This parameter represents the initial magnitude of the increase in the learning rate conferred by the intervention at `t=0`. It quantifies the maximum instantaneous impact of the program on a student's ability to learn.

*   **`DecayRate`**: This parameter controls how quickly the intervention's effect fades. A `DecayRate` of zero would imply a permanent effect, while a larger `DecayRate` signifies a more transient effect, causing the `LearningRate(t)` to revert more rapidly towards the student's `LR_base`. This exponential decay models the common phenomenon where the skills or motivational benefits gained from a short-term program diminish as students return to their normal classroom environment.