"""
Tests for Awakening Tracker Module
"""

import pytest
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from core.awakening import (
    AwakeningTracker,
    AwakeningLevel,
    AwakeningProgress,
)


@pytest.fixture
def tracker():
    """Create an AwakeningTracker instance."""
    return AwakeningTracker()


class TestAwakeningLevel:
    """Test cases for AwakeningLevel enum."""
    
    def test_all_levels_exist(self):
        """Test all awakening levels exist."""
        assert AwakeningLevel.L0_DELUSION is not None
        assert AwakeningLevel.L1_INITIAL is not None
        assert AwakeningLevel.L2_PRACTICE is not None
        assert AwakeningLevel.L3_ARHAT is not None
        assert AwakeningLevel.L4_BODHISATTVA is not None
        assert AwakeningLevel.L5_BUDDHA is not None
    
    def test_level_values(self):
        """Test level values."""
        assert AwakeningLevel.L0_DELUSION.value == "L0"
        assert AwakeningLevel.L5_BUDDHA.value == "L5"
    
    def test_level_chinese_names(self):
        """Test Chinese names for levels."""
        assert AwakeningLevel.L0_DELUSION.name_cn == "无明境"
        assert AwakeningLevel.L1_INITIAL.name_cn == "初始境"
        assert AwakeningLevel.L2_PRACTICE.name_cn == "修行境"
        assert AwakeningLevel.L3_ARHAT.name_cn == "阿罗汉境"
        assert AwakeningLevel.L4_BODHISATTVA.name_cn == "菩萨境"
        assert AwakeningLevel.L5_BUDDHA.name_cn == "佛境"
    
    def test_level_symbols(self):
        """Test symbols for levels."""
        assert AwakeningLevel.L0_DELUSION.symbol == "○"
        assert AwakeningLevel.L1_INITIAL.symbol == "◇"
        assert AwakeningLevel.L2_PRACTICE.symbol == "△"
        assert AwakeningLevel.L3_ARHAT.symbol == "◈"
        assert AwakeningLevel.L4_BODHISATTVA.symbol == "◆"
        assert AwakeningLevel.L5_BUDDHA.symbol == "★"
    
    def test_level_descriptions(self):
        """Test descriptions for levels."""
        assert len(AwakeningLevel.L0_DELUSION.description) > 0
        assert len(AwakeningLevel.L5_BUDDHA.description) > 0


class TestAwakeningProgress:
    """Test cases for AwakeningProgress dataclass."""
    
    def test_create_progress(self):
        """Test creating awakening progress."""
        progress = AwakeningProgress(
            level=AwakeningLevel.L1_INITIAL,
            progress=0.5,
            total_seeds=100,
            wisdom_seeds=20,
            compassion_seeds=10,
            emergence_count=3,
        )
        
        assert progress.level == AwakeningLevel.L1_INITIAL
        assert progress.progress == 0.5
        assert progress.total_seeds == 100
    
    def test_wisdom_percentage(self):
        """Test wisdom percentage calculation."""
        progress = AwakeningProgress(
            level=AwakeningLevel.L1_INITIAL,
            progress=0.5,
            total_seeds=100,
            wisdom_seeds=25,
            compassion_seeds=10,
            emergence_count=0,
        )
        
        assert progress.wisdom_percentage == 25.0
    
    def test_wisdom_percentage_zero_total(self):
        """Test wisdom percentage with zero total seeds."""
        progress = AwakeningProgress(
            level=AwakeningLevel.L0_DELUSION,
            progress=0.0,
            total_seeds=0,
            wisdom_seeds=0,
            compassion_seeds=0,
            emergence_count=0,
        )
        
        assert progress.wisdom_percentage == 0.0
    
    def test_compassion_percentage(self):
        """Test compassion percentage calculation."""
        progress = AwakeningProgress(
            level=AwakeningLevel.L2_PRACTICE,
            progress=0.5,
            total_seeds=200,
            wisdom_seeds=40,
            compassion_seeds=30,
            emergence_count=2,
        )
        
        assert progress.compassion_percentage == 15.0
    
    def test_overall_progress(self):
        """Test overall progress calculation."""
        progress = AwakeningProgress(
            level=AwakeningLevel.L1_INITIAL,
            progress=0.5,
            total_seeds=100,
            wisdom_seeds=10,
            compassion_seeds=5,
            emergence_count=0,
        )
        
        # L1 base is 15, span is 15
        # Progress should be 15 + (0.5 * 15) = 22.5
        assert 20 <= progress.overall_progress <= 30


