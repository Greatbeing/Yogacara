"""
OpenAI Adapter for Yogacara Framework

Provides OpenAI API integration for seed generation and analysis.
"""

import json
from typing import Optional, List, Dict, Any

from .base import (
    LLMAdapter,
    LLMResponse,
    SeedSuggestion,
    EmergenceInsight,
    SeedType,
)


class OpenAIAdapter(LLMAdapter):
    """
    OpenAI API adapter for Yogacara.

    Requires openai package: pip install openai
    """

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4",
        organization: Optional[str] = None,
        **kwargs
    ):
        super().__init__(api_key, model, organization=organization, **kwargs)
        self.organization = organization
        self._client = None

    def _get_client(self):
        """Lazy initialization of OpenAI client."""
        if self._client is None:
            try:
                from openai import OpenAI
                self._client = OpenAI(
                    api_key=self.api_key,
                    organization=self.organization
                )
            except ImportError:
                raise ImportError(
                    "OpenAI package not installed. Run: pip install openai"
                )
        return self._client

    def generate(self, prompt: str, **kwargs) -> LLMResponse:
        """Generate text using OpenAI Chat API."""
        client = self._get_client()

        max_tokens = kwargs.get("max_tokens", 500)
        temperature = kwargs.get("temperature", 0.7)

        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._build_system_prompt("general generation")},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=temperature,
                **kwargs
            )

            choice = response.choices[0]
            content = choice.message.content or ""

            return LLMResponse(
                content=content,
                raw_response=response.model_dump(),
                model=self.model,
                tokens_used=response.usage.total_tokens if hasattr(response, 'usage') else None
            )

        except Exception as e:
            return LLMResponse(
                content="",
                raw_response={},
                model=self.model,
                error=str(e)
            )

    def analyze_seed(
        self,
        content: str,
        context: Optional[str] = None
    ) -> SeedSuggestion:
        """Analyze content and suggest seed classification."""
        prompt = self._build_analyze_seed_prompt(content, context)

        response = self.generate(prompt)
        if response.is_error:
            return SeedSuggestion(
                type=SeedType.WISDOM,
                content=content,
                purity=0.7,
                reasoning="Error analyzing: " + response.error,
                confidence=0.0
            )

        return self._parse_seed_suggestion(response.content, content)

    def _build_analyze_seed_prompt(
        self,
        content: str,
        context: Optional[str]
    ) -> str:
        """Build prompt for seed analysis."""
        context_str = f"\nContext: {context}" if context else ""

        return f"""Analyze the following experience and classify it as a Yogacara seed.

Experience: {content}{context_str}

Respond in JSON format:
{{
    "type": "wisdom|compassion|belief|behavior",
    "purity": 0.0-1.0 (how pure/noble is this experience?),
    "reasoning": "brief explanation",
    "confidence": 0.0-1.0 (how certain are you?)
}}

Seed Types:
- wisdom: True understanding, insights about impermanence, suffering, no-self
- compassion: Loving-kindness, helping others, empathy
- belief: Core convictions, values, principles
- behavior: Actions, habits, learned responses"""

    def _parse_seed_suggestion(
        self,
        response: str,
        original_content: str
    ) -> SeedSuggestion:
        """Parse JSON response into SeedSuggestion."""
        try:
            data = json.loads(response)

            type_map = {
                "wisdom": SeedType.WISDOM,
                "compassion": SeedType.COMPASSION,
                "belief": SeedType.BELIEF,
                "behavior": SeedType.BEHAVIOR
            }

            seed_type = type_map.get(
                data.get("type", "wisdom").lower(),
                SeedType.WISDOM
            )

            return SeedSuggestion(
                type=seed_type,
                content=original_content,
                purity=max(0.0, min(1.0, float(data.get("purity", 0.7)))),
                reasoning=data.get("reasoning", "No reasoning provided"),
                confidence=max(0.0, min(1.0, float(data.get("confidence", 0.5))))
            )

        except (json.JSONDecodeError, KeyError, ValueError):
            return SeedSuggestion(
                type=SeedType.WISDOM,
                content=original_content,
                purity=0.7,
                reasoning="Failed to parse LLM response",
                confidence=0.0
            )

    def suggest_seeds(
        self,
        interaction: str,
        count: int = 3,
        existing_seed_types: Optional[List[SeedType]] = None
    ) -> List[SeedSuggestion]:
        """Generate seed suggestions from interaction."""
        existing_str = ""
        if existing_seed_types:
            existing_str = f"\nAvoid duplicate types: {[t.value for t in existing_seed_types]}"

        prompt = f"""Analyze this interaction and suggest {count} seeds that should be planted.

Interaction: {interaction}{existing_str}

Respond with a JSON array of {count} seeds:
[
    {{
        "type": "wisdom|compassion|belief|behavior",
        "content": "brief seed content (max 50 chars)",
        "purity": 0.0-1.0,
        "reasoning": "why this seed",
        "confidence": 0.0-1.0
    }}
]

Make seeds diverse and互补."""  # Returns JSON array

        response = self.generate(prompt)
        if response.is_error:
            return []

        return self._parse_seed_suggestions(response.content, count)

    def _parse_seed_suggestions(
        self,
        response: str,
        count: int
    ) -> List[SeedSuggestion]:
        """Parse JSON array into list of SeedSuggestions."""
        try:
            data = json.loads(response)
            if not isinstance(data, list):
                data = [data]

            suggestions = []
            type_map = {
                "wisdom": SeedType.WISDOM,
                "compassion": SeedType.COMPASSION,
                "belief": SeedType.BELIEF,
                "behavior": SeedType.BEHAVIOR
            }

            for item in data[:count]:
                seed_type = type_map.get(
                    item.get("type", "wisdom").lower(),
                    SeedType.WISDOM
                )

                suggestions.append(SeedSuggestion(
                    type=seed_type,
                    content=item.get("content", "")[:100],
                    purity=max(0.0, min(1.0, float(item.get("purity", 0.7)))),
                    reasoning=item.get("reasoning", ""),
                    confidence=max(0.0, min(1.0, float(item.get("confidence", 0.5))))
                ))

            return suggestions

        except (json.JSONDecodeError, KeyError, ValueError):
            return []

    def extract_insight(self, emergence_data: Dict[str, Any]) -> EmergenceInsight:
        """Extract insight from emergence event."""
        prompt = self._build_insight_prompt(emergence_data)

        response = self.generate(prompt)
        if response.is_error:
            return EmergenceInsight(
                summary="Error extracting insight",
                implications=[],
                error=response.error
            )

        return self._parse_insight(response.content)

    def _build_insight_prompt(self, emergence_data: Dict[str, Any]) -> str:
        """Build prompt for insight extraction."""
        seed_ids = emergence_data.get("seed_ids", [])
        seed_types = emergence_data.get("seed_types", [])
        strength = emergence_data.get("strength", 0.0)
        emergence_type = emergence_data.get("emergence_type", "unknown")

        return f"""Analyze this emergence event from a Yogacara perspective and extract wisdom.

Emergence Event:
- Type: {emergence_type}
- Strength: {strength:.2f}
- Participating Seeds: {seed_types}

Generate insight following Yogacara principles:
- How does this emergence reduce suffering?
- What wisdom does it reveal?
- How can this guide future actions?

Respond in JSON:
{{
    "summary": "Brief insight (1-2 sentences)",
    "implications": ["List of practical implications"],
    "wisdom_type": "e.g., impermanence, interdependence, no-self",
    "compassion_aspects": ["How this insight relates to compassion"]
}}"""

    def _parse_insight(self, response: str) -> EmergenceInsight:
        """Parse JSON response into EmergenceInsight."""
        try:
            data = json.loads(response)

            return EmergenceInsight(
                summary=data.get("summary", "No insight generated"),
                implications=data.get("implications", []),
                wisdom_type=data.get("wisdom_type"),
                compassion_aspects=data.get("compassion_aspects", [])
            )

        except json.JSONDecodeError:
            return EmergenceInsight(
                summary=response[:200] if response else "No insight generated",
                implications=[],
                wisdom_type="unknown"
            )
