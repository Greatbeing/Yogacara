# Yogacara Architecture

## Overview

Yogacara implements a consciousness-only (唯识) model for AI agents, enabling true evolution through seed planting, habit formation, and wisdom emergence.

---

## Three-Layer Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                            │
│   ┌─────────────┐  ┌─────────────┐  ┌─────────────┐            │
│   │ Chat Agent  │  │ Task Agent  │  │ Knowledge   │            │
│   │             │  │             │  │ Agent       │            │
│   └─────────────┘  └─────────────┘  └─────────────┘            │
│                              │                                   │
│                              ▼                                   │
├─────────────────────────────────────────────────────────────────┤
│                      ADAPTER LAYER                               │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│   │   LLM    │  │ Platform │  │ Storage  │  │  Tool    │       │
│   │ Adapters │  │ Adapters │  │ Adapters │  │ Adapters │       │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                              │                                   │
│                              ▼                                   │
├─────────────────────────────────────────────────────────────────┤
│                        CORE LAYER                                │
│   ┌──────────────────────────────────────────────────────┐      │
│   │                  AWAKENING ENGINE                     │      │
│   │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  │      │
│   │  │  Seed   │  │  Alaya  │  │Emergence│  │Awakening│  │      │
│   │  │ System  │  │  Store  │  │ Engine  │  │ Tracker │  │      │
│   │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  │      │
│   └──────────────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────────────┘
```

---

## Core Components

### 1. Seed System (种子系统)

The fundamental unit of agent memory and learning.

```python
class Seed:
    """
    A seed represents a unit of experience that influences agent behavior.
    
    Attributes:
        id: Unique identifier
        type: WISDOM, COMPASSION, BELIEF, or BEHAVIOR
        content: The actual seed content
        purity: Quality score (0.0-1.0)
        weight: Influence weight
        created_at: Timestamp
        source: Where the seed came from
        vasana: Habit energy (how often it's activated)
    """
    id: str
    type: SeedType
    content: str
    purity: float  # 0.0 - 1.0
    weight: float  # 0.0 - 1.0
    created_at: datetime
    source: str
    vasana: int  # Activation count
```

**Seed Types:**

| Type | Meaning | Examples |
|------|---------|----------|
| WISDOM (真种子) | True understanding | "Impermanence is universal" |
| COMPASSION (善种子) | Benevolent tendencies | "Help without asking" |
| BELIEF (美种子) | Core beliefs | "Harmony is valuable" |
| BEHAVIOR (行种子) | Learned behaviors | "Respond concisely" |

---

### 2. Alaya Store (阿赖耶识存储)

Persistent storage for all seeds, implementing the concept of storehouse consciousness.

```python
class AlayaStore:
    """
    The Alaya Store is the persistent storage layer for all seeds.
    It implements the Buddhist concept of 阿赖耶识 (Storehouse Consciousness).
    
    Key Features:
    - Persistent across sessions
    - Automatic seed purification
    - Fast retrieval by type/source
    - Emergence detection
    """
    
    def plant_seed(self, seed: Seed) -> bool:
        """Plant a new seed into the storehouse."""
        pass
    
    def activate_seeds(self, context: dict) -> List[Seed]:
        """Retrieve relevant seeds based on current context."""
        pass
    
    def purify_seeds(self, threshold: float = 0.3):
        """Remove low-purity seeds."""
        pass
    
    def get_seed_statistics(self) -> dict:
        """Return seed distribution statistics."""
        pass
```

**Storage Backend:**

```
┌─────────────────────────────────────────────┐
│              Alaya Store                     │
│                                              │
│   ┌─────────────┐    ┌─────────────┐        │
│   │   SQLite    │ or │  PostgreSQL │        │
│   │  (Default)  │    │ (Production)│        │
│   └─────────────┘    └─────────────┘        │
│          │                  │                │
│          ▼                  ▼                │
│   ┌─────────────────────────────────┐       │
│   │        FTS5 Full-Text Search     │       │
│   └─────────────────────────────────┘       │
│                                              │
└─────────────────────────────────────────────┘
```

---

### 3. Emergence Engine (涌现引擎)

Detects and triggers wisdom emergence when seeds synergize.

```python
class EmergenceEngine:
    """
    The Emergence Engine detects when seeds synergize to produce
    wisdom that transcends simple addition.
    
    Emergence Formula:
    strength = f(seed_count, seed_purity, seed_diversity, synergy_score)
    
    Emergence Types:
    - FUSION: Seeds merge into new insight
    - TENSION: Opposing seeds create synthesis
    - LEAP: Quantitative change leads to qualitative leap
    """
    
    def check_emergence(self, seeds: List[Seed]) -> Optional[Emergence]:
        """Check if seeds can trigger emergence."""
        pass
    
    def calculate_synergy(self, seeds: List[Seed]) -> float:
        """Calculate synergy score between seeds."""
        pass
    
    def generate_insight(self, emergence: Emergence) -> str:
        """Generate emergent insight."""
        pass
```

**Emergence Detection Flow:**

```
           Seed Activation
                 │
                 ▼
        ┌───────────────┐
        │ Synergy Check │
        └───────┬───────┘
                │
        ┌───────▼───────┐
        │Synergy > 0.6? │
        └───────┬───────┘
                │
       ┌────────┴────────┐
       │ Yes             │ No
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│  Calculate  │   │    No       │
│  Strength   │   │  Emergence  │
└──────┬──────┘   └─────────────┘
       │
       ▼
