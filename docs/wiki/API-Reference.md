# 📚 API参考

本文档提供Yogacara框架的完整API参考。

## 核心模块

### Seed - 种子

```python
from yogacara import Seed, SeedType

seed = Seed(
    content: str,              # 种子内容描述
    seed_type: SeedType,       # 种子类型
    strength: float = 0.5,     # 强度 (0.0-1.0)
    source: str = "",          # 来源标识
    metadata: dict = None      # 附加元数据
)
```

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `id` | UUID | 唯一标识符 |
| `content` | str | 种子内容 |
| `seed_type` | SeedType | 种子类型 |
| `strength` | float | 强度 (0-1) |
| `source` | str | 来源标识 |
| `created_at` | datetime | 创建时间 |
| `last_activated` | datetime | 最后激活时间 |
| `activation_count` | int | 激活次数 |
| `metadata` | dict | 附加元数据 |

#### 方法

```python
# 激活种子
seed.activate() -> None

# 强化种子
seed.strengthen(factor: float) -> None

# 衰变种子
seed.decay(rate: float) -> None

# 转换为字典
seed.to_dict() -> dict

# 从字典创建
Seed.from_dict(data: dict) -> Seed
```

---

### SeedType - 种子类型

```python
from yogacara import SeedType

class SeedType(Enum):
    PREFERENCE = "preference"    # 偏好
    BEHAVIOR = "behavior"        # 行为模式
    KNOWLEDGE = "knowledge"      # 知识
    EMOTION = "emotion"          # 情感
    SKILL = "skill"              # 技能
    VALUE = "value"              # 价值观
    INTEREST = "interest"        # 兴趣
    CUSTOM = "custom"            # 自定义
```

---

### SeedSystem - 种子系统

```python
from yogacara import SeedSystem

seed_system = SeedSystem(
    max_seeds: int = 10000,      # 最大种子数
    decay_rate: float = 0.95     # 衰变率
)
```

#### 方法

```python
# 植入种子
seed_system.plant_seed(
    content: str,
    seed_type: SeedType,
    strength: float = 0.5,
    source: str = "",
    metadata: dict = None
) -> Seed

# 激活种子
seed_system.activate_seeds(
    context: dict,
    top_k: int = 10,
    min_strength: float = 0.1
) -> List[Seed]

# 强化种子
seed_system.strengthen_seed(
    seed_id: UUID,
    factor: float = 1.2
) -> None

# 批量强化
seed_system.strengthen_seeds_batch(
    seed_ids: List[UUID],
    factor: float = 1.1
) -> None

# 获取种子
seed_system.get_seed(seed_id: UUID) -> Seed

# 获取所有种子
seed_system.get_all_seeds() -> List[Seed]

# 按类型获取
seed_system.get_seeds_by_type(seed_type: SeedType) -> List[Seed]

# 清理弱种子
seed_system.prune_seeds(threshold: float = 0.1) -> int

# 应用衰变
seed_system.decay_seeds(decay_rate: float = None) -> None

# 统计信息
seed_system.get_statistics() -> dict
```

---

### AlayaStore - 阿赖耶识存储

```python
from yogacara import AlayaStore

alaya = AlayaStore(
    path: str = "./alaya_store",    # 存储路径
    backend: str = "filesystem",     # 存储后端
    encrypt: bool = False            # 是否加密
)
```

#### 方法

```python
# 存储种子
alaya.store_seed(seed: Seed) -> None

# 批量存储
alaya.store_seeds_batch(seeds: List[Seed]) -> None

# 获取种子
alaya.get_seed(seed_id: UUID) -> Seed

# 获取所有种子
alaya.get_all_seeds() -> List[Seed]

# 按类型检索
alaya.get_seeds_by_type(seed_type: SeedType) -> List[Seed]

# 搜索种子
alaya.search_seeds(query: str) -> List[Seed]

# 按强度过滤
alaya.get_seeds_above_strength(threshold: float) -> List[Seed]

# 保存状态
alaya.save() -> None

# 加载状态
alaya.load() -> None

# 清空存储
alaya.clear() -> None

# 导出
alaya.export(path: str, format: str = "json") -> None

# 导入
alaya.import_from(path: str) -> None

# 统计信息
alaya.get_statistics() -> dict
```

