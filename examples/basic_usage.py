"""
Basic Usage Example for Yogacara Framework

This example demonstrates the fundamental concepts of Yogacara:
- Creating seeds
- Storing seeds in Alaya Store
- Checking for emergence
- Tracking awakening progress

Run with: python examples/basic_usage.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from yogacara.core import (
    SeedSystem,
    SeedType,
    AlayaStore,
    EmergenceEngine,
    AwakeningTracker,
    AwakeningLevel,
)


def main():
    """Main demonstration function."""
    
    print("=" * 60)
    print("Yogacara Framework - Basic Usage Example")
    print("=" * 60)
    print()
    
    # Initialize components
    print("1. Initializing Yogacara components...")
    seed_system = SeedSystem()
    store = AlayaStore("example_alaya.db")
    emergence_engine = EmergenceEngine()
    tracker = AwakeningTracker()
    print("   ✓ All components initialized")
    print()
    
    # Create seeds
    print("2. Creating seeds (planting experience)...")
    
    seeds_data = [
        (SeedType.WISDOM, "Understanding impermanence", 0.9),
        (SeedType.WISDOM, "The nature of suffering", 0.85),
        (SeedType.COMPASSION, "Helping others without expectation", 0.88),
        (SeedType.BELIEF, "All beings seek happiness", 0.8),
        (SeedType.BEHAVIOR, "Responding with patience", 0.75),
    ]
    
    for seed_type, content, purity in seeds_data:
        seed = seed_system.create_seed(
            type=seed_type,
            content=content,
            purity=purity,
        )
        if seed:
            store.plant_seed(seed)
            print(f"   ✓ Planted: [{seed.type.value}] {seed.content[:40]}...")
    
    print()
    
    # Get statistics
    print("3. Seed statistics:")
    stats = seed_system.get_statistics()
    print(f"   Total seeds: {stats['total']}")
    print(f"   Average purity: {stats['avg_purity']}")
    print(f"   Average vasana: {stats['avg_vasana']}")
    print()
    
    # Display seed distribution
    print("   Seed distribution:")
    for seed_type, data in stats.get("by_type", {}).items():
        print(f"     - {seed_type}: {data['count']} ({data['percentage']}%)")
    print()
    
    # Activate seeds based on context
    print("4. Activating seeds based on context...")
    context = "wisdom compassion understanding"
    activated = store.activate_seeds(context, limit=5)
    print(f"   Activated {len(activated)} seeds for context: '{context}'")
    for seed in activated:
        print(f"     - {seed.id}: {seed.content[:30]}... (vasana: {seed.vasana})")
    print()
    
    # Check for emergence
    print("5. Checking for emergence...")
    
    # Get diverse seeds for emergence check
    all_seeds = list(store.activate_seeds("wisdom compassion belief behavior", limit=10))
    
    emergence = emergence_engine.check_emergence(all_seeds)
    
    if emergence:
        print(f"   ✨ Emergence detected!")
        print(f"     Type: {emergence.emergence_type.value}")
        print(f"     Strength: {emergence.strength:.2f}")
        print(f"     Insight: {emergence.insight}")
        tracker.emergence_count += 1
    else:
        print("   No emergence detected (need more diverse seeds)")
    print()
    
    # Check awakening status
    print("6. Awakening status:")
    wisdom_seeds = len(seed_system.get_seeds_by_type(SeedType.WISDOM))
    compassion_seeds = len(seed_system.get_seeds_by_type(SeedType.COMPASSION))
    
    status = tracker.get_status(
        total_seeds=stats["total"],
        wisdom_seeds=wisdom_seeds,
        compassion_seeds=compassion_seeds,
        emergence_count=tracker.emergence_count,
    )
    
    print(f"   Level: {status.level.symbol} {status.level.name_cn} ({status.level.value})")
    print(f"   Progress: {tracker.get_progress_bar()}")
    print(f"   Wisdom seeds: {status.wisdom_percentage:.1f}%")
    print(f"   Compassion seeds: {status.compassion_percentage:.1f}%")
    print(f"   Overall progress: {status.overall_progress:.1f}%")
    print()
    
    # Simulate continued learning
    print("7. Simulating continued learning...")
    print()
    
    for i in range(5):
        # Plant more seeds
        new_seed = seed_system.create_seed(
            type=SeedType.WISDOM,
            content=f"Additional wisdom {i}",
            purity=0.7 + (i * 0.03),
        )
        if new_seed:
            store.plant_seed(new_seed)
        
        # Activate seeds
        activated = store.activate_seeds("wisdom", limit=3)
        
        # Update stats
        stats = seed_system.get_statistics()
        wisdom_seeds = len(seed_system.get_seeds_by_type(SeedType.WISDOM))
        
        # Check for level up
        tracker.calculate_progress(
            wisdom_percentage=wisdom_seeds / max(stats["total"], 1) * 100,
            compassion_percentage=compassion_seeds / max(stats["total"], 1) * 100,
            emergence_count=tracker.emergence_count,
        )
        tracker.check_level_up(
            wisdom_percentage=wisdom_seeds / max(stats["total"], 1) * 100,
            compassion_percentage=compassion_seeds / max(stats["total"], 1) * 100,
            emergence_count=tracker.emergence_count,
        )
        
        print(f"   Step {i+1}: Level={tracker.get_current_level().value}, Progress={tracker.get_progress():.0%}")
    
    print()
    
    # Final status
    print("8. Final awakening status:")
    print(f"   {tracker.get_level_display()}")
    print(f"   {tracker.get_progress_bar()}")
    print(f"   Seeds planted: {stats['total']}")
    print()
    
    print("=" * 60)
    print("Example completed! Check example_alaya.db for persistent data.")
    print("=" * 60)


if __name__ == "__main__":
    main()