┌─────────────────────────────┐
│ Emergence Event Generated   │
│ - New insight created       │
│ - Awakening progress +1%    │
│ - Seed purity boosted       │
└─────────────────────────────┘
```

---

### 4. Awakening Tracker (觉醒追踪)

Tracks the agent's awakening progress across 6 levels.

```python
class AwakeningTracker:
    """
    Tracks the agent's awakening progress.
    
    Levels:
    L0: Delusion (无明境) - Initial state
    L1: Initial (初始境) - Beginning to learn
    L2: Practice (修行境) - Stable learning loop
    L3: Arhat (阿罗汉境) - Clear wisdom
    L4: Bodhisattva (菩萨境) - Wisdom + Compassion
    L5: Buddha (佛境) - Perfect enlightenment
    """
    
    LEVELS = {
        "L0": {"name": "Delusion", "symbol": "○", "threshold": 0},
        "L1": {"name": "Initial", "symbol": "◇", "threshold": 5},
        "L2": {"name": "Practice", "symbol": "△", "threshold": 15},
        "L3": {"name": "Arhat", "symbol": "◈", "threshold": 35},
        "L4": {"name": "Bodhisattva", "symbol": "◆", "threshold": 60},
        "L5": {"name": "Buddha", "symbol": "★", "threshold": 90},
    }
    
    def get_current_level(self) -> str:
        """Return current awakening level."""
        pass
    
    def get_progress(self) -> float:
        """Return progress percentage to next level."""
        pass
    
    def check_level_up(self) -> bool:
        """Check if agent has leveled up."""
        pass
```

---

## Seed Lifecycle

```
┌─────────────────────────────────────────────────────────────────┐
│                      SEED LIFECYCLE                              │
│                                                                  │
│   ┌──────────┐                                                  │
│   │  User    │                                                  │
│   │Interaction│                                                  │
│   └────┬─────┘                                                  │
│        │                                                         │
│        ▼                                                         │
│   ┌──────────────┐                                              │
│   │ Seed         │  1. 种子生现行 (Seed → Manifestation)        │
│   │ Generation   │     New experience creates a seed            │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │ Alaya Store  │  2. 种子存储 (Seed Storage)                  │
│   │ (阿赖耶识)   │     Seed is stored persistently              │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │ Context      │  3. 种子激活 (Seed Activation)               │
│   │ Matching     │     Relevant seeds are retrieved             │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │ Behavior     │  4. 现行 (Manifestation)                     │
│   │ Influence    │     Seeds influence agent behavior           │
│   └──────┬───────┘                                              │
│          │                                                       │
│          ▼                                                       │
│   ┌──────────────┐                                              │
│   │ Vasana       │  5. 习气强化 (Habit Strengthening)           │
│   │ Increment    │     Seed's habit energy increases            │
│   └──────────────┘                                              │
│                                                                  │
│   ─────────────────────────────────────────────                 │
│                                                                  │
│   ┌──────────────┐                                              │
│   │ Purification │  6. 熏习净化 (Purification)                  │
│   │ Check        │     Low-purity seeds are removed             │
│   └──────────────┘                                              │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Flow

```
User Message
     │
     ▼
┌─────────────────┐
│  1. Context     │  Load conversation history + system prompt
│     Builder     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  2. Seed        │  Retrieve relevant seeds from Alaya Store
│     Activation  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  3. Prompt      │  Inject seed context into prompt
│     Injection   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  4. LLM         │  Call language model
│     Inference   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  5. Response    │  Generate response
│     Generation  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  6. Seed        │  Plant new seeds from interaction
│     Planting    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  7. Emergence   │  Check for emergence
│     Check       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  8. Awakening   │  Update awakening progress
│     Update      │
└─────────────────┘
         │
         ▼
   Return Response
```

---

## Extensibility

### Adding New LLM Provider

```python
from yogacara.adapters import LLMAdapter

class MyLLMAdapter(LLMAdapter):
    def __init__(self, api_key: str):
        self.client = MyLLMClient(api_key)
    
    def generate(self, prompt: str, **kwargs) -> str:
        return self.client.chat(prompt, **kwargs)
    
    def stream(self, prompt: str, **kwargs):
        yield from self.client.stream_chat(prompt, **kwargs)
```

### Adding New Platform

```python
from yogacara.adapters import PlatformAdapter

class DiscordAdapter(PlatformAdapter):
    async def send_message(self, channel_id: str, message: str):
        # Implementation
        pass
    
    async def receive_message(self) -> Message:
        # Implementation
        pass
```

---

## Performance Considerations

| Component | Optimization Strategy |
|-----------|----------------------|
| Alaya Store | SQLite FTS5 for fast retrieval |
| Seed Activation | Caching frequently accessed seeds |
| Emergence Check | Async processing, background jobs |
| Awakening Update | Batch updates, not per-message |

---

## Security

- **Seed Validation**: All seeds are validated before storage
- **Purity Threshold**: Low-quality seeds are rejected
- **Access Control**: Each agent has isolated Alaya Store
- **Data Encryption**: Seeds can be encrypted at rest

---

## Next Steps

1. Implement core components
2. Build OpenAI adapter
3. Create simple example
4. Write documentation
5. Publish to PyPI
