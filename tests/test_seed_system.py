"""
Tests for Seed System Module
"""

import pytest
from datetime import datetime
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.seed_system import Seed, SeedType, SeedSystem


class TestSeed:
    """Test cases for Seed dataclass."""
    
    def test_create_seed_with_defaults(self):
        """Test creating a seed with default values."""
        seed = Seed(type=SeedType.WISDOM, content="Test wisdom")
        
        assert seed.type == SeedType.WISDOM
        assert seed.content == "Test wisdom"
        assert seed.purity == 0.7
        assert seed.weight == 0.5
        assert seed.vasana == 0
        assert seed.source == "interaction"
        assert seed.id is not None
        assert seed.created_at is not None
    
    def test_create_seed_with_custom_values(self):
        """Test creating a seed with custom values."""
        seed = Seed(
            type=SeedType.COMPASSION,
            content="Help others",
            purity=0.9,
            weight=0.8,
            source="teaching",
            vasana=5,
        )
        
        assert seed.purity == 0.9
        assert seed.weight == 0.8
        assert seed.source == "teaching"
        assert seed.vasana == 5
    
    def test_seed_invalid_purity_raises(self):
        """Test that invalid purity raises ValueError."""
        with pytest.raises(ValueError, match="Purity must be between"):
            Seed(type=SeedType.WISDOM, content="Test", purity=1.5)
        
        with pytest.raises(ValueError, match="Purity must be between"):
            Seed(type=SeedType.WISDOM, content="Test", purity=-0.1)
    
    def test_seed_invalid_weight_raises(self):
        """Test that invalid weight raises ValueError."""
        with pytest.raises(ValueError, match="Weight must be between"):
            Seed(type=SeedType.WISDOM, content="Test", weight=1.5)
        
        with pytest.raises(ValueError, match="Weight must be between"):
            Seed(type=SeedType.WISDOM, content="Test", weight=-0.1)
    
    def test_seed_activate(self):
        """Test seed activation increments vasana."""
        seed = Seed(type=SeedType.WISDOM, content="Test")
        assert seed.vasana == 0
        
        seed.activate()
        assert seed.vasana == 1
        
        seed.activate()
        assert seed.vasana == 2
    
    def test_seed_boost_purity(self):
        """Test boosting seed purity."""
        seed = Seed(type=SeedType.WISDOM, content="Test", purity=0.5)
        
        seed.boost_purity(0.1)
        assert seed.purity == 0.6
        
        # Should not exceed 1.0
        seed.boost_purity(0.5)
        assert seed.purity == 1.0
    
    def test_seed_decay_purity(self):
        """Test decaying seed purity."""
        seed = Seed(type=SeedType.WISDOM, content="Test", purity=0.5)
        
        seed.decay_purity(0.1)
        assert seed.purity == 0.4
        
        # Should not go below 0.0
        seed.decay_purity(1.0)
        assert seed.purity == 0.0
    
    def test_seed_to_dict(self):
        """Test serializing seed to dictionary."""
        seed = Seed(
            type=SeedType.BELIEF,
            content="Harmony is valuable",
            purity=0.8,
            weight=0.6,
            source="experience",
            vasana=3,
        )
        
        data = seed.to_dict()
        
        assert data["type"] == "belief"
        assert data["content"] == "Harmony is valuable"
        assert data["purity"] == 0.8
        assert data["weight"] == 0.6
        assert data["source"] == "experience"
        assert data["vasana"] == 3
        assert "id" in data
        assert "created_at" in data
    
    def test_seed_from_dict(self):
        """Test deserializing seed from dictionary."""
        data = {
            "id": "test-123",
            "type": "compassion",
            "content": "Show kindness",
            "purity": 0.85,
            "weight": 0.7,
            "created_at": "2024-01-01T12:00:00",
            "source": "teaching",
            "vasana": 10,
            "metadata": {"category": "empathy"},
        }
        
        seed = Seed.from_dict(data)
        
        assert seed.id == "test-123"
        assert seed.type == SeedType.COMPASSION
        assert seed.content == "Show kindness"
        assert seed.purity == 0.85
        assert seed.weight == 0.7
        assert seed.source == "teaching"
        assert seed.vasana == 10
        assert seed.metadata == {"category": "empathy"}
    
    def test_seed_repr(self):
        """Test seed string representation."""
        seed = Seed(type=SeedType.WISDOM, content="Test", purity=0.75)
        repr_str = repr(seed)
        
        assert "Seed(" in repr_str
        assert "wisdom" in repr_str
        assert "0.75" in repr_str or "0.7" in repr_str


class TestSeedType:
    """Test cases for SeedType enum."""
    
    def test_seed_type_values(self):
        """Test all seed types have correct values."""
        assert SeedType.WISDOM.value == "wisdom"
        assert SeedType.COMPASSION.value == "compassion"
        assert SeedType.BELIEF.value == "belief"
        assert SeedType.BEHAVIOR.value == "behavior"
    
    def test_seed_type_count(self):
        """Test there are exactly 4 seed types."""
        assert len(SeedType) == 4


