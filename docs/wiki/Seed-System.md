# 🌱 种子系统

种子（Bija，बीज）是Yogacara框架的核心概念，代表Agent经验的原子单位。

## 什么是种子？

在唯识学中，种子是潜伏在阿赖耶识中的潜在力量，能在条件成熟时产生现行（行为、认知）。Yogacara将这一概念数字化：

```python
from yogacara import Seed, SeedType

seed = Seed(
    content="用户喜欢简洁的回答",  # 种子内容
    seed_type=SeedType.PREFERENCE,  # 种子类型
    strength=0.8,                   # 种子强度 (0-1)
    source="interaction_001",       # 种子来源
    created_at=datetime.now()       # 创建时间
)
```

## 种子类型

Yogacara定义了多种种子类型：

| 类型 | 枚举值 | 描述 | 示例 |
|------|--------|------|------|
| 偏好 | `PREFERENCE` | 用户偏好模式 | "用户喜欢简洁的回复" |
| 行为 | `BEHAVIOR` | 行为模式 | "回答前先确认理解" |
| 知识 | `KNOWLEDGE` | 知识记忆 | "Python是一门编程语言" |
| 情感 | `EMOTION` | 情感倾向 | "用户对AI持开放态度" |
| 技能 | `SKILL` | 能力种子 | "擅长代码解释" |
| 价值 | `VALUE` | 价值判断 | "准确性比速度重要" |
| 兴趣 | `INTEREST` | 兴趣领域 | "对机器学习感兴趣" |

## 种子生命周期

```
┌─────────────────────────────────────────────────────┐
│                   种子生命周期                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│  ┌──────────┐                                       │
│  │ 1. 植入  │ ← 交互、学习、推理                    │
│  │  Plant   │                                       │
│  └────┬─────┘                                       │
│       │                                             │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ 2. 沉睡  │ ← 存储在阿赖耶识中                    │
│  │  Dormant │                                       │
│  └────┬─────┘                                       │
│       │                                             │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ 3. 激活  │ ← 条件满足时被触发                    │
│  │ Activate │                                       │
│  └────┬─────┘                                       │
│       │                                             │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ 4. 现行  │ → 影响当前行为                        │
│  │Manifest  │                                       │
│  └────┬─────┘                                       │
│       │                                             │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ 5. 强化  │ ← 正反馈增强强度                      │
│  │Strengthen│                                       │
│  └────┬─────┘                                       │
│       │                                             │
│       ▼                                             │
│  ┌──────────┐                                       │
│  │ 6. 衰变  │ ← 时间流逝或负反馈                    │
│  │  Decay   │                                       │
│  └──────────┘                                       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 种子操作

### 植入种子

```python
seed_system = SeedSystem()

# 基础植入
seed_system.plant_seed(
    content="用户是技术背景",
    seed_type=SeedType.KNOWLEDGE
)

# 带强度的植入
seed_system.plant_seed(
    content="用户偏好深度分析",
    seed_type=SeedType.PREFERENCE,
    strength=0.9,  # 高强度
    metadata={"source": "explicit_feedback"}
)
```

### 激活种子

```python
# 根据上下文激活相关种子
context = {
    "user_input": "帮我分析这个算法的复杂度",
    "domain": "technical",
    "depth": "detailed"
}

activated = seed_system.activate_seeds(context)

for seed in activated:
    print(f"激活: {seed.content} (强度: {seed.strength})")
```

### 强化种子

```python
# 正向反馈强化种子
seed_system.strengthen_seed(
    seed_id=seed.id,
    factor=1.2  # 强度提升20%
)
```

### 衰变种子

```python
# 时间衰变
seed_system.decay_seeds(decay_rate=0.95)
```

## 种子属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `id` | UUID | 唯一标识符 |
| `content` | str | 种子内容描述 |
| `seed_type` | SeedType | 种子类型 |
| `strength` | float | 强度 (0-1) |
| `source` | str | 来源标识 |
| `created_at` | datetime | 创建时间 |
| `last_activated` | datetime | 最后激活时间 |
| `activation_count` | int | 激活次数 |
| `metadata` | dict | 附加元数据 |

## 种子协同

多个种子可以协同作用，产生涌现效应：

```python
from yogacara import EmergenceEngine

emergence = EmergenceEngine(seed_system)

# 检测种子协同模式
patterns = emergence.detect_patterns()

# 生成涌现洞察
insights = emergence.generate_insights(context)
```

## 最佳实践

### 1. 合理设置强度
- 显式反馈：0.8-1.0
- 推理得出：0.5-0.7
- 默认假设：0.3-0.5

### 2. 及时强化/衰变
```python
# 每次交互后更新种子
if user_satisfied:
    seed_system.strengthen_seed(seed_id, 1.1)
else:
    seed_system.strengthen_seed(seed_id, 0.9)
```

### 3. 保持种子多样性
不同类型的种子保持平衡，避免单一类型主导。

### 4. 定期清理
```python
# 清理强度过低的种子
seed_system.prune_seeds(threshold=0.1)
```
