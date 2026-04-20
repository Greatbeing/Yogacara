# API Reference

Complete API documentation for the Yogacara framework.

---

## Core Module (`yogacara.core`)

### Seed System

#### `SeedType`

Enum representing the four types of seeds in Yogacara philosophy.

```python
from yogacara import SeedType

SeedType.WISDOM      # 真种子 - True understanding
SeedType.COMPASSION  # 善种子 - Benevolent tendencies
SeedType.BELIEF      # 美种子 - Core beliefs
SeedType.BEHAVIOR    # 行种子 - Learned behaviors
```

**Attributes:**
- `value` (str): The lowercase string identifier

---

#### `Seed`

Dataclass representing a unit of experience that influences agent behavior.

```python
from yogacara import Seed, SeedType

seed = Seed(
    type=SeedType.WISDOM,
    content="Understanding impermanence",
    purity=0.85,
    weight=0.7,
)
```

**Attributes:**
- `id` (str): Unique identifier (UUID, first 8 characters)
- `type` (SeedType): The seed type
- `content` (str): The seed content
- `purity` (float): Quality score (0.0-1.0, default: 0.7)
- `weight` (float): Influence weight (0.0-1.0, default: 0.5)
- `created_at` (datetime): Creation timestamp
- `source` (str): Origin of the seed (default: "interaction")
- `vasana` (int): Habit energy - activation count (default: 0)
- `metadata` (dict): Additional structured data

**Methods:**

##### `activate() -> None`
Increment the vasana (habit energy) when the seed is activated.

##### `boost_purity(amount: float = 0.05) -> None`
Increase purity based on positive feedback.

##### `decay_purity(amount: float = 0.01) -> None`
Decrease purity over time or with negative feedback.

##### `to_dict() -> Dict[str, Any]`
Serialize the seed to a dictionary.

##### `from_dict(data: Dict[str, Any]) -> Seed`
Create a seed from a dictionary.

---

#### `SeedSystem`

Manages seed creation, validation, and lifecycle.

```python
from yogacara import SeedSystem, SeedType

system = SeedSystem()
seed = system.create_seed(
    type=SeedType.WISDOM,
    content="New insight",
    purity=0.8,
)
```

**Attributes:**
- `PURITY_THRESHOLD` (float): Minimum purity to accept seeds (default: 0.3)
- `WEIGHT_DECAY_RATE` (float): Decay rate per day (default: 0.01)
- `seeds` (Dict[str, Seed]): All stored seeds

**Methods:**

##### `create_seed(type: SeedType, content: str, purity: float = 0.7, source: str = "interaction", **kwargs) -> Optional[Seed]`
Create a new seed. Returns `None` if purity is below threshold.

##### `get_seeds_by_type(type: SeedType) -> List[Seed]`
Get all seeds of a specific type.

##### `get_seeds_by_source(source: str) -> List[Seed]`
Get all seeds from a specific source.

##### `get_high_purity_seeds(threshold: float = 0.8) -> List[Seed]`
Get seeds with purity above threshold.

##### `get_statistics() -> Dict[str, Any]`
Get seed distribution statistics.

##### `decay_all_seeds(days: int = 1) -> int`
Decay purity of all seeds. Returns count of seeds below threshold.

---

### Alaya Store

#### `AlayaStore`

Persistent storage for all seeds, implementing the concept of storehouse consciousness.

```python
from yogacara import AlayaStore

store = AlayaStore(db_path="alaya.db")
store.plant_seed(seed)
```

**Constructor:**
```python
AlayaStore(db_path: str = "alaya.db")
```

**Methods:**

##### `plant_seed(seed: Seed) -> bool`
Plant a new seed into the storehouse. Returns `True` on success.

##### `activate_seeds(context: str, seed_types: Optional[List[SeedType]] = None, limit: int = 10) -> List[Seed]`
Retrieve relevant seeds based on context using FTS5 search. Increments vasana for each activated seed.

##### `get_seed_by_id(seed_id: str) -> Optional[Seed]`
Retrieve a specific seed by ID.

