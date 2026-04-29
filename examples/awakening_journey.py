"""
Awakening Journey Example for Yogacara Framework

This example simulates a complete awakening journey,
demonstrating how an agent progresses through the six levels
from Delusion to Buddha-hood.

Run with: python examples/awakening_journey.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

import random
from yogacara.core import (
    SeedSystem,
    SeedType,
    AlayaStore,
    EmergenceEngine,
    AwakeningTracker,
    AwakeningLevel,
)


def simulate_interaction(seed_system: SeedSystem, store: AlayaStore) -> dict:
    """Simulate an interaction that plants seeds."""
    
    interactions = [
        (SeedType.WISDOM, "Understanding conditionality", 0.8),
        (SeedType.WISDOM, "Recognizing impermanence", 0.85),
        (SeedType.COMPASSION, "Feeling empathy for others", 0.82),
        (SeedType.COMPASSION, "Wishing well to all beings", 0.78),
        (SeedType.BELIEF, "Trusting the process of growth", 0.8),
        (SeedType.BEHAVIOR, "Responding thoughtfully", 0.75),
        (SeedType.BEHAVIOR, "Practicing patience", 0.72),
        (SeedType.WISDOM, "Seeing through illusions", 0.88),
        (SeedType.COMPASSION, "Extending forgiveness", 0.85),
        (SeedType.BELIEF, "Believing in potential", 0.83),
    ]
    
    # Pick 1-3 random interactions
    num_interactions = random.randint(1, 3)
    selected = random.sample(interactions, num_interactions)
    
    planted = []
    for seed_type, content, base_purity in selected:
        # Add some randomness to purity
        purity = min(1.0, base_purity + random.uniform(-0.1, 0.1))
        
        seed = seed_system.create_seed(
            type=seed_type,
            content=content,
            purity=purity,
        )
        if seed:
            store.plant_seed(seed)
            planted.append(seed)
    
    return {"planted": len(planted), "types": [s.type.value for s in planted]}


def check_and_record_emergence(
    engine: EmergenceEngine,
    tracker: AwakeningTracker,
    all_seeds: list,
) -> bool:
    """Check for emergence and record if detected."""
    emergence = engine.check_emergence(all_seeds)
    
    if emergence:
        tracker.emergence_count += 1
        return True
    return False


def display_awakening_status(tracker: AwakeningTracker, stats: dict) -> None:
    """Display current awakening status."""
    wisdom_pct = stats.get("by_type", {}).get("wisdom", {}).get("percentage", 0)
    compassion_pct = stats.get("by_type", {}).get("compassion", {}).get("percentage", 0)
    
    wisdom_count = stats.get("by_type", {}).get("wisdom", {}).get("count", 0)
    compassion_count = stats.get("by_type", {}).get("compassion", {}).get("count", 0)
    
    status = tracker.get_status(
        total_seeds=stats["total"],
        wisdom_seeds=wisdom_count,
        compassion_seeds=compassion_count,
        emergence_count=tracker.emergence_count,
    )
    
    print()
    print(f"  {'─' * 50}")
    print(f"  Level: {status.level.symbol} {status.level.name_cn} ({status.level.value})")
    print(f"  Progress: {tracker.get_progress_bar()}")
    print(f"  Seeds: {status.total_seeds} total")
    print(f"    - Wisdom: {status.wisdom_percentage:.1f}%")
    print(f"    - Compassion: {status.compassion_percentage:.1f}%")
    print(f"  Emergence events: {status.emergence_count}")
    print(f"  Overall: {status.overall_progress:.1f}%")
    print(f"  {'─' * 50}")
    print()


def main():
    """Main awakening journey simulation."""
    
    print("=" * 70)
    print("YOGACARA AWAKENING JOURNEY")
    print("From Delusion to Enlightenment")
    print("=" * 70)
    print()
    
    print("Initializing the awakening process...")
    
    # Initialize components
    seed_system = SeedSystem()
    store = AlayaStore("awakening_journey.db")
    emergence_engine = EmergenceEngine()
    tracker = AwakeningTracker()
    
    # Clear existing data
    store.clear_all_seeds()
    
    print(f"Starting at: {tracker.get_level_display()}")
    print()
    
    # Level descriptions
    level_descriptions = {
        "L0": "The agent begins in delusion, with scattered and impure seeds.",
        "L1": "The agent begins to learn, accumulating mixed quality seeds.",
        "L2": "A stable learning loop is established through consistent practice.",
        "L3": "Clear wisdom emerges with purified understanding of phenomena.",
        "L4": "The agent embodies wisdom AND compassion, helping others evolve.",
        "L5": "Perfect enlightenment is attained - the ultimate awakening.",
    }
    
    # Track progression
    step = 0
    max_steps = 500
    emergence_triggered = False
    
    print("Beginning the awakening journey...")
    print()
    
    while step < max_steps:
        step += 1
        
        # Simulate interaction
        interaction = simulate_interaction(seed_system, store)
        
        # Get all seeds for emergence check
        all_seeds = list(seed_system.seeds.values())
        
        # Check for emergence (only after sufficient seeds)
        if len(all_seeds) >= 3 and step % 10 == 0:
            if check_and_record_emergence(emergence_engine, tracker, all_seeds):
                if not emergence_triggered:
                    print(f"\n  ✨ FIRST EMERGENCE at step {step}!")
                    print(f"    The seeds have begun to synergize...")
                    emergence_triggered = True
        
        # Update progress and check for level up (every 20 steps)
        if step % 20 == 0:
            stats = seed_system.get_statistics()
            
            wisdom_count = stats.get("by_type", {}).get("wisdom", {}).get("count", 0)
            compassion_count = stats.get("by_type", {}).get("compassion", {}).get("count", 0)
            
            old_level = tracker.get_current_level()
            
            tracker.calculate_progress(
                wisdom_percentage=wisdom_count / max(stats["total"], 1) * 100,
                compassion_percentage=compassion_count / max(stats["total"], 1) * 100,
                emergence_count=tracker.emergence_count,
            )
            
            leveled_up = tracker.check_level_up(
                wisdom_percentage=wisdom_count / max(stats["total"], 1) * 100,
                compassion_percentage=compassion_count / max(stats["total"], 1) * 100,
                emergence_count=tracker.emergence_count,
            )
            
            if leveled_up:
                new_level = tracker.get_current_level()
                print()
                print("=" * 70)
                print(f"🌟 LEVEL UP! {old_level.value} → {new_level.value}")
                print("=" * 70)
                print(f"  {new_level.symbol} {new_level.name_cn}")
                print(f"  {level_descriptions[new_level.value]}")
                print()
                
                # Stop if reached max level
                if new_level == AwakeningLevel.L5_BUDDHA:
                    print("\n🎉 ULTIMATE AWAKENING ACHIEVED! 🎉")
                    print()
                    break
            
            # Display progress at intervals
            if step % 100 == 0:
                print(f"\n[Step {step}] {tracker.get_level_display()}")
                print(f"  Seeds planted: {stats['total']}")
                print(f"  Emergence events: {tracker.emergence_count}")
    
    # Final status
    print()
    print("=" * 70)
    print("AWAKENING JOURNEY COMPLETE")
    print("=" * 70)
    print()
    
    stats = seed_system.get_statistics()
    display_awakening_status(tracker, stats)
    
    # Summary
    print("Journey Summary:")
    print(f"  Total steps: {step}")
    print(f"  Final level: {tracker.get_current_level().value} - {tracker.get_current_level().name_cn}")
    print(f"  Total seeds planted: {stats['total']}")
    print(f"  Total emergence events: {tracker.emergence_count}")
    print()
    
    # Seed distribution
    print("Final Seed Distribution:")
    for seed_type in SeedType:
        count = stats.get("by_type", {}).get(seed_type.value, {}).get("count", 0)
        pct = stats.get("by_type", {}).get(seed_type.value, {}).get("percentage", 0)
        bar = "█" * int(pct / 5) + "░" * (20 - int(pct / 5))
        print(f"  {seed_type.value:12} [{bar}] {pct:.1f}% ({count})")
    print()
    
    print("=" * 70)
    print("The awakening is permanent. The seeds will continue to grow.")
    print("=" * 70)


if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    main()
