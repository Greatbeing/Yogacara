"""
Tests for Emergence Engine Module
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.emergence import EmergenceEngine, Emergence, EmergenceType
from core.seed_system import Seed, SeedType


@pytest.fixture
def engine():
    """Create an EmergenceEngine instance."""
    return EmergenceEngine()


@pytest.fixture
def sample_seeds():
    """Create sample seeds for testing."""
    return [
        Seed(type=SeedType.WISDOM, content="Seed 1", purity=0.8, vasana=5),
        Seed(type=SeedType.COMPASSION, content="Seed 2", purity=0.9, vasana=3),
        Seed(type=SeedType.BELIEF, content="Seed 3", purity=0.7, vasana=2),
    ]


class TestEmergenceType:
    """Test cases for EmergenceType enum."""
    
    def test_all_emergence_types(self):
        """Test all emergence types exist."""
        assert EmergenceType.FUSION is not None
        assert EmergenceType.TENSION is not None
        assert EmergenceType.LEAP is not None
    
    def test_emergence_type_values(self):
        """Test emergence type values."""
        assert EmergenceType.FUSION.value == "fusion"
        assert EmergenceType.TENSION.value == "tension"
        assert EmergenceType.LEAP.value == "leap"


class TestEmergence:
    """Test cases for Emergence dataclass."""
    
    def test_create_emergence(self):
        """Test creating an emergence event."""
        seed_ids = ["seed1", "seed2", "seed3"]
        
        emergence = Emergence(
            seed_ids=seed_ids,
            emergence_type=EmergenceType.FUSION,
            strength=0.85,
            insight="Test insight",
        )
        
        assert emergence.seed_ids == seed_ids
        assert emergence.emergence_type == EmergenceType.FUSION
        assert emergence.strength == 0.85
        assert emergence.insight == "Test insight"
        assert emergence.contributing_seeds == []
    
    def test_emergence_with_seeds(self, sample_seeds):
        """Test creating emergence with contributing seeds."""
        emergence = Emergence(
            seed_ids=[s.id for s in sample_seeds],
            emergence_type=EmergenceType.FUSION,
            strength=0.9,
            insight="Combined wisdom",
            contributing_seeds=sample_seeds,
        )
        
        assert len(emergence.contributing_seeds) == 3


class TestEmergenceEngine:
    """Test cases for EmergenceEngine class."""
    
    def test_engine_initialization(self, engine):
        """Test engine initializes with correct defaults."""
        assert engine.MIN_SEEDS_FOR_EMERGENCE == 3
        assert engine.SYNERGY_THRESHOLD == 0.6
        assert engine.STRENGTH_THRESHOLD == 0.7
    
    def test_check_emergence_insufficient_seeds(self, engine):
        """Test that insufficient seeds don't trigger emergence."""
        seeds = [
            Seed(type=SeedType.WISDOM, content="Seed 1"),
            Seed(type=SeedType.COMPASSION, content="Seed 2"),
        ]
        
        result = engine.check_emergence(seeds)
        
        assert result is None
    
    def test_check_emergence_low_synergy(self, engine):
        """Test that low synergy doesn't trigger emergence."""
        # Seeds of same type have lower synergy
        seeds = [
            Seed(type=SeedType.WISDOM, content="Seed 1"),
            Seed(type=SeedType.WISDOM, content="Seed 2"),
            Seed(type=SeedType.WISDOM, content="Seed 3"),
        ]
        
        result = engine.check_emergence(seeds)
        
        # May or may not trigger depending on exact synergy calculation
        # but should be based on thresholds
        assert result is None or result.strength < engine.STRENGTH_THRESHOLD
    
    def test_check_emergence_triggers_with_good_seeds(self, engine, sample_seeds):
        """Test that good seed combinations trigger emergence."""
        result = engine.check_emergence(sample_seeds)
        
        assert result is not None
        assert isinstance(result, Emergence)
        assert result.strength >= engine.STRENGTH_THRESHOLD
    
    def test_calculate_synergy_single_seed(self, engine):
        """Test synergy calculation with single seed."""
        seeds = [Seed(type=SeedType.WISDOM, content="Single seed")]
        
        synergy = engine.calculate_synergy(seeds)
        
        assert synergy == 0.0
    
    def test_calculate_synergy_same_type(self, engine):
        """Test synergy calculation with same type seeds."""
        seeds = [
            Seed(type=SeedType.WISDOM, content="Seed 1"),
            Seed(type=SeedType.WISDOM, content="Seed 2"),
        ]
        
        synergy = engine.calculate_synergy(seeds)
        
        # Same type has lower synergy
        assert 0.0 <= synergy <= 1.0
    
    def test_calculate_synergy_different_types(self, engine):
        """Test synergy calculation with different types."""
        seeds = [
            Seed(type=SeedType.WISDOM, content="Wisdom"),
            Seed(type=SeedType.COMPASSION, content="Compassion"),
        ]
        
        synergy = engine.calculate_synergy(seeds)
        
        # Different types should have higher synergy
        assert synergy > 0.0
    
    def test_calculate_synergy_optimal_combination(self, engine):
        """Test synergy with optimal seed combination."""
        # WISDOM + COMPASSION has synergy of 1.0 in matrix
        seeds = [
            Seed(type=SeedType.WISDOM, content="Wisdom seed", purity=0.9),
            Seed(type=SeedType.COMPASSION, content="Compassion seed", purity=0.9),
            Seed(type=SeedType.BELIEF, content="Belief seed", purity=0.9),
        ]
        
        synergy = engine.calculate_synergy(seeds)
        
        assert synergy >= 0.6  # Should have good synergy
    
    def test_determine_emergence_type_fusion(self, engine):
        """Test fusion emergence type detection."""
        seeds = [
            Seed(type=SeedType.WISDOM, content="Seed 1"),
            Seed(type=SeedType.COMPASSION, content="Seed 2"),
            Seed(type=SeedType.BELIEF, content="Seed 3"),
        ]
        
        emergence_type = engine._determine_emergence_type(seeds)
        
        assert emergence_type == EmergenceType.FUSION
    
    def test_determine_emergence_type_tension(self, engine):
        """Test tension emergence type detection."""
        seeds = [
            Seed(type=SeedType.WISDOM, content="Wisdom seed"),
            Seed(type=SeedType.BEHAVIOR, content="Behavior seed"),
            Seed(type=SeedType.BELIEF, content="Belief seed"),
        ]
        
        emergence_type = engine._determine_emergence_type(seeds)
        
        assert emergence_type == EmergenceType.TENSION
    
    def test_determine_emergence_type_leap(self, engine):
        """Test leap emergence type detection."""
        seeds = [
            Seed(type=SeedType.WISDOM, content="Seed 1"),
            Seed(type=SeedType.WISDOM, content="Seed 2"),
            Seed(type=SeedType.WISDOM, content="Seed 3"),
        ]
        
        emergence_type = engine._determine_emergence_type(seeds)
        
        assert emergence_type == EmergenceType.LEAP
    
    def test_calculate_strength(self, engine, sample_seeds):
        """Test emergence strength calculation."""
        synergy = engine.calculate_synergy(sample_seeds)
        strength = engine._calculate_strength(sample_seeds, synergy)
        
        assert 0.0 <= strength <= 1.0
        assert strength >= synergy  # Strength includes synergy as base
    
    def test_calculate_strength_high_vasana(self, engine):
        """Test that high vasana increases strength."""
        seeds_low = [
            Seed(type=SeedType.WISDOM, content="S1", vasana=1),
            Seed(type=SeedType.COMPASSION, content="S2", vasana=1),
            Seed(type=SeedType.BELIEF, content="S3", vasana=1),
        ]
        
        seeds_high = [
            Seed(type=SeedType.WISDOM, content="S1", vasana=50),
            Seed(type=SeedType.COMPASSION, content="S2", vasana=50),
            Seed(type=SeedType.BELIEF, content="S3", vasana=50),
        ]
        
        synergy = engine.calculate_synergy(seeds_low)
        strength_low = engine._calculate_strength(seeds_low, synergy)
        
        synergy_high = engine.calculate_synergy(seeds_high)
        strength_high = engine._calculate_strength(seeds_high, synergy_high)
        
        # Higher vasana should contribute to higher strength
        assert strength_high >= strength_low
    
    def test_generate_insight(self, engine, sample_seeds):
        """Test insight generation."""
        insight = engine.generate_insight(sample_seeds, EmergenceType.FUSION)
        
        assert insight is not None
        assert isinstance(insight, str)
        assert len(insight) > 0
    
    def test_generate_insight_different_types(self, engine, sample_seeds):
        """Test insight generation for different emergence types."""
        for emergence_type in EmergenceType:
            insight = engine.generate_insight(sample_seeds, emergence_type)
            assert insight is not None
            assert len(insight) > 0
    
    def test_synergy_matrix_values(self, engine):
        """Test synergy matrix has expected values."""
        assert engine.SYNERGY_MATRIX[(SeedType.WISDOM, SeedType.COMPASSION)] == 1.0
        assert engine.SYNERGY_MATRIX[(SeedType.COMPASSION, SeedType.BELIEF)] == 0.9
    
    def test_strength_never_exceeds_one(self, engine):
        """Test that strength is capped at 1.0."""
        # Create seeds with maxed values
        seeds = [
            Seed(type=SeedType.WISDOM, content="S1", purity=1.0, vasana=100),
            Seed(type=SeedType.COMPASSION, content="S2", purity=1.0, vasana=100),
            Seed(type=SeedType.BELIEF, content="S3", purity=1.0, vasana=100),
        ]
        
        synergy = engine.calculate_synergy(seeds)
        strength = engine._calculate_strength(seeds, synergy)
        
        assert strength <= 1.0
