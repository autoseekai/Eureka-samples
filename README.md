<div align="center">

# 🌌 Eureka × AutoSeek

**Autonomous Scientific Discovery, Powered by Pareto-Guided World Models**

[![Demo](https://img.shields.io/badge/🚀_Live_Demo-go.eureka--ai.top-6366f1?style=for-the-badge)](https://go.eureka-ai.top)
[![Framework](https://img.shields.io/badge/Framework-CrewAI-f59e0b?style=for-the-badge)](https://github.com/crewAIInc/crewAI)
[![Python](https://img.shields.io/badge/Python-3.11+-3b82f6?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org)
[![License](https://img.shields.io/badge/License-MIT-10b981?style=for-the-badge)](LICENSE)
[![AutoSeek](https://img.shields.io/badge/AutoSeek-Live-22c55e?style=for-the-badge)](https://go.eureka-ai.top)
[![Eureka](https://img.shields.io/badge/Eureka-In_Development-f59e0b?style=for-the-badge)](#)

<br/>

*Give it a research objective and a dataset.*  
*It reads papers, writes analysis code, forms hypotheses,*  
*and delivers a fully traceable scientific report — autonomously.*

<br/>

**[🚀 Try Live Demo](https://go.eureka-ai.top) · [📖 How It Works](#how-it-works) · [⚙️ Architecture](#architecture) · [📊 Why Pareto](#why-pareto)**

</div>

---

## Table of Contents

- [Overview](#overview)
- [The Two Projects](#the-two-projects)
- [How It Works](#how-it-works)
- [Architecture](#architecture)
- [Why Pareto?](#why-pareto)
- [Design Principles](#design-principles)
- [Tech Stack](#tech-stack)
- [Development Status](#development-status)

---

## Overview

**Eureka × AutoSeek** is a two-layer autonomous research system:

<video src="https://github.com/user-attachments/assets/a6de70db-fcc0-41d3-9417-ad05e0b08115" 
       width="100%" controls autoplay muted loop>
</video>


| | AutoSeek 🔬 | Eureka 🌌 |
|---|---|---|
| **What it does** | Executes one focused research task end-to-end | Orchestrates many tasks into a long-horizon discovery run |
| **Scope** | One question → one structured answer | One objective → many cycles → scientific report |
| **State** | Stateless between runs | Persistent World Model across all cycles |
| **Status** | ✅ Live at [go.eureka-ai.top](https://go.eureka-ai.top) | 🔧 In active development |

---

## The Two Projects

### 🔬 AutoSeek — The Execution Engine `✅ Live`

A **CrewAI-powered multi-agent framework** that takes a single focused
research question and answers it completely — planning, coding, reviewing,
and retrieving literature — without human intervention.

**Agent crew:**

| Agent | Role |
|---|---|
| 🗺️ **Planner** | Decomposes the question into executable sub-steps |
| 💻 **Coder** | Writes and runs Python analysis code |
| 🔍 **Reviewer** | Checks results for errors and logical consistency |
| 📚 **RAG Agent** | Retrieves and synthesizes relevant literature |

**Every run outputs a structured JSON block:**

```json
{
  "claim": "A single falsifiable statement summarizing the finding",
  "confidence": 0.87,
  "novelty": 0.72,
  "relevance": 0.95,
  "sources": ["notebook:analysis_v2.ipynb:cell_14", "paper:doi:10.xxxx"],
  "key_numbers": { "p_value": 0.003, "effect_size": 0.41 },
  "follow_up_questions": ["What is the mechanism?", "Does this generalize?"]
}
