# 经验库 (EXPERIENCE_LIBRARY)

**最后更新：** 2026-02-08

---

## 🎯 核心经验

### 1. 记忆框架设计

| 字段 | 内容 |
|------|------|
| **ID** | memory_framework_design |
| **模式** | 搭建 AI 记忆系统 |
| **经验** | 基于论文(Training-Free GRPO)的经验库思路，区分记录和提炼，采用动态更新策略 |
| **验证次数** | 1 |
| **成功率** | 100% |
| **状态** | pending |
| **置信度** | medium |
| **来源** | 与用户协作创建 |

### 2. 论文分析策略

| 字段 | 内容 |
|------|------|
| **ID** | paper_analysis_approach |
| **模式** | 解读学术论文 |
| **经验** | 结构化解读：核心问题→创新点→方法原理→实验结果→应用启发 |
| **验证次数** | 1 |
| **成功率** | 100% |
| **状态** | pending |
| **置信度** | medium |
| **来源** | Training-Free GRPO 论文解读 |

### 3. 技能安装流程

| 字段 | 内容 |
|------|------|
| **ID** | skill_installation |
| **模式** | 安装 OpenClaw skills |
| **经验** | 1. 使用 clawhub CLI 搜索 2. 安装到 workspace/skills 3. 通过 openclaw skills list 验证 |
| **验证次数** | 1 |
| **成功率** | 100% |
| **状态** | verified |
| **置信度** | high |
| **来源** | notebooklm-skill, planning-with-files 安装 |

---

## 🔧 工具使用经验

### NotebookLM Skill
- **状态**: ready
- **用途**: 查询 Google NotebookLM 笔记本
- **最佳实践**: 直接提问，获取引用来源的回答
- **限制**: 需要用户有 NotebookLM 账户和笔记本

### Planning-with-files Skill
- **状态**: installed
- **用途**: 复杂任务的规划和进度追踪
- **最佳实践**: 用于 >5 步的项目
- **创建文件**: task_plan.md, findings.md, progress.md

---

### 5. 标题模式策略（来自 viral-memory）

| 字段 | 内容 |
|------|------|
| **ID** | viral_memory_title_pattern |
| **模式** | 内容创作/标题优化 |
| **经验** | 1. "结果先给 + 风格锚点"提高点击率 2. 公式：Making [X] & [Y] [Z] | Ghibli-Style ASMR 3. 建立承诺→满足的闭环 |
| **验证次数** | 待迁移 |
| **成功率** | 待验证 |
| **状态** | untested |
| **置信度** | medium |
| **来源** | viral-memory TP-0001 |

### 6. 记忆系统编号规则（来自 viral-memory）

| 字段 | 内容 |
|------|------|
| **ID** | viral_memory_naming |
| **模式** | 记忆条目管理 |
| **经验** | 1. 编号稳定：TP/E/F/P-0001… 2. 版本用 v01/v02 3. 时间戳 created_at/updated_at 4. 展示名独立于文件名 |
| **验证次数** | 长期验证 |
| **成功率** | N/A（系统规则） |
| **状态** | verified |
| **置信度** | high |
| **来源** | viral-memory 规则库 |

---

## 📈 验证状态统计

| 状态 | 数量 |
|------|------|
| untested | 1 |
| pending | 3 |
| verified | 2 |
| deprecated | 0 |

---

## 🔄 更新日志

### 2026-02-08
- ✅ 初始化经验库
- ✅ 添加 3 个核心经验
- ✅ 记录工具使用经验
- ✅ 演示：添加"记忆优化策略"经验
- ✅ 整合 viral-memory，提炼 2 个新经验

---

*此文件由记忆系统自动维护*
