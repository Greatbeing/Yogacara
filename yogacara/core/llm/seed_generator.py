"""
Seed Generator - LLM-powered seed creation for Yogacara

Combines LLM analysis with seed system to automatically generate
high-quality seeds from interactions.
"""

from typing import List, Optional, Dict, Any

from yogacara.core.seed_system import Seed, SeedType, SeedSystem
from yogacara.core.alaya_store import AlayaStore
from yogacara.core.llm.base import LLMAdapter, SeedSuggestion


class SeedGenerator:
    """
    Generates seeds using LLM analysis.

    This class bridges the LLM adapter with the seed system,
    automatically creating and storing seeds based on interactions.
    """

    def __init__(
        self,
        llm_adapter: LLMAdapter,
        seed_system: Optional[SeedSystem] = None,
        alaya_store: Optional[AlayaStore] = None,
        auto_plant: bool = True,
        min_confidence: float = 0.5
    ):
        """
        Initialize SeedGenerator.

        Args:
            llm_adapter: LLM adapter for analysis
            seed_system: SeedSystem instance for in-memory storage
            alaya_store: AlayaStore instance for persistent storage
            auto_plant: Automatically plant seeds after generation
            min_confidence: Minimum confidence threshold for planting
        """
        self.llm = llm_adapter
        self.seed_system = seed_system or SeedSystem()
        self.alaya_store = alaya_store
        self.auto_plant = auto_plant
        self.min_confidence = min_confidence

    def process_interaction(
        self,
        interaction: str,
        context: Optional[str] = None,
        max_seeds: int = 3
    ) -> List[Seed]:
        """
        Process an interaction and generate seeds.

        Args:
            interaction: User interaction text
            context: Optional context for better analysis
            max_seeds: Maximum number of seeds to generate

        Returns:
            List of generated Seed objects
        """
        existing_types = [s.type for s in self.seed_system.seeds.values()]

        suggestions = self.llm.suggest_seeds(
            interaction=interaction,
            count=max_seeds,
            existing_seed_types=existing_types or None
        )

        seeds = []
        for suggestion in suggestions:
            if suggestion.confidence < self.min_confidence:
                continue

            seed = self._create_seed_from_suggestion(suggestion)
            if seed:
                seeds.append(seed)

                if self.auto_plant:
                    self.plant_seed(seed)

        return seeds

    def _create_seed_from_suggestion(self, suggestion: SeedSuggestion) -> Optional[Seed]:
        """Create a Seed object from LLM suggestion."""
        type_mapping = {
            "wisdom": SeedType.WISDOM,
            "compassion": SeedType.COMPASSION,
            "belief": SeedType.BELIEF,
            "behavior": SeedType.BEHAVIOR
        }

        seed_type = type_mapping.get(suggestion.type.value, SeedType.WISDOM)

        seed = Seed(
            type=seed_type,
            content=suggestion.content,
            purity=suggestion.purity,
            source="llm_generated",
            metadata={
                "reasoning": suggestion.reasoning,
                "confidence": suggestion.confidence,
                "llm_model": self.llm.model
            }
        )

        return seed

    def plant_seed(self, seed: Seed) -> bool:
        """
        Plant a seed in both in-memory and persistent storage.

        Args:
            seed: Seed to plant

        Returns:
            True if successfully planted in at least one store
        """
        self.seed_system.seeds[seed.id] = seed

        if self.alaya_store:
            return self.alaya_store.plant_seed(seed)

        return True

    def analyze_existing_seed(
        self,
        seed: Seed,
        context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Re-analyze an existing seed using LLM.

        Args:
            seed: Seed to analyze
            context: Optional additional context

        Returns:
            Dictionary with analysis results
        """
        suggestion = self.llm.analyze_seed(seed.content, context)

        return {
            "original_purity": seed.purity,
            "suggested_purity": suggestion.purity,
            "reasoning": suggestion.reasoning,
            "confidence": suggestion.confidence,
            "should_update": abs(suggestion.purity - seed.purity) > 0.2
        }

    def generate_from_emergence(
        self,
        emergence_data: Dict[str, Any]
    ) -> List[SeedSuggestion]:
        """
        Generate seeds from an emergence event.

        Args:
            emergence_data: Dictionary containing emergence information

        Returns:
            List of seed suggestions based on emergence insight
        """
        insight = self.llm.extract_insight(emergence_data)

        suggestions = []

        if insight.wisdom_type:
            suggestions.append(SeedSuggestion(
                type=SeedType.WISDOM,
                content=f"Understanding of {insight.wisdom_type}",
                purity=0.85,
                reasoning=f"Derived from emergence: {insight.summary}",
                confidence=0.8
            ))

        for aspect in insight.compassion_aspects[:2]:
            suggestions.append(SeedSuggestion(
                type=SeedType.COMPASSION,
                content=aspect[:100],
                purity=0.8,
                reasoning=f"Compassion aspect from emergence: {insight.summary}",
                confidence=0.75
            ))

        return suggestions

    def get_stats(self) -> Dict[str, Any]:
        """Get generation statistics."""
        stats = self.seed_system.get_statistics()
        stats["llm_model"] = self.llm.model
        stats["auto_plant"] = self.auto_plant
        stats["min_confidence"] = self.min_confidence

        llm_generated = sum(
            1 for s in self.seed_system.seeds.values()
            if s.source == "llm_generated"
        )
        stats["llm_generated_count"] = llm_generated

        return stats
