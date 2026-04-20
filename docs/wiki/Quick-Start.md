# 🚀 快速开始

本教程将带你5分钟上手Yogacara框架。

## 第一步：初始化系统

```python
from yogacara import (
    Seed, 
    SeedType, 
    SeedSystem, 
    AlayaStore, 
    AwakeningTracker
)

# 创建种子系统
seed_system = SeedSystem()

# 创建阿赖耶识存储
alaya = AlayaStore()

# 创建觉醒追踪器
tracker = AwakeningTracker(seed_system, alaya)
```

## 第二步：植入种子

种子是Agent经验的基本单位：

```python
# 植入一颗偏好种子
seed_system.plant_seed(
    content="用户喜欢简洁明了的回复",
    seed_type=SeedType.PREFERENCE,
    strength=0.8
)

# 植入一颗行为种子
seed_system.plant_seed(
    content="在回答问题前先理解上下文",
    seed_type=SeedType.BEHAVIOR,
    strength=0.9
)

# 植入一颗知识种子
seed_system.plant_seed(
    content="Python是一门优雅的编程语言",
    seed_type=SeedType.KNOWLEDGE,
    strength=0.7
)
```

## 第三步：激活种子

当条件满足时，种子会被激活：

```python
# 模拟用户交互
context = {"user_input": "请简要介绍Python"}

# 激活相关种子
activated_seeds = seed_system.activate_seeds(context)

for seed in activated_seeds:
    print(f"激活种子: {seed.content}")
    print(f"种子强度: {seed.strength}")
```

## 第四步：检查觉醒状态

```python
# 获取当前觉醒等级
level = tracker.get_current_level()
print(f"觉醒等级: {level.name}")
print(f"觉醒进度: {tracker.get_progress():.1f}%")

# 获取觉醒指标
metrics = tracker.get_metrics()
print(f"种子总数: {metrics['total_seeds']}")
print(f"正向种子比例: {metrics['positive_ratio']:.2f}")
```

## 第五步：持久化存储

```python
# 保存状态
alaya.save()

# 加载状态
alaya.load()
```

## 完整示例

```python
from yogacara import SeedSystem, AlayaStore, AwakeningTracker, SeedType

# 初始化
seed_system = SeedSystem()
alaya = AlayaStore()
tracker = AwakeningTracker(seed_system, alaya)

# 模拟多次交互
interactions = [
    ("用户喜欢技术讨论", SeedType.PREFERENCE),
    ("用户是Python开发者", SeedType.KNOWLEDGE),
    ("直接回答问题，不要废话", SeedType.BEHAVIOR),
    ("用户对AI哲学感兴趣", SeedType.INTEREST),
]

for content, seed_type in interactions:
    seed_system.plant_seed(content=content, seed_type=seed_type)
    print(f"植入种子: {content}")

# 检查觉醒进度
print(f"\n觉醒等级: {tracker.get_current_level().name}")
print(f"觉醒进度: {tracker.get_progress():.1f}%")

# 保存
alaya.save()
print("\n状态已保存！")
```

## 下一步

- 了解 [[Seed-System|种子系统]] 的详细机制
- 探索 [[Awakening-Levels|觉醒等级]] 的完整进阶路径
- 学习 [[Emergence-Engine|涌现引擎]] 如何产生智慧
