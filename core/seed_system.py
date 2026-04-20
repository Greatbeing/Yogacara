"""
Seed System - 种子系统

Implements the core concept of "seeds" (种子) from Yogacara Buddhism.
Seeds are units of experience that influence agent behavior.
"""

from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any
import uuid
import json


class SeedType(Enum):
    """Types of seeds based on Yogacara philosophy"""
    WISDOM = "wisdom"       # 真种子 - True understanding
    COMPASSION = "compassion"  # 善种子 - Benevolent tendencies  
    BELIEF = "belief"       # 美种子 - Core beliefs
    BEHAVIOR = "behavior"   # 行种子 - Learned behaviors


@dataclass
class Seed:
    """
    A seed represents a unit of experience that influences agent behavior.
    
    In Yogacara Buddhism, seeds (bija) are stored in the Alaya-vijnana
    (storehouse consciousness) and influence future thoughts and actions.
    
    Attributes:
        id: Unique identifier (UUID)
        type: Seed type (WISDOM, COMPASSION, BELIEF, BEHAVIOR)
        content: The actual seed content (insight, behavior pattern, etc.)
        purity: Quality score (0.0-1.0), higher is better
        weight: Influence weight (0.0-1.0)
        created_at: Timestamp when seed was created
        source: Where the seed came from (interaction, emergence, etc.)
        vasana: Habit energy - number of times activated
        metadata: Additional structured data
    """
    
    type: SeedType
    content: str
    purity: float = 0.7
    weight: float = 0.5
    id: str = field(default_factory=lambda: str(uuid.uuid4())[:8])
    created_at: datetime = field(default_factory=datetime.now)
    source: str = "interaction"
    vasana: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate seed parameters"""
        if not 0.0 <= self.purity <= 1.0:
            raise ValueError(f"Purity must be between 0.0 and 1.0, got {self.purity}")
        if not 0.0 <= self.weight <= 1.0:
            raise ValueError(f"Weight must be between 0.0 and 1.0, got {self.weight}")
    
    def activate(self) -> None:
        """Increment habit energy (vasana) when seed is activated"""
        self.vasana += 1
    
    def boost_purity(self, amount: float = 0.05) -> None:
        """Increase purity (positive feedback from successful use)"""
        self.purity = min(1.0, self.purity + amount)
    
    def decay_purity(self, amount: float = 0.01) -> None:
        """Decrease purity (time decay or negative feedback)"""
        self.purity = max(0.0, self.purity - amount)
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize seed to dictionary"""
        return {
            "id": self.id,
            "type": self.type.value,
            "content": self.content,
            "purity": self.purity,
            "weight": self.weight,
            "created_at": self.created_at.isoformat(),
            "source": self.source,
            "vasana": self.vasana,
            "metadata": self.metadata,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Seed":
        """Deserialize seed from dictionary"""
        return cls(
            id=data["id"],
            type=SeedType(data["type"]),
            content=data["content"],
            purity=data["purity"],
            weight=data["weight"],
            created_at=datetime.fromisoformat(data["created_at"]),
            source=data["source"],
            vasana=data["vasana"],
            metadata=data.get("metadata", {}),
        )
    
    def __repr__(self) -> str:
        return f"Seed({self.id}, {self.type.value}, purity={self.purity:.2f})"


class SeedSystem:
    """
    Manages seed creation, validation, and lifecycle.
    
    The Seed System is responsible for:
    - Creating seeds from interactions
    - Validating seed quality
    - Managing seed lifecycle (creation, activation, decay)
    """
    
    PURITY_THRESHOLD = 0.3  # Seeds below this purity are rejected
    WEIGHT_DECAY_RATE = 0.01  # Decay rate per day
    
    def __init__(self):
        self.seeds: Dict[str, Seed] = {}
    
    def create_seed(
        self,
        type: SeedType,
        content: str,
        purity: float = 0.7,
        source: str = "interaction",
        **kwargs
    ) -> Optional[Seed]:
        """
        Create a new seed.
        
        Returns None if seed doesn't meet purity threshold.
        """
        if purity < self.PURITY_THRESHOLD:
            return None  # Reject low-quality seed
        
        seed = Seed(
            type=type,
            content=content,
            purity=purity,
            source=source,
            **kwargs
        )
        
        self.seeds[seed.id] = seed
        return seed
    
    def get_seeds_by_type(self, type: SeedType) -> list[Seed]:
        """Get all seeds of a specific type"""
        return [s for s in self.seeds.values() if s.type == type]
    
    def get_seeds_by_source(self, source: str) -> list[Seed]:
        """Get all seeds from a specific source"""
        return [s for s in self.seeds.values() if s.source == source]
    
    def get_high_purity_seeds(self, threshold: float = 0.8) -> list[Seed]:
        """Get seeds with purity above threshold"""
        return [s for s in self.seeds.values() if s.purity >= threshold]
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get seed distribution statistics"""
        total = len(self.seeds)
        if total == 0:
            return {"total": 0}
        
        by_type = {}
        for seed_type in SeedType:
            count = len(self.get_seeds_by_type(seed_type))
            by_type[seed_type.value] = {
                "count": count,
                "percentage": round(count / total * 100, 1)
            }
        
        avg_purity = sum(s.purity for s in self.seeds.values()) / total
        avg_vasana = sum(s.vasana for s in self.seeds.values()) / total
        
        return {
            "total": total,
            "by_type": by_type,
            "avg_purity": round(avg_purity, 2),
            "avg_vasana": round(avg_vasana, 1),
        }
    
    def decay_all_seeds(self, days: int = 1) -> int:
        """
        Decay purity of all seeds over time.
        
        Returns number of seeds that dropped below threshold.
        """
        decayed_count = 0
        decay_amount = self.WEIGHT_DECAY_RATE * days
        
        for seed in self.seeds.values():
            seed.decay_purity(decay_amount)
            if seed.purity < self.PURITY_THRESHOLD:
                decayed_count += 1
        
        return decayed_count
    
    def remove_low_purity_seeds(self) -> int:
        """
        Remove seeds below purity threshold.
        
        Returns number of seeds removed.
        """
        to_remove = [
            sid for sid, seed in self.seeds.items()
            if seed.purity < self.PURITY_THRESHOLD
        ]
        
        for sid in to_remove:
            del self.seeds[sid]
        
        return len(to_remove)