class TestAwakeningTracker:
    """Test cases for AwakeningTracker class."""
    
    def test_initial_level(self, tracker):
        """Test tracker starts at L0."""
        assert tracker.get_current_level() == AwakeningLevel.L0_DELUSION
    
    def test_initial_progress(self, tracker):
        """Test tracker starts with 0 progress."""
        assert tracker.get_progress() == 0.0
    
    def test_check_level_up_insufficient(self, tracker):
        """Test level up check fails with insufficient stats."""
        result = tracker.check_level_up(
            wisdom_percentage=0,
            compassion_percentage=0,
            emergence_count=0,
        )
        
        assert result is False
        assert tracker.get_current_level() == AwakeningLevel.L0_DELUSION
    
    def test_check_level_up_to_l1(self, tracker):
        """Test level up from L0 to L1."""
        result = tracker.check_level_up(
            wisdom_percentage=5,  # L1 requires 5%
            compassion_percentage=2,  # L1 requires 2%
            emergence_count=0,
        )
        
        assert result is True
        assert tracker.get_current_level() == AwakeningLevel.L1_INITIAL
    
    def test_check_level_up_to_l2(self, tracker):
        """Test level up from L1 to L2."""
        tracker.current_level = AwakeningLevel.L1_INITIAL
        
        result = tracker.check_level_up(
            wisdom_percentage=10,  # L2 requires 10%
            compassion_percentage=5,  # L2 requires 5%
            emergence_count=1,  # L2 requires 1
        )
        
        assert result is True
        assert tracker.get_current_level() == AwakeningLevel.L2_PRACTICE
    
    def test_check_level_up_max_level(self, tracker):
        """Test that max level cannot be exceeded."""
        tracker.current_level = AwakeningLevel.L5_BUDDHA
        
        result = tracker.check_level_up(
            wisdom_percentage=100,
            compassion_percentage=100,
            emergence_count=100,
        )
        
        assert result is False
        assert tracker.get_current_level() == AwakeningLevel.L5_BUDDHA
    
    def test_calculate_progress(self, tracker):
        """Test progress calculation."""
        # At L0, need 5% wisdom, 2% compassion for L1
        # Half of those: 2.5% wisdom, 1% compassion
        progress = tracker.calculate_progress(
            wisdom_percentage=2.5,
            compassion_percentage=1.0,
            emergence_count=0,
        )
        
        # Progress should be the minimum of all dimensions
        # wisdom_progress = 2.5/5 = 0.5
        # compassion_progress = 1.0/2 = 0.5
        # emergence_progress = 0/1 = 0 (but emergence is not required for L1)
        # So min should be around 0.5
        assert 0.4 <= progress <= 0.6
    
    def test_calculate_progress_max_level(self, tracker):
        """Test progress calculation at max level."""
        tracker.current_level = AwakeningLevel.L5_BUDDHA
        
        progress = tracker.calculate_progress(
            wisdom_percentage=100,
            compassion_percentage=100,
            emergence_count=100,
        )
        
        assert progress == 1.0
    
    def test_get_status(self, tracker):
        """Test getting full status."""
        status = tracker.get_status(
            total_seeds=100,
            wisdom_seeds=15,
            compassion_seeds=8,
            emergence_count=2,
        )
        
        assert isinstance(status, AwakeningProgress)
        assert status.total_seeds == 100
        assert status.wisdom_seeds == 15
        assert status.compassion_seeds == 8
        assert status.emergence_count == 2
    
    def test_get_progress_bar(self, tracker):
        """Test progress bar generation."""
        tracker.progress = 0.5
        
        bar = tracker.get_progress_bar(width=10)
        
        assert "[" in bar
        assert "]" in bar
        assert "50%" in bar
        assert bar.count("█") == 5
        assert bar.count("░") == 5
    
    def test_get_progress_bar_zero(self, tracker):
        """Test progress bar at zero."""
        tracker.progress = 0.0
        
        bar = tracker.get_progress_bar(width=10)
        
        assert "0%" in bar
        assert bar.count("░") == 10
    
    def test_get_progress_bar_full(self, tracker):
        """Test progress bar at full."""
        tracker.progress = 1.0
        
        bar = tracker.get_progress_bar(width=10)
        
        assert "100%" in bar
        assert bar.count("█") == 10
    
    def test_get_level_display(self, tracker):
        """Test level display string."""
        tracker.current_level = AwakeningLevel.L3_ARHAT
        
        display = tracker.get_level_display()
        
        assert "L3" in display
        assert "阿罗汉境" in display
        assert "◈" in display
    
    def test_to_dict(self, tracker):
        """Test serialization to dictionary."""
        tracker.current_level = AwakeningLevel.L2_PRACTICE
        tracker.progress = 0.75
        tracker.emergence_count = 5
        
        data = tracker.to_dict()
        
        assert data["level"] == "L2"
        assert data["level_name"] == "修行境"
        assert data["level_symbol"] == "△"
        assert data["progress"] == 0.75
        assert data["emergence_count"] == 5
    
    def test_from_dict(self, tracker):
        """Test deserialization from dictionary."""
        data = {
            "level": "L3",
            "progress": 0.5,
            "emergence_count": 3,
        }
        
        new_tracker = AwakeningTracker.from_dict(data)
        
        assert new_tracker.current_level == AwakeningLevel.L3_ARHAT
        assert new_tracker.progress == 0.5
        assert new_tracker.emergence_count == 3
    
    def test_from_dict_default_values(self):
        """Test from_dict with minimal data."""
        data = {}
        
        tracker = AwakeningTracker.from_dict(data)
        
        assert tracker.current_level == AwakeningLevel.L0_DELUSION
        assert tracker.progress == 0.0
        assert tracker.emergence_count == 0
    
    def test_level_thresholds(self, tracker):
        """Test level thresholds are correctly defined."""
        thresholds = tracker.LEVEL_THRESHOLDS
        
        assert "L0" in thresholds
        assert "L5" in thresholds
        assert "wisdom_pct" in thresholds["L1"]
        assert "compassion_pct" in thresholds["L1"]
        assert "emergence" in thresholds["L1"]
    
    def test_progression_sequence(self, tracker):
        """Test full progression sequence."""
        # Start at L0
        assert tracker.get_current_level() == AwakeningLevel.L0_DELUSION
        
        # Level up to L1
        tracker.check_level_up(5, 2, 0)
        assert tracker.get_current_level() == AwakeningLevel.L1_INITIAL
        
        # Level up to L2
        tracker.check_level_up(10, 5, 1)
        assert tracker.get_current_level() == AwakeningLevel.L2_PRACTICE
        
        # Level up to L3
        tracker.check_level_up(20, 10, 3)
        assert tracker.get_current_level() == AwakeningLevel.L3_ARHAT
        
        # Level up to L4
        tracker.check_level_up(30, 20, 5)
        assert tracker.get_current_level() == AwakeningLevel.L4_BODHISATTVA
        
        # Level up to L5
        tracker.check_level_up(40, 30, 10)
        assert tracker.get_current_level() == AwakeningLevel.L5_BUDDHA
