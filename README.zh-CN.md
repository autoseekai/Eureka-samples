<div align="right">
  🇨🇳 中文 &nbsp;|&nbsp; <a href="./README.md">🇺🇸 English</a>
</div>
<div align="center">

# 🌌 Eureka

**Real outputs from Eureka × AutoSeek — 探索不止，发现不断**

[![Live Demo](https://img.shields.io/badge/🚀_Try_Live_Demo-go.eureka--ai.top-6366f1?style=for-the-badge)](https://go.eureka-ai.top)
[![Framework](https://img.shields.io/badge/Powered_by-CrewAI-f59e0b?style=for-the-badge)](https://github.com/crewAIInc/crewAI)
[![AutoSeek](https://img.shields.io/badge/AutoSeek-✅_Live-22c55e?style=for-the-badge)](https://go.eureka-ai.top)
[![Eureka](https://img.shields.io/badge/Eureka_Full-🔧_In_Development-f59e0b?style=for-the-badge)](#)

<br/>

> 这里的每一份研究报告，都由 AI 从零开始独立完成——
> **没有人类干预，没有预设结论，只有数据、目标，和自主思考。**

<br/>

**[🚀 立即体验](https://go.eureka-ai.top) · [📖 了解工作原理](#-工作原理) · [📂 浏览样本](#-样本列表)**

</div>

---

## 这个仓库是什么？

**Eureka-Samples** 收录了 [Eureka × AutoSeek](https://go.eureka-ai.top) 平台真实运行产出的完整研究案例。

每个样本都是一次完整的自主科学发现过程的原始记录：从研究假设的生成，到方法论的设计，再到数据分析代码的编写与执行——全程由多智能体系统独立完成，**展示的是真实能力，而非精心筛选的演示**。

---

## 🔬 工作原理

Eureka 通过三个严格顺序执行的自主阶段完成一次完整的科学研究：


```
│
┌─────────▼──────────┐
│ Phase 1 · 💡 Idea │ AI 通过对抗式辩论生成并筛选最优研究假设
└─────────┬──────────┘
│ 假设报告
┌─────────▼────────────┐
│ Phase 2 · 📐 Method │ AI 设计系统性研究方法与实验规划（~500词）
└─────────┬────────────┘
│ 方法论文档
┌─────────▼──────────────────┐
│ Phase 3 · 🧪 Experiment │ AI 编写代码、执行分析、解读结果
└─────────┬──────────────────┘
│
完整研究结论报告（学术级，~2000词）
```

每个阶段均由专门的 AI Agent 协作完成：**Planner 规划员 · Engineer 工程师 · Reviewer 审查员 · RAG Researcher 检索研究员**。

---

## 🗺️ 路线图
- [x] **动态提示词路由** — 先根据用户输入与信号（例如是否提供数据集/CSV）动态选择一套提示词系统，然后仅在必要时动态丰富提示词（例如注入统计严谨性规则、因果主张警告、时序约束等）。
- [ ] **结构化世界模型** — 引入持久化世界模型，支持超长时间的研究运行，
      同时不丢失任何中间研究细节与上下文
- [ ] **索引与审查机制** — 添加自动化索引与质量检查层，
      使系统输出可直接用于发表的论文或研究报告

---
## 🚀 亲自体验

Eureka 的 AutoSeek 执行引擎目前已上线，支持单次完整研究任务的自主执行。

<div align="center">

### **[→ 前往 go.eureka-ai.top 开始探索](https://go.eureka-ai.top)**

</div>

输入你的研究目标，上传数据集，剩下的交给 Eureka。

---

## 📂 样本列表

仓库中的每个目录对应一次完整的研究运行，目录名为任务的唯一 ID。

---

### 📘 Sample 1 · 教育干预的时间动态效应

> **研究领域**：教育学 / 量化社会科学
> **语言**：English

**研究假设（Phase 1 输出）**

> *Catching Up and Leveling Off: A Dynamic Simulation of How Temporary Learning Rate Boosts Generate Larger Effects for Low-Achievers*
>
> 本研究假设：针对基础学习技能的干预措施，通过暂时提升低成就学生的学习速率，产生加速追赶效应。
> 模拟结果预期表明：干预效应并非静态，而是在中间时间点达到峰值后因效应衰减与掌握度上限的共同作用而下降，
> 这一峰值效应远超传统简单前后测设计所能捕捉的范围。

<div align="left">
  <img src="./assets/g1.gif" alt="Eureka Demo" width="800"/>
</div>
📁 [`59d59dd0-d095-4ee4-8bd3-076486cc2cea/`](./59d59dd0-d095-4ee4-8bd3-076486cc2cea/)

---

### 📗 Sample 2 · 个性化教育干预的匹配效应模拟

> **研究领域**：教育学 / 精准教育
> **语言**：中文

**研究假设（Phase 1 输出）**

> **因材施教的增益：通过机制性模拟量化教育干预的匹配效应**
>
> 本研究构建机制性模拟模型，量化"诊断-匹配"干预策略相对于"一刀切"通用干预的优越性。
> 模型中学生成就由知识与动机双重因素决定，并引入交互效应以使匹配优势自然涌现。
> 预期结果将清晰量化"匹配增益"，为精准教育范式提供理论依据。

📁 [`782496e4-6b3d-4934-a1e9-a4ef00b60b0a/`](./782496e4-6b3d-4934-a1e9-a4ef00b60b0a/)

---

### 📙 Sample 3 · 私募股权市场的先动者信息级联

> **研究领域**：金融学 / 行为经济学
> **语言**：English

**研究假设（Phase 1 输出）**

> *First-Mover Dynamics: Quantifying Informational Cascades and Network Leadership in Private Equity Investing*
>
> 本研究探究：在经济危机中，机构私募投资者的交易行为是否由理性信息级联（而非非理性羊群效应）所驱动。
> 通过对共同投资网络中交易序列的事件驱动时序分析，识别一致性"先动者"子群，
> 并验证其行为对同伴跟随概率的预测能力。研究成果为不透明市场的风险管理提供新框架。

📁 [`e6ee99f8-1e6c-47d6-ac64-c9d584efad23/`](./e6ee99f8-1e6c-47d6-ac64-c9d584efad23/)

---

## 📁 样本目录结构

每个样本目录均保留了该次研究运行的**完整原始产物**：
```
<task-id>/
├── idea/
│ ├── result.md # ✦ 最终假设报告（论文标题 + 摘要）
│ ├── plan/ # Planner 生成的任务分解计划
│ └── control/ # 各轮 Agent 执行记录
│
├── methods/
│ ├── result.md # ✦ 完整方法论文档（~500词）
│ ├── plan/
│ └── control/
│
└── experiment/
├── result.md # ✦ 完整实验结论报告（~2000词，学术风格）
├── plan/
└── control/ # 包含 AI 生成并执行的 Python 代码与输出
```

> **`result.md` 是每个阶段的最终交付物**，`plan/` 与 `control/` 保留了 AI 的完整思考与执行过程，供研究者审查。

---

## ℹ️ 关于 Eureka × AutoSeek

**Eureka × AutoSeek** 是一个双层自主科学研究平台：

| | AutoSeek 🔬 | Eureka 🌌 |
|---|---|---|
| **定位** | 单次研究任务执行引擎 | 长周期科学发现编排平台 |
| **范围** | 一个问题 → 一份结构化答案 | 一个目标 → 多轮循环 → 完整研究报告 |
| **状态管理** | 单次无状态运行 | 跨轮次持久化世界模型 |
| **当前状态** | ✅ 已上线 [go.eureka-ai.top](https://go.eureka-ai.top) | 🔧 积极开发中 |

---

<div align="center">

Built with [CrewAI](https://github.com/crewAIInc/crewAI) · FastAPI · Vue 3


</div>
