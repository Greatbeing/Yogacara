"""
Base LLM Adapter for Yogacara Framework

Abstract base class and data models for LLM integrations.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Optional, List, Dict, Any


class SeedType(Enum):
    """Seed types for classification."""
    WISDOM = "wisdom"
    COMPASSION = "compassion"
    BELIEF = "belief"
    BEHAVIOR = "behavior"


@dataclass
class LLMResponse:
    """Response from LLM API."""
    content: str
    raw_response: Dict[str, Any]
    model: str
    tokens_used: Optional[int] = None
    error: Optional[str] = None

    @property
    def is_error(self) -> bool:
        return self.error is not None


@dataclass
class SeedSuggestion:
    """Suggested seed from LLM analysis."""
    type: SeedType
    content: str
    purity: float
    reasoning: str
    confidence: float


@dataclass
class EmergenceInsight:
    """Insight extracted from emergence event."""
    summary: str
    implications: List[str]
    wisdom_type: Optional[str] = None
    compassion_aspects: List[str] = None

    def __post_init__(self):
        if self.compassion_aspects is None:
            self.compassion_aspects = []


class LLMAdapter(ABC):
    """
    Abstract base class for LLM adapters.

    All LLM integrations must implement these methods:
    - generate(): Generate text from prompt
    - analyze_seed(): Classify and rate a seed
    - suggest_seeds(): Generate seed suggestions from interaction
    - extract_insight(): Extract insight from emergence event
    """

    def __init__(self, api_key: str, model: str = "gpt-4", **kwargs):
        """
        Initialize LLM adapter.

        Args:
            api_key: API key for the LLM service
            model: Model identifier to use
            **kwargs: Additional provider-specific options
        """
        self.api_key = api_key
        self.model = model
        self.config = kwargs

    @abstractmethod
    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """
        Generate text from a prompt.

        Args:
            prompt: Input prompt
            **kwargs: Additional generation options

        Returns:
            LLMResponse with generated content
        """
        pass

    @abstractmethod
    def analyze_seed(
        self,
        content: str,
        context: Optional[str] = None
    ) -> SeedSuggestion:
        """
        Analyze content and suggest seed classification.

        Args:
            content: Content to analyze
            context: Optional context for better classification

        Returns:
            SeedSuggestion with type, purity, and reasoning
        """
        pass

    @abstractmethod
    def suggest_seeds(
        self,
        interaction: str,
        count: int = 3,
        existing_seed_types: Optional[List[SeedType]] = None
    ) -> List[SeedSuggestion]:
        """
        Generate seed suggestions from an interaction.

        Args:
            interaction: User interaction text
            count: Number of seeds to suggest
            existing_seed_types: Types already present to avoid duplication

        Returns:
            List of SeedSuggestion objects
        """
        pass

    @abstractmethod
    def extract_insight(
        self,
        emergence_data: Dict[str, Any]
    ) -> EmergenceInsight:
        """
        Extract meaningful insight from emergence event data.

        Args:
            emergence_data: Dictionary containing emergence information

        Returns:
            EmergenceInsight with summary and implications
        """
        pass

    def _build_system_prompt(self, task: str) -> str:
        """
        Build system prompt for Yogacara context.

        Args:
            task: Task description

        Returns:
            Formatted system prompt
        """
        return f"""You are a wise teacher following the Yogacara Buddhist philosophy.

Yogacara (Consciousness-Only) teaches that our experiences create "seeds" (bija)
in the storehouse consciousness (Alaya-vijnana). These seeds later manifest as
actions, thoughts, and understanding.

Your task: {task}

Focus on wisdom that helps reduce suffering and increase compassion.
Be concise but profound."""