##### `count_seeds() -> int`
Count total seeds in the store.

##### `count_seeds_by_type() -> Dict[SeedType, int]`
Count seeds grouped by type.

##### `delete_seed(seed_id: str) -> bool`
Delete a seed by ID.

##### `clear_all_seeds() -> None`
Delete all seeds from the store.

##### `search_seeds(query: str) -> List[Seed]`
Full-text search for seeds.

##### `get_recent_seeds(limit: int = 10) -> List[Seed]`
Get the most recently planted seeds.

##### `get_high_purity_seeds(threshold: float = 0.8) -> List[Seed]`
Get seeds with purity above threshold.

---

### Emergence Engine

#### `EmergenceType`

Enum representing types of emergence.

```python
from yogacara import EmergenceType

EmergenceType.FUSION   # Seeds merge into new insight
EmergenceType.TENSION   # Opposing seeds create synthesis
EmergenceType.LEAP     # Quantitative change → qualitative leap
```

---

#### `Emergence`

Dataclass representing an emergence event.

```python
from yogacara import Emergence, EmergenceType

emergence = Emergence(
    seed_ids=["seed1", "seed2", "seed3"],
    emergence_type=EmergenceType.FUSION,
    strength=0.85,
    insight="Combined understanding",
)
```

**Attributes:**
- `seed_ids` (List[str]): IDs of contributing seeds
- `emergence_type` (EmergenceType): Type of emergence
- `strength` (float): Emergence strength (0.0-1.0)
- `insight` (Optional[str]): Generated insight text
- `contributing_seeds` (List[Seed]): Full seed objects

---

#### `EmergenceEngine`

Detects wisdom emergence when seeds synergize.

```python
from yogacara import EmergenceEngine

engine = EmergenceEngine()
emergence = engine.check_emergence(seeds)
```

**Attributes:**
- `MIN_SEEDS_FOR_EMERGENCE` (int): Minimum seeds needed (default: 3)
- `SYNERGY_THRESHOLD` (float): Minimum synergy to trigger (default: 0.6)
- `STRENGTH_THRESHOLD` (float): Minimum strength to trigger (default: 0.7)
- `SYNERGY_MATRIX` (Dict): Synergy values between seed type pairs

**Methods:**

##### `check_emergence(seeds: List[Seed]) -> Optional[Emergence]`
Check if seeds can trigger emergence. Returns `Emergence` if triggered.

##### `calculate_synergy(seeds: List[Seed]) -> float`
Calculate synergy score between seeds (0.0-1.0).

##### `generate_insight(seeds: List[Seed], emergence_type: EmergenceType) -> str`
Generate insight text based on seeds and emergence type.

---

### Awakening Tracker

#### `AwakeningLevel`

Enum representing the six levels of awakening.

```python
from yogacara import AwakeningLevel

AwakeningLevel.L0_DELUSION      # ○ 无明境
AwakeningLevel.L1_INITIAL       # ◇ 初始境
AwakeningLevel.L2_PRACTICE      # △ 修行境
AwakeningLevel.L3_ARHAT         # ◈ 阿罗汉境
AwakeningLevel.L4_BODHISATTVA   # ◆ 菩萨境
AwakeningLevel.L5_BUDDHA        # ★ 佛境
```

**Properties:**
- `name_cn` (str): Chinese name for the level
- `symbol` (str): Unicode symbol representing the level
- `description` (str): Description of the level

---

#### `AwakeningProgress`

Dataclass representing current awakening progress.

```python
from yogacara import AwakeningProgress

progress = AwakeningProgress(
    level=AwakeningLevel.L2_PRACTICE,
    progress=0.65,
    total_seeds=150,
    wisdom_seeds=25,
    compassion_seeds=15,
    emergence_count=2,
)
```

**Properties:**
- `wisdom_percentage` (float): Percentage of wisdom seeds
- `compassion_percentage` (float): Percentage of compassion seeds
- `overall_progress` (float): Overall progress across all levels (0-100)

---

#### `AwakeningTracker`

