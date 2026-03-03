# 长期记忆数据库架构

## 🗃️ 数据库结构

### 1. 核心记忆表
```
memory_core/
├── conversations/      # 对话记录
├── decisions/         # 重要决策
├── preferences/       # 用户偏好
├── projects/          # 项目记录
├── skills/            # 技能使用记录
└── system/            # 系统配置
```

### 2. 分类系统
**按类型分类**：
- `conversation`: 对话交流
- `decision`: 重要决定
- `preference`: 用户偏好
- `project`: 项目进展
- `skill`: 技能使用
- `system`: 系统配置

**按重要性分级**：
- `critical`: 关键记忆（永久保存）
- `important`: 重要记忆（长期保存）
- `normal`: 普通记忆（定期归档）
- `temporary`: 临时记忆（短期保存）

### 3. 索引系统
**时间索引**：
- 按年/月/日组织
- 支持时间范围查询

**主题索引**：
- 关键词标签系统
- 语义关联网络

**关系索引**：
- 记忆之间的关联关系
- 因果链和依赖关系

## 🔄 数据流程

### 输入处理
```
原始记忆 → 分类 → 重要性评估 → 结构化存储 → 索引建立
```

### 检索流程
```
查询 → 语义匹配 → 索引查找 → 关联扩展 → 结果排序 → 返回
```

### 维护流程
```
定期整理 → 重要性重评估 → 归档过期记忆 → 优化索引
```

## 💾 存储格式

### 1. 对话记录格式
```yaml
id: conv_20260211_0450
timestamp: 2026-02-11T04:50:00PST
type: conversation
importance: important
participants: ["用户", "小玉"]
channel: whatsapp
content: "OK继续初始化"
tags: ["初始化", "确认", "贾维斯模式"]
related: ["init_20260211_0447"]
```

### 2. 决策记录格式
```yaml
id: decision_20260211_0450
timestamp: 2026-02-11T04:50:00PST
type: decision
importance: critical
title: "技能安装安全检查策略"
description: "用户要求安装技能时必须进行安全检查"
decision: "建立安全检查流程"
reason: "确保系统安全，防止恶意技能"
impact: "高 - 影响所有技能安装操作"
tags: ["安全", "技能", "策略"]
```

### 3. 用户偏好格式
```yaml
id: pref_20260211_0447
timestamp: 2026-02-11T04:47:00PST
type: preference
importance: important
category: "communication"
key: "response_style"
value: "简洁专业"
source: "贾维斯模式初始化指令"
confidence: 0.9
tags: ["沟通风格", "贾维斯模式"]
```

## 🛡️ 记忆保护机制

### 1. 防删除保护
- 关键记忆标记为只读
- 删除操作需要双重确认
- 自动备份被删除的记忆

### 2. 完整性检查
- 定期校验记忆完整性
- 自动修复损坏的记忆
- 备份恢复机制

### 3. 访问控制
- 分级访问权限
- 操作日志记录
- 异常访问报警

## 📊 统计指标

### 记忆总量统计
- 总记忆数量
- 按类型分布
- 按重要性分布
- 增长趋势

### 使用频率统计
- 高频访问记忆
- 关联关系强度
- 检索成功率
- 响应时间

### 质量评估
- 记忆完整性评分
- 关联网络密度
- 检索准确率
- 用户满意度

## 🔧 维护工具

### 1. 记忆整理脚本
```bash
# 整理过期记忆
./scripts/memory_cleanup.sh

# 重建索引
./scripts/rebuild_index.sh

# 完整性检查
./scripts/integrity_check.sh
```

### 2. 备份恢复工具
```bash
# 完整备份
./scripts/backup_full.sh

# 增量备份
./scripts/backup_incremental.sh

# 恢复记忆
./scripts/restore_memory.sh
```

### 3. 分析报告工具
```bash
# 生成统计报告
./scripts/generate_report.sh

# 分析使用模式
./scripts/analyze_patterns.sh

# 优化建议
./scripts/optimization_suggestions.sh
```

---

**架构版本**: 1.0
**创建时间**: 2026-02-11 04:50 PST
**最后更新**: 2026-02-11 04:50 PST