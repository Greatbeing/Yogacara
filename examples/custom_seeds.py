"""
Custom Seeds Example for Yogacara Framework

This example demonstrates how to create and use custom seeds
with metadata and advanced features.

Run with: python examples/custom_seeds.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import json
from datetime import datetime
from core import (
    SeedSystem,
    SeedType,
    Seed,
    AlayaStore,
)


def main():
    """Main demonstration of custom seed features."""
    
    print("=" * 60)
    print("Yogacara Framework - Custom Seeds Example")
    print("=" * 60)
    print()
    
    # Initialize
    seed_system = SeedSystem()
    store = AlayaStore("custom_seeds.db")
    
    # Example 1: Seeds with rich metadata
    print("1. Creating seeds with rich metadata...")
    print()
    
    wisdom_seed = Seed(
        type=SeedType.WISDOM,
        content="Understanding the selflessness of all phenomena",
        purity=0.95,
        weight=0.8,
        source="meditation",
        metadata={
            "practice": "vipassana",
            "duration_minutes": 45,
            "insight_type": "emptiness",
            "difficulty": "advanced",
            "tags": ["meditation", "insight", "emptiness"],
        },
    )
    
    compassion_seed = Seed(
        type=SeedType.COMPASSION,
        content="May all beings be free from suffering",
        purity=0.92,
        weight=0.85,
        source="practice",
        metadata={
            "practice": "metta_bhavana",
            "target": "all_beings",
            "language": "pali",
            "recitation_count": 108,
            "tags": ["compassion", "loving-kindness", "recitation"],
        },
    )
    
    belief_seed = Seed(
        type=SeedType.BELIEF,
        content="The path of awakening is available to all",
        purity=0.88,
        weight=0.7,
        source="teaching",
        metadata={
            "source_text": "Dhammapada",
            "verse": 174,
            "interpretation": "universalist",
            "tags": ["faith", "path", "potential"],
        },
    )
    
    behavior_seed = Seed(
        type=SeedType.BEHAVIOR,
        content="Pause and breathe before responding to challenges",
        purity=0.9,
        weight=0.75,
        source="habit_formation",
        metadata={
            "trigger": "stressful_situation",
            "response": "mindful_pause",
            "success_rate": 0.75,
            "streak_days": 14,
            "tags": ["mindfulness", "response_prevention", "habit"],
        },
    )
    
    # Plant all seeds
    for seed in [wisdom_seed, compassion_seed, belief_seed, behavior_seed]:
        seed_system.seeds[seed.id] = seed
        store.plant_seed(seed)
        print(f"   ✓ Planted {seed.type.value} seed: {seed.id}")
        print(f"     Content: {seed.content[:50]}...")
        print(f"     Purity: {seed.purity}, Weight: {seed.weight}")
        print(f"     Source: {seed.source}")
        print(f"     Metadata keys: {list(seed.metadata.keys())}")
        print()
    
    # Example 2: Seed activation and vasana
    print("2. Seed activation and habit energy (vasana)...")
    print()
    
    print(f"   Initial vasana for wisdom seed: {wisdom_seed.vasana}")
    
    for i in range(5):
        wisdom_seed.activate()
        wisdom_seed.boost_purity(0.01)  # Each activation slightly improves purity
    
    print(f"   After 5 activations: {wisdom_seed.vasana}")
    print(f"   Purity increased to: {wisdom_seed.purity:.2f}")
    print()
    
    # Example 3: Serialization and deserialization
    print("3. Serialization and deserialization...")
    print()
    
    # Serialize to JSON
    seed_dict = wisdom_seed.to_dict()
    print("   Serialized seed:")
    print(f"   {json.dumps(seed_dict, indent=4, default=str)[:300]}...")
    print()
    
    # Deserialize
    restored_seed = Seed.from_dict(seed_dict)
    print(f"   Restored seed ID: {restored_seed.id}")
    print(f"   Restored seed type: {restored_seed.type}")
    print(f"   Restored purity: {restored_seed.purity}")
    print(f"   Restored metadata: {restored_seed.metadata}")
    print()
    
    # Example 4: Filtering seeds
    print("4. Filtering seeds...")
    print()
    
    # Add more seeds for filtering demo
    for i in range(3):
        seed = seed_system.create_seed(
            type=SeedType.BEHAVIOR,
            content=f"Behavior pattern {i}",
            purity=0.6 + i * 0.1,
            source="learning",
        )
        if seed:
            store.plant_seed(seed)
    
    # Filter by type
    print("   Seeds by type:")
    for seed_type in SeedType:
        seeds = seed_system.get_seeds_by_type(seed_type)
        print(f"     {seed_type.value}: {len(seeds)}")
    print()
    
    # Filter by source
    print("   Seeds by source:")
    sources = {}
    for seed in seed_system.seeds.values():
        sources[seed.source] = sources.get(seed.source, 0) + 1
    for source, count in sources.items():
        print(f"     {source}: {count}")
    print()
    
    # High purity seeds
    print("   High purity seeds (≥0.8):")
    high_purity = seed_system.get_high_purity_seeds(threshold=0.8)
    for seed in high_purity:
        print(f"     - [{seed.type.value}] {seed.content[:40]}... (purity: {seed.purity})")
    print()
    
    # Example 5: Statistics
    print("5. System statistics...")
    print()
    
    stats = seed_system.get_statistics()
    print(f"   Total seeds: {stats['total']}")
    print(f"   Average purity: {stats['avg_purity']:.2f}")
    print(f"   Average vasana: {stats['avg_vasana']:.1f}")
    print()
    
    # Example 6: Seed decay
    print("6. Seed decay over time...")
    print()
    
    seed = seed_system.seeds[list(seed_system.seeds.keys())[0]]
    original_purity = seed.purity
    print(f"   Original purity: {original_purity:.2f}")
    
    seed.decay_purity(0.05)
    print(f"   After decay: {seed.purity:.2f}")
    
    # Decay all seeds
    decayed = seed_system.decay_all_seeds(days=1)
    print(f"   Seeds decayed (below threshold): {decayed}")
    print()
    
    # Example 7: Custom seed system configuration
    print("7. Custom Seed System configuration...")
    print()
    
    # Create custom system with different thresholds
    custom_system = SeedSystem()
    custom_system.PURITY_THRESHOLD = 0.5  # Stricter threshold
    custom_system.WEIGHT_DECAY_RATE = 0.02  # Faster decay
    
    print(f"   Custom purity threshold: {custom_system.PURITY_THRESHOLD}")
    print(f"   Custom decay rate: {custom_system.WEIGHT_DECAY_RATE}")
    
    # Create seed that would fail with stricter threshold
    low_seed = custom_system.create_seed(
        type=SeedType.BEHAVIOR,
        content="Low quality behavior",
        purity=0.4,  # Below 0.5 threshold
    )
    
    if low_seed is None:
        print("   ✓ Low quality seed rejected (as expected)")
    else:
        print("   ✗ Low quality seed accepted (unexpected)")
    
    high_seed = custom_system.create_seed(
        type=SeedType.WISDOM,
        content="High quality wisdom",
        purity=0.9,
    )
    
    if high_seed:
        print("   ✓ High quality seed accepted")
    print()
    
    print("=" * 60)
    print("Custom seeds example completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