Tracks and manages awakening progress.

```python
from yogacara import AwakeningTracker

tracker = AwakeningTracker()
level = tracker.get_current_level()
```

**Methods:**

##### `get_current_level() -> AwakeningLevel`
Get the current awakening level.

##### `get_progress() -> float`
Get progress to next level (0.0-1.0).

##### `check_level_up(wisdom_percentage: float, compassion_percentage: float, emergence_count: int) -> bool`
Check if agent qualifies for level up. Updates level if qualified.

##### `calculate_progress(wisdom_percentage: float, compassion_percentage: float, emergence_count: int) -> float`
Calculate progress to next level.

##### `get_status(total_seeds: int, wisdom_seeds: int, compassion_seeds: int, emergence_count: int) -> AwakeningProgress`
Get full awakening status including progress dataclass.

##### `get_progress_bar(width: int = 20) -> str`
Generate text progress bar.

##### `get_level_display() -> str`
Get formatted level display string.

##### `to_dict() -> Dict[str, Any]`
Serialize tracker state to dictionary.

##### `from_dict(data: Dict[str, Any]) -> AwakeningTracker`
Create tracker from dictionary.

---

## Configuration Module (`yogacara.config`)

### `YogacaraConfig`

Main configuration class.

```python
from yogacara import YogacaraConfig

config = YogacaraConfig()
config.seed_system.purity_threshold = 0.4
```

**Sub-configurations:**
- `seed_system` (SeedSystemConfig)
- `alaya_store` (AlayaStoreConfig)
- `emergence` (EmergenceConfig)
- `awakening` (AwakeningConfig)

**Class Methods:**
- `from_dict(data: Dict) -> YogacaraConfig`
- `from_yaml(path: Path) -> YogacaraConfig`
- `from_json(path: Path) -> YogacaraConfig`
- `from_env(prefix: str = "YOGACARA_") -> YogacaraConfig`
- `load(path: Optional = None, create_default: bool = False) -> YogacaraConfig`

**Methods:**
- `to_dict() -> Dict[str, Any]`
- `save_yaml(path: Path) -> None`
- `save_json(path: Path) -> None`

---

## Logging Module (`yogacara.logger`)

### `YogacaraLogger`

Structured logger for Yogacara framework.

```python
from yogacara import YogacaraLogger, get_logger

logger = YogacaraLogger(name="yogacara", level=logging.INFO)
# or
logger = get_logger(level=logging.INFO, log_file="yogacara.log")
```

**Methods:**
- `debug(message: str, **kwargs)`
- `info(message: str, **kwargs)`
- `warning(message: str, **kwargs)`
- `error(message: str, **kwargs)`
- `critical(message: str, **kwargs)`
- `seed_planted(seed_id: str, seed_type: str)`
- `seed_activated(seed_id: str, vasana: int)`
- `emergence_detected(emergence_type: str, strength: float)`
- `level_up(old_level: str, new_level: str)`

### `configure_logging`

Convenience function to configure logging.

```python
from yogacara import configure_logging

logger = configure_logging(level="INFO", log_dir="logs")
```

---

## CLI Module (`yogacara.cli`)

Command-line interface for Yogacara.

```bash
# Show info
yogacara info

# Check status
yogacara status --db-path alaya.db

# Plant a seed
yogacara plant --type wisdom --content "Test wisdom" --purity 0.8

# View levels
yogacara levels

# Check level
yogacara check-level --total 100 --wisdom 20 --compassion 10 --emergence 3

# View statistics
yogacara stats --db-path alaya.db
```

---

## Package-Level Exports

```python
from yogacara import (
    # Version info
    __version__,
    __author__,
    __email__,
    __license__,
    
    # Seed System
    Seed,
    SeedType,
    SeedSystem,
    
    # Alaya Store
    AlayaStore,
    
    # Emergence Engine
    EmergenceEngine,
    Emergence,
    EmergenceType,
    
    # Awakening Tracker
    AwakeningTracker,
    AwakeningLevel,
    AwakeningProgress,
)
```