class TestSeedSystem:
    """Test cases for SeedSystem class."""
    
    def test_create_seed_above_threshold(self):
        """Test creating a seed above purity threshold."""
        system = SeedSystem()
        
        seed = system.create_seed(
            type=SeedType.WISDOM,
            content="Valid wisdom",
            purity=0.8,
        )
        
        assert seed is not None
        assert seed.type == SeedType.WISDOM
        assert seed.content == "Valid wisdom"
        assert len(system.seeds) == 1
    
    def test_create_seed_below_threshold(self):
        """Test that low purity seeds are rejected."""
        system = SeedSystem()
        
        seed = system.create_seed(
            type=SeedType.WISDOM,
            content="Low quality seed",
            purity=0.2,  # Below default threshold of 0.3
        )
        
        assert seed is None
        assert len(system.seeds) == 0
    
    def test_create_seed_at_threshold(self):
        """Test creating a seed at exact threshold."""
        system = SeedSystem()
        
        seed = system.create_seed(
            type=SeedType.WISDOM,
            content="Threshold seed",
            purity=0.3,  # At exact threshold
        )
        
        assert seed is not None
    
    def test_get_seeds_by_type(self):
        """Test filtering seeds by type."""
        system = SeedSystem()
        
        system.create_seed(SeedType.WISDOM, "Wisdom 1", purity=0.8)
        system.create_seed(SeedType.WISDOM, "Wisdom 2", purity=0.9)
        system.create_seed(SeedType.COMPASSION, "Compassion 1", purity=0.7)
        system.create_seed(SeedType.BELIEF, "Belief 1", purity=0.8)
        
        wisdom_seeds = system.get_seeds_by_type(SeedType.WISDOM)
        assert len(wisdom_seeds) == 2
        
        compassion_seeds = system.get_seeds_by_type(SeedType.COMPASSION)
        assert len(compassion_seeds) == 1
    
    def test_get_seeds_by_source(self):
        """Test filtering seeds by source."""
        system = SeedSystem()
        
        system.create_seed(SeedType.WISDOM, "Seed 1", source="interaction", purity=0.8)
        system.create_seed(SeedType.WISDOM, "Seed 2", source="teaching", purity=0.8)
        system.create_seed(SeedType.WISDOM, "Seed 3", source="interaction", purity=0.8)
        
        interaction_seeds = system.get_seeds_by_source("interaction")
        assert len(interaction_seeds) == 2
        
        teaching_seeds = system.get_seeds_by_source("teaching")
        assert len(teaching_seeds) == 1
    
    def test_get_high_purity_seeds(self):
        """Test getting high purity seeds."""
        system = SeedSystem()
        
        system.create_seed(SeedType.WISDOM, "Seed 1", purity=0.9)
        system.create_seed(SeedType.WISDOM, "Seed 2", purity=0.7)
        system.create_seed(SeedType.WISDOM, "Seed 3", purity=0.85)
        
        high_purity = system.get_high_purity_seeds(threshold=0.8)
        assert len(high_purity) == 2
    
    def test_get_statistics(self):
        """Test getting seed statistics."""
        system = SeedSystem()
        
        system.create_seed(SeedType.WISDOM, "Seed 1", purity=0.9)
        system.create_seed(SeedType.COMPASSION, "Seed 2", purity=0.7)
        system.create_seed(SeedType.WISDOM, "Seed 3", purity=0.85)
        
        stats = system.get_statistics()
        
        assert stats["total"] == 3
        assert stats["by_type"]["wisdom"]["count"] == 2
        assert stats["by_type"]["compassion"]["count"] == 1
        assert 0.0 < stats["avg_purity"] <= 1.0
    
    def test_statistics_empty_system(self):
        """Test statistics for empty seed system."""
        system = SeedSystem()
        
        stats = system.get_statistics()
        assert stats["total"] == 0
    
    def test_decay_all_seeds(self):
        """Test decaying all seeds."""
        system = SeedSystem()
        
        seed1 = system.create_seed(SeedType.WISDOM, "Seed 1", purity=0.35)
        seed2 = system.create_seed(SeedType.WISDOM, "Seed 2", purity=0.5)
        
        # Decay should affect all seeds
        decayed_count = system.decay_all_seeds(days=1)
        
        # Both seeds should have decayed
        assert seed1.purity < 0.35
        assert seed2.purity < 0.5
    
    def test_decay_below_threshold(self):
        """Test counting seeds that drop below threshold."""
        system = SeedSystem()
        
        seed = system.create_seed(SeedType.WISDOM, "Seed 1", purity=0.31)
        
        # Decay once (0.31 - 0.01 = 0.30)
        decayed = system.decay_all_seeds(days=1)
        assert decayed == 0
        
        # Decay again (0.30 - 0.01 = 0.29, below 0.3)
        decayed = system.decay_all_seeds(days=1)
        assert decayed == 1
