<div align="right">
  <a href="./README.zh-CN.md">中文</a> | <b>English</b>
</div>

<div align="center">

# 🌌 Eureka

**Real outputs from Eureka × AutoSeek — Explore More. Discover More.**

[![Live Demo](https://img.shields.io/badge/🚀_Try_Live_Demo-go.eureka--ai.top-6366f1?style=for-the-badge)](https://go.eureka-ai.top)
[![Framework](https://img.shields.io/badge/Powered_by-CrewAI-f59e0b?style=for-the-badge)](https://github.com/crewAIInc/crewAI)
[![AutoSeek](https://img.shields.io/badge/AutoSeek-✅_Live-22c55e?style=for-the-badge)](https://go.eureka-ai.top)
[![Eureka](https://img.shields.io/badge/Eureka_Full-🔧_In_Development-f59e0b?style=for-the-badge)](#)

<br/>

> Every research report in this repository was completed entirely by AI —
> **no human intervention, no preset conclusions. Just data, an objective, and autonomous reasoning.**

<br/>

**[🚀 Try Live Demo](https://go.eureka-ai.top) · [📖 How It Works](#-how-it-works) · [📂 Browse Samples](#-samples)**

</div>

---

## What is This Repository?

**Eureka-Samples** is a curated collection of real, end-to-end research outputs
produced by the [Eureka × AutoSeek](https://go.eureka-ai.top) platform.

Each sample is an unedited record of a complete autonomous discovery run:
from hypothesis generation, through methodology design,
to data analysis code execution and interpretation —
all performed independently by a multi-agent AI system.
**This is real capability, not a hand-crafted demo.**

---

## 🔬 How It Works

Eureka completes a full research cycle through three strictly sequential autonomous phases:

```
flowchart TD
    INPUT["📥 You provide: Research Objective + Dataset"]

    INPUT --> IDEA
    IDEA["💡 Phase 1 · Idea<br/>AI generates & refines hypotheses via adversarial debate"]

    IDEA -->|Hypothesis Report| METHOD
    METHOD["📐 Phase 2 · Method<br/>AI designs a systematic research methodology (~500 words)"]

    METHOD -->|Methodology Document| EXPERIMENT
    EXPERIMENT["🧪 Phase 3 · Experiment<br/>AI writes code, executes analysis, interprets results"]

    EXPERIMENT --> OUTPUT
    OUTPUT["📄 Full Research Report (academic style, ~2000 words)"]

    style INPUT     fill:#6366f1,color:#fff,stroke:none
    style IDEA      fill:#f59e0b,color:#fff,stroke:none
    style METHOD    fill:#009688,color:#fff,stroke:none
    style EXPERIMENT fill:#3b82f6,color:#fff,stroke:none
    style OUTPUT    fill:#22c55e,color:#fff,stroke:none
```

Each phase is executed by a dedicated crew of AI agents:
**Planner · Engineer · Reviewer · RAG Researcher**

---

## 📂 Samples

Each directory corresponds to one complete research run, named by its unique task ID.

---

### 📘 Sample 1 · Temporal Dynamics of Educational Interventions

> **Domain**: Education / Quantitative Social Science | **Language**: English

**Research Hypothesis (Phase 1 Output)**

> *Catching Up and Leveling Off: A Dynamic Simulation of How Temporary Learning
> Rate Boosts Generate Larger Effects for Low-Achievers*
>
> We hypothesize that interventions targeting foundational learning skills produce
> disproportionately large effects for low-achievers by temporarily boosting their
> learning rate. Simulation results are expected to show that the intervention effect
> is not static — it peaks at an intermediate time point before declining due to
> effect decay and mastery ceiling effects, a dynamic that traditional pre-post
> designs fundamentally fail to capture.

<div align="center">
  <img src="./assets/g1.gif" alt="Eureka Demo" width="800"/>
</div>
📁 [`59d59dd0-d095-4ee4-8bd3-076486cc2cea/`](./59d59dd0-d095-4ee4-8bd3-076486cc2cea/)

---

### 📗 Sample 2 · The Matching Effect of Personalized Educational Interventions

> **Domain**: Education / Precision Learning | **Language**: Chinese

**Research Hypothesis (Phase 1 Output)**

> *The Gain of Personalization: Quantifying the Matching Effect of Educational
> Interventions via Mechanistic Simulation*
>
> This study builds a mechanistic simulation model to quantify the superiority of a
> "diagnose-and-match" intervention strategy over a one-size-fits-all approach.
> Student achievement is driven by dual latent factors (knowledge and motivation)
> with interaction effects, allowing the matching advantage to emerge organically
> from the model. Results are expected to clearly quantify the "Matching Gain" and
> provide a theoretical basis for shifting educational practice toward precision support.

<div align="center">
  <img src="./assets/2.gif" alt="Eureka Demo" width="800"/>
</div>
📁 [`782496e4-6b3d-4934-a1e9-a4ef00b60b0a/`](./782496e4-6b3d-4934-a1e9-a4ef00b60b0a/)

---

### 📙 Sample 3 · First-Mover Dynamics in Private Equity Markets

> **Domain**: Finance / Behavioral Economics | **Language**: English

**Research Hypothesis (Phase 1 Output)**

> *First-Mover Dynamics: Quantifying Informational Cascades and Network Leadership
> in Private Equity Investing*
>
> This study investigates whether transaction behavior among sophisticated private equity
> investors during economic crises is driven by rational informational cascades rather
> than irrational herding. Using event-based relative timing analysis within
> co-investment networks, we identify consistent "first-movers" and test whether
> peer follow-through probability is a function of the first-mover's historical
> success — offering a new framework for risk management in opaque markets.

<div align="center">
  <img src="./assets/3.gif" alt="Eureka Demo" width="800"/>
</div>
📁 [`e6ee99f8-1e6c-47d6-ac64-c9d584efad23/`](./e6ee99f8-1e6c-47d6-ac64-c9d584efad23/)

---

## 📁 Sample Directory Structure

Each sample directory preserves the **complete raw artifacts** of that research run:

```
<task-id>/
├── idea/
│   ├── result.md          # ✦ Final hypothesis report (paper title + abstract)
│   ├── plan/              # Planner's task decomposition
│   └── control/           # Per-round agent execution logs
│
├── methods/
│   ├── result.md          # ✦ Full methodology document (~500 words)
│   ├── plan/
│   └── control/
│
└── experiment/
    ├── result.md          # ✦ Full research results report (~2000 words)
    ├── plan/
    └── control/           # AI-generated Python code and execution output
```

> **`result.md` is the final deliverable of each phase.**
> The `plan/` and `control/` folders preserve the AI's full reasoning
> and execution trace for inspection.

---

## 🚀 Try It Yourself

The **AutoSeek** execution engine is live and supports full end-to-end
autonomous research task execution.

<div align="center">

### **[→ Visit go.eureka-ai.top to start exploring](https://go.eureka-ai.top)**

</div>

Provide a research objective, upload your dataset — Eureka handles the rest.

---

## ℹ️ About Eureka × AutoSeek

| | AutoSeek 🔬 | Eureka 🌌 |
|---|---|---|
| **Role** | Single-task execution engine | Long-horizon discovery orchestrator |
| **Scope** | One question → one structured answer | One objective → multi-cycle → full report |
| **State** | Stateless per run | Persistent world model across cycles |
| **Status** | ✅ Live at [go.eureka-ai.top](https://go.eureka-ai.top) | 🔧 In active development |

---

<div align="center">

Built with [CrewAI](https://github.com/crewAIInc/crewAI) · FastAPI · Vue 3

© 2025 QIMING HU · All Rights Reserved

</div>
