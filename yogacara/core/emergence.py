"""
Emergence Engine - 涌现引擎

Detects and triggers wisdom emergence when seeds synergize.
Based on the concept that wisdom emerges from the interaction of multiple seeds,
not from simple accumulation.
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple
import math

from .seed_system import Seed, SeedType


class EmergenceType(Enum):
    """Types of emergence based on seed interaction patterns"""
    FUSION = "fusion"       # 种子融合：Multiple seeds merge into new insight
    TENSION = "tension"     # 张力涌现：Opposing seeds create synthesis
    LEAP = "leap"          # 跃迁涌现：Quantitative change leads to qualitative leap


@dataclass
class Emergence:
    """
    Represents an emergence event.
    
    Emergence occurs when seeds synergize to produce wisdom that
    transcends simple addition - the whole is greater than parts.
    """
    seed_ids: List[str]
    emergence_type: EmergenceType
    strength: float  # 0.0 - 1.0
    insight: Optional[str] = None
    contributing_seeds: List[Seed] = None
    
    def __post_init__(self):
        if self.contributing_seeds is None:
            self.contributing_seeds = []


class EmergenceEngine:
    """
    The Emergence Engine detects when seeds synergize to produce wisdom.
    
    Key Principles:
    1. Emergence requires seed diversity (not just quantity)
    2. Purity amplifies emergence strength
    3. Complementary seed types boost synergy
    4. High vasana (habit) seeds are more likely to trigger emergence
    
    Emergence Formula:
    strength = f(seed_count, seed_purity, seed_diversity, synergy_score)
    """
    
    # Emergence thresholds
    MIN_SEEDS_FOR_EMERGENCE = 3
    SYNERGY_THRESHOLD = 0.6
    STRENGTH_THRESHOLD = 0.7
    
    # Seed type synergy matrix
    # Higher values indicate better synergy between types
    SYNERGY_MATRIX = {
        (SeedType.WISDOM, SeedType.COMPASSION): 1.0,    # 悲智双运
        (SeedType.WISDOM, SeedType.BELIEF): 0.8,
        (SeedType.COMPASSION, SeedType.BELIEF): 0.9,
        (SeedType.BEHAVIOR, SeedType.WISDOM): 0.6,
        (SeedType.BEHAVIOR, SeedType.COMPASSION): 0.5,
    }
    
    def check_emergence(self, seeds: List[Seed]) -> Optional[Emergence]:
        """
        Check if given seeds can trigger emergence.
        
        Returns Emergence object if emergence detected, None otherwise.
        """
        if len(seeds) < self.MIN_SEEDS_FOR_EMERGENCE:
            return None
        
        # Calculate synergy score
        synergy = self.calculate_synergy(seeds)
        
        if synergy < self.SYNERGY_THRESHOLD:
            return None
        
        # Determine emergence type
        emergence_type = self._determine_emergence_type(seeds)
        
        # Calculate strength
        strength = self._calculate_strength(seeds, synergy)
        
        if strength < self.STRENGTH_THRESHOLD:
            return None
        
        # Generate insight
        insight = self.generate_insight(seeds, emergence_type)
        
        return Emergence(
            seed_ids=[s.id for s in seeds],
            emergence_type=emergence_type,
            strength=strength,
            insight=insight,
            contributing_seeds=seeds
        )
    
    def calculate_synergy(self, seeds: List[Seed]) -> float:
        """
        Calculate synergy score between seeds.
        
        Synergy is based on:
        - Type diversity (more types = higher synergy)
        - Type combinations (some types synergize better)
        - Purity alignment (similar purity = better synergy)
        """
        if len(seeds) < 2:
            return 0.0
        
        # Type diversity score
        types_present = set(s.type for s in seeds)
        diversity_score = len(types_present) / len(SeedType)
        
        # Type synergy score
        synergy_sum = 0.0
        pair_count = 0
        
        for i, seed1 in enumerate(seeds):
            for seed2 in seeds[i+1:]:
                pair = (seed1.type, seed2.type)
                reverse_pair = (seed2.type, seed1.type)
                
                synergy_value = self.SYNERGY_MATRIX.get(
                    pair, self.SYNERGY_MATRIX.get(reverse_pair, 0.3)
                )
                synergy_sum += synergy_value
                pair_count += 1
        
        type_synergy = synergy_sum / pair_count if pair_count > 0 else 0
        
        # Purity alignment score
        purity_values = [s.purity for s in seeds]
        purity_variance = sum(
            (p - sum(purity_values)/len(purity_values))**2 
            for p in purity_values
        ) / len(purity_values)
        purity_alignment = 1.0 - min(purity_variance, 1.0)
        
        # Combined synergy
        synergy = (
            diversity_score * 0.4 +
            type_synergy * 0.4 +
            purity_alignment * 0.2
        )
        
        return round(synergy, 2)
    
    def _determine_emergence_type(self, seeds: List[Seed]) -> EmergenceType:
        """Determine the type of emergence based on seed patterns"""
        types = [s.type for s in seeds]
        
        # Check for tension (opposing seeds)
        if SeedType.WISDOM in types and SeedType.BEHAVIOR in types:
            return EmergenceType.TENSION
        
        # Check for leap (many seeds of same type with high purity)
        type_counts = {}
        for t in types:
            type_counts[t] = type_counts.get(t, 0) + 1
        
        max_count = max(type_counts.values())
        if max_count >= 3:
            return EmergenceType.LEAP
        
        # Default to fusion
        return EmergenceType.FUSION
    
    def _calculate_strength(self, seeds: List[Seed], synergy: float) -> float:
        """Calculate emergence strength"""
        # Base strength from synergy
        base = synergy
        
        # Purity bonus
        avg_purity = sum(s.purity for s in seeds) / len(seeds)
        purity_bonus = avg_purity * 0.3
        
        # Vasana bonus (seeds used more have more influence)
        total_vasana = sum(s.vasana for s in seeds)
        vasana_bonus = min(total_vasana / 100, 0.2)
        
        # Quantity bonus (more seeds = stronger emergence)
        quantity_bonus = min(len(seeds) / 10, 0.1)
        
        strength = base + purity_bonus + vasana_bonus + quantity_bonus
        
        return round(min(strength, 1.0), 2)
    
    def generate_insight(
        self,
        seeds: List[Seed],
        emergence_type: EmergenceType
    ) -> str:
        """
        Generate emergent insight from seeds.
        
        This is where the magic happens - creating new wisdom
        from the combination of seeds.
        """
        # Group seeds by type
        by_type = {}
        for seed in seeds:
            if seed.type not in by_type:
                by_type[seed.type] = []
            by_type[seed.type].append(seed.content)
        
        # Generate insight based on emergence type
        if emergence_type == EmergenceType.FUSION:
            # Fusion: Combine insights from different perspectives
            parts = []
            for seed_type, contents in by_type.items():
                key_point = contents[0] if contents else ""
                parts.append(f"{key_point}")
            
            return " + ".join(parts[:2]) + " → 综合洞见"
        
        elif emergence_type == EmergenceType.TENSION:
            # Tension: Synthesis from opposing forces
            wisdom_seeds = by_type.get(SeedType.WISDOM, [])
            behavior_seeds = by_type.get(SeedType.BEHAVIOR, [])
            
            if wisdom_seeds and behavior_seeds:
                return f"{wisdom_seeds[0]} ←→ {behavior_seeds[0]} → 平衡之道"
            
            return "张力产生新平衡"
        
        elif emergence_type == EmergenceType.LEAP:
            # Leap: Deepening of understanding
            main_type = max(by_type.keys(), key=lambda t: len(by_type[t]))
            contents = by_type[main_type]
            
            return f"{contents[0]} → 深化理解 → 新层次"
        
        return "智慧涌现"
    
    def get_emergence_potential(self, seeds: List[Seed]) -> float:
        """
        Calculate emergence potential without triggering.
        
        Useful for UI feedback.
        """
        if len(seeds) < self.MIN_SEEDS_FOR_EMERGENCE:
            return 0.0
        
        synergy = self.calculate_synergy(seeds)
        strength = self._calculate_strength(seeds, synergy)
        
        return strength