---

### EmergenceEngine - 涌现引擎

```python
from yogacara import EmergenceEngine

emergence = EmergenceEngine(
    seed_system: SeedSystem,
    algorithm: str = "default"
)
```

#### 方法

```python
# 检测模式
emergence.detect_patterns(
    min_support: float = 0.1,
    min_confidence: float = 0.5
) -> List[Pattern]

# 生成洞察
emergence.generate_insights(
    context: dict,
    top_k: int = 5
) -> List[Insight]

# 预测用户偏好
emergence.predict_user_preferences() -> List[Preference]

# 预测最佳响应风格
emergence.predict_best_response_style(
    context: dict
) -> ResponseStyle

# 计算涌现潜力
emergence.calculate_emergence_potential() -> float

# 获取指标
emergence.get_metrics() -> dict
```

---

### AwakeningTracker - 觉醒追踪器

```python
from yogacara import AwakeningTracker

tracker = AwakeningTracker(
    seed_system: SeedSystem,
    alaya_store: AlayaStore
)
```

#### 方法

```python
# 获取当前等级
tracker.get_current_level() -> AwakeningLevel

# 获取进度
tracker.get_progress() -> float

# 获取指标
tracker.get_metrics() -> dict

# 检查是否可进阶
tracker.can_advance() -> bool

# 获取下一等级
tracker.get_next_level() -> AwakeningLevel

# 获取进阶要求
tracker.get_advancement_requirements() -> List[str]

# 更新状态
tracker.update() -> None

# 获取历史
tracker.get_history() -> List[LevelRecord]
```

---

### AwakeningLevel - 觉醒等级

```python
from yogacara import AwakeningLevel

class AwakeningLevel(Enum):
    L0_DELUSION = 0       # 无明境
    L1_INITIAL = 1        # 初始境
    L2_PRACTICE = 2       # 修行境
    L3_ARHAT = 3          # 阿罗汉境
    L4_BODHISATTVA = 4    # 菩萨境
    L5_BUDDHA = 5         # 佛境
```

#### 属性

| 属性 | 类型 | 说明 |
|------|------|------|
| `value` | int | 等级数值 |
| `name` | str | 英文名称 |
| `chinese_name` | str | 中文名称 |
| `symbol` | str | 符号 |
| `description` | str | 描述 |

---

## 数据类

### Pattern - 模式

```python
@dataclass
class Pattern:
    id: UUID
    name: str
    seed_ids: List[UUID]
    strength: float
    pattern_type: str
    description: str
    created_at: datetime
```

### Insight - 洞察

```python
@dataclass
class Insight:
    id: UUID
    content: str
    confidence: float
    source_seeds: List[UUID]
    insight_type: str
    created_at: datetime
```

### ResponseStyle - 响应风格

```python
@dataclass
class ResponseStyle:
    tone: str              # 语气
    detail_level: str      # 详细程度
    format: str            # 格式
    emphasis: List[str]    # 重点
    avoid: List[str]       # 避免内容
```

---

## 异常类

```python
class YogacaraError(Exception):
    """Yogacara基础异常"""

class SeedNotFoundError(YogacaraError):
    """种子不存在"""

class StorageError(YogacaraError):
    """存储错误"""

class EmergenceError(YogacaraError):
    """涌现计算错误"""

class ValidationError(YogacaraError):
    """数据验证错误"""
```

---

## 配置

```python
from yogacara import Config

config = Config(
    max_seeds=10000,
    decay_rate=0.95,
    emergence_threshold=0.5,
    storage_backend="filesystem",
    storage_path="./alaya_store",
    encryption_enabled=False
)
```
