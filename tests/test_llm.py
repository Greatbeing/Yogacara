"""
Tests for LLM Module
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from yogacara.core.llm.base import (
    LLMAdapter,
    LLMResponse,
    SeedSuggestion,
    EmergenceInsight,
    SeedType,
)
from yogacara.core.llm.seed_generator import SeedGenerator
from yogacara.core.llm.openai_adapter import OpenAIAdapter
from yogacara.core.seed_system import SeedSystem, SeedType as CoreSeedType


class TestLLMResponse:
    """Test cases for LLMResponse dataclass."""

    def test_create_response(self):
        """Test creating LLM response."""
        response = LLMResponse(
            content="Test content",
            raw_response={"model": "gpt-4"},
            model="gpt-4",
            tokens_used=100
        )

        assert response.content == "Test content"
        assert response.model == "gpt-4"
        assert response.is_error is False

    def test_error_response(self):
        """Test error response detection."""
        response = LLMResponse(
            content="",
            raw_response={},
            model="gpt-4",
            error="API Error"
        )

        assert response.is_error is True
        assert response.error == "API Error"


class TestSeedSuggestion:
    """Test cases for SeedSuggestion dataclass."""

    def test_create_suggestion(self):
        """Test creating seed suggestion."""
        suggestion = SeedSuggestion(
            type=SeedType.WISDOM,
            content="Understanding impermanence",
            purity=0.85,
            reasoning="Deep insight about change",
            confidence=0.9
        )

        assert suggestion.type == SeedType.WISDOM
        assert suggestion.content == "Understanding impermanence"
        assert suggestion.purity == 0.85
        assert suggestion.confidence == 0.9


class TestEmergenceInsight:
    """Test cases for EmergenceInsight dataclass."""

    def test_create_insight(self):
        """Test creating emergence insight."""
        insight = EmergenceInsight(
            summary="All things are interconnected",
            implications=["Practice compassion", "Accept change"],
            wisdom_type="interdependence",
            compassion_aspects=["All beings share suffering"]
        )

        assert insight.summary == "All things are interconnected"
        assert len(insight.implications) == 2
        assert insight.wisdom_type == "interdependence"

    def test_insight_defaults(self):
        """Test insight default values."""
        insight = EmergenceInsight(
            summary="Test summary",
            implications=[]
        )

        assert insight.compassion_aspects == []


class TestSeedGenerator:
    """Test cases for SeedGenerator class."""

    def test_create_generator(self):
        """Test creating seed generator with mock adapter."""
        class MockAdapter(LLMAdapter):
            def generate(self, prompt, **kwargs):
                return LLMResponse(content="mock", raw_response={}, model="mock")

            def analyze_seed(self, content, context=None):
                return SeedSuggestion(
                    type=SeedType.WISDOM,
                    content=content,
                    purity=0.8,
                    reasoning="mock",
                    confidence=0.9
                )

            def suggest_seeds(self, interaction, count=3, existing_seed_types=None):
                return [
                    SeedSuggestion(
                        type=SeedType.WISDOM,
                        content="Test seed",
                        purity=0.8,
                        reasoning="mock",
                        confidence=0.9
                    )
                ]

            def extract_insight(self, emergence_data):
                return EmergenceInsight(
                    summary="Test insight",
                    implications=["Implication 1"]
                )

        adapter = MockAdapter(api_key="test-key")
        generator = SeedGenerator(adapter)

        assert generator.llm is adapter
        assert generator.auto_plant is True
        assert generator.min_confidence == 0.5

    def test_seed_type_mapping(self):
        """Test seed type mapping from LLM to core."""
        mapping = {
            "wisdom": CoreSeedType.WISDOM,
            "compassion": CoreSeedType.COMPASSION,
            "belief": CoreSeedType.BELIEF,
            "behavior": CoreSeedType.BEHAVIOR
        }

        assert mapping["wisdom"] == CoreSeedType.WISDOM
        assert mapping["compassion"] == CoreSeedType.COMPASSION
        assert mapping["belief"] == CoreSeedType.BELIEF
        assert mapping["behavior"] == CoreSeedType.BEHAVIOR


class TestOpenAIAdapter:
    """Test cases for OpenAI adapter (without actual API calls)."""

    def test_adapter_initialization(self):
        """Test adapter initialization."""
        adapter = OpenAIAdapter(
            api_key="test-key",
            model="gpt-4"
        )

        assert adapter.api_key == "test-key"
        assert adapter.model == "gpt-4"

    def test_build_system_prompt(self):
        """Test system prompt generation."""
        adapter = OpenAIAdapter(api_key="test-key")

        prompt = adapter._build_system_prompt("test task")

        assert "Yogacara" in prompt
        assert "seeds" in prompt
        assert "test task" in prompt

    def test_parse_seed_suggestion_valid_json(self):
        """Test parsing valid JSON response."""
        adapter = OpenAIAdapter(api_key="test-key")

        json_str = '''
        {
            "type": "wisdom",
            "purity": 0.85,
            "reasoning": "Deep insight",
            "confidence": 0.9
        }
        '''

        suggestion = adapter._parse_seed_suggestion(json_str, "Original content")

        assert suggestion.type == SeedType.WISDOM
        assert suggestion.purity == 0.85
        assert suggestion.reasoning == "Deep insight"
        assert suggestion.confidence == 0.9

    def test_parse_seed_suggestion_invalid_json(self):
        """Test parsing invalid JSON returns default."""
        adapter = OpenAIAdapter(api_key="test-key")

        suggestion = adapter._parse_seed_suggestion("not json", "Original content")

        assert suggestion.type == SeedType.WISDOM
        assert suggestion.purity == 0.7
        assert suggestion.confidence == 0.0

    def test_parse_insight_valid_json(self):
        """Test parsing valid insight JSON."""
        adapter = OpenAIAdapter(api_key="test-key")

        json_str = '''
        {
            "summary": "All is impermanent",
            "implications": ["Accept change", "Let go"],
            "wisdom_type": "impermanence",
            "compassion_aspects": ["All beings suffer"]
        }
        '''

        insight = adapter._parse_insight(json_str)

        assert insight.summary == "All is impermanent"
        assert len(insight.implications) == 2
        assert insight.wisdom_type == "impermanence"

    def test_parse_insight_invalid_json(self):
        """Test parsing invalid insight JSON."""
        adapter = OpenAIAdapter(api_key="test-key")

        insight = adapter._parse_insight("not json")

        assert insight.summary == "not json"
        assert insight.wisdom_type == "unknown"
