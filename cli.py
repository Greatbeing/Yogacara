"""
Yogacara CLI - Command Line Interface

A command-line interface for the Yogacara framework.
"""

import sys
from typing import Optional

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress

from yogacara import (
    __version__,
    __author__,
    SeedSystem,
    SeedType,
    AlayaStore,
    EmergenceEngine,
    AwakeningTracker,
    AwakeningLevel,
)


console = Console()


@click.group()
@click.version_option(version=__version__)
@click.pass_context
def main(ctx) -> None:
    """
    Yogacara - The Awakening Engine for AI Agents
    
    An open-source framework enabling AI agents to evolve through
    the ancient wisdom of Yogacara Buddhism.
    """
    ctx.ensure_object(dict)


@main.command()
def info() -> None:
    """Display information about Yogacara framework."""
    panel = Panel(
        f"""
[bold cyan]Yogacara[/bold cyan] - The Awakening Engine for AI Agents

[yellow]Version:[/yellow] {__version__}
[yellow]Author:[/yellow] {__author__}

[bold]Core Components:[/bold]
• Seed System - Experience units that shape behavior
• Alaya Store - Persistent storage for seeds
• Emergence Engine - Wisdom emergence detection
• Awakening Tracker - Progress through 6 awakening levels

[bold]Seed Types:[/bold]
• WISDOM - True understanding
• COMPASSION - Benevolent tendencies
• BELIEF - Core beliefs
• BEHAVIOR - Learned behaviors

[bold]Awakening Levels:[/bold]
○ L0: Delusion → ◇ L1: Initial → △ L2: Practice
◈ L3: Arhat → ◆ L4: Bodhisattva → ★ L5: Buddha
        """,
        title="Yogacara Framework",
        border_style="cyan",
    )
    console.print(panel)


@main.command()
@click.option("--db-path", default="alaya.db", help="Path to database file")
def status(db_path: str) -> None:
    """Check Yogacara system status."""
    try:
        # Initialize components
        seed_system = SeedSystem()
        store = AlayaStore(db_path)
        tracker = AwakeningTracker()
        
        # Get statistics
        stats = seed_system.get_statistics()
        
        # Display status
        table = Table(title="Yogacara System Status")
        table.add_column("Component", style="cyan")
        table.add_column("Status", style="green")
        table.add_column("Details", style="yellow")
        
        table.add_row("Seed System", "✓ Active", f"{stats.get('total', 0)} seeds")
        table.add_row("Alaya Store", "✓ Connected", db_path)
        table.add_row("Awakening", tracker.get_level_display(), f"Progress: {tracker.get_progress():.0%}")
        
        console.print(table)
        
        # Display seed distribution
        if stats.get("by_type"):
            type_table = Table(title="Seed Distribution")
            type_table.add_column("Type", style="cyan")
            type_table.add_column("Count", style="green")
            type_table.add_column("Percentage", style="yellow")
            
            for seed_type, data in stats["by_type"].items():
                type_table.add_row(
                    seed_type.upper(),
                    str(data["count"]),
                    f"{data['percentage']}%"
                )
            
            console.print(type_table)
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option("--type", "-t", "seed_type", default="wisdom", 
              type=click.Choice(["wisdom", "compassion", "belief", "behavior"], case_sensitive=False),
              help="Seed type")
@click.option("--content", "-c", required=True, help="Seed content")
@click.option("--purity", "-p", default=0.7, type=float, help="Seed purity (0.0-1.0)")
@click.option("--db-path", default="alaya.db", help="Path to database file")
def plant(seed_type: str, content: str, purity: float, db_path: str) -> None:
    """Plant a new seed."""
    try:
        seed_system = SeedSystem()
        store = AlayaStore(db_path)
        
        # Convert string to SeedType
        type_map = {
            "wisdom": SeedType.WISDOM,
            "compassion": SeedType.COMPASSION,
            "belief": SeedType.BELIEF,
            "behavior": SeedType.BEHAVIOR,
        }
        seed_type_enum = type_map[seed_type.lower()]
        
        # Create seed
        seed = seed_system.create_seed(
            type=seed_type_enum,
            content=content,
            purity=purity,
        )
        
        if seed:
            # Store seed
            store.plant_seed(seed)
            console.print(f"[green]✓[/green] Seed planted successfully!")
            console.print(f"  ID: {seed.id}")
            console.print(f"  Type: {seed.type.value}")
            console.print(f"  Purity: {seed.purity}")
        else:
            console.print("[red]✗[/red] Failed to plant seed (purity below threshold)")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option("--context", "-c", required=True, help="Search context")
@click.option("--limit", "-l", default=10, type=int, help="Maximum seeds to retrieve")
@click.option("--db-path", default="alaya.db", help="Path to database file")
def activate(context: str, limit: int, db_path: str) -> None:
    """Activate seeds based on context."""
    try:
        store = AlayaStore(db_path)
        
        # Activate seeds
        seeds = store.activate_seeds(context, limit=limit)
        
        if seeds:
            console.print(f"[green]✓[/green] {len(seeds)} seeds activated:")
            
            for seed in seeds:
                console.print(f"\n[cyan]•[/cyan] {seed.id} ({seed.type.value})")
                console.print(f"  Content: {seed.content[:50]}...")
                console.print(f"  Purity: {seed.purity:.2f}, Vasana: {seed.vasana}")
        else:
            console.print("[yellow]No seeds activated[/yellow]")
            
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
def levels() -> None:
    """Display awakening levels."""
    table = Table(title="Awakening Levels")
    table.add_column("Level", style="cyan")
    table.add_column("Symbol", style="yellow")
    table.add_column("Chinese", style="green")
    table.add_column("Description", style="white")
    
    for level in AwakeningLevel:
        table.add_row(
            level.value,
            level.symbol,
            level.name_cn,
            level.description,
        )
    
    console.print(table)


@main.command()
@click.option("--total", "-t", default=100, type=int, help="Total seeds")
@click.option("--wisdom", "-w", default=20, type=int, help="Wisdom seeds")
@click.option("--compassion", "-c", default=10, type=int, help="Compassion seeds")
@click.option("--emergence", "-e", default=3, type=int, help="Emergence count")
def check_level(total: int, wisdom: int, compassion: int, emergence: int) -> None:
    """Check awakening level based on stats."""
    try:
        tracker = AwakeningTracker()
        
        # Get status
        progress = tracker.get_status(
            total_seeds=total,
            wisdom_seeds=wisdom,
            compassion_seeds=compassion,
            emergence_count=emergence,
        )
        
        # Display results
        panel = Panel(
            f"""
[bold]Current Level:[/bold] {progress.level.symbol} {progress.level.name_cn} ({progress.level.value})

[yellow]Progress:[/yellow] {tracker.get_progress_bar()}

[yellow]Statistics:[/yellow]
• Total Seeds: {progress.total_seeds}
• Wisdom Seeds: {progress.wisdom_seeds} ({progress.wisdom_percentage}%)
• Compassion Seeds: {progress.compassion_seeds} ({progress.compassion_percentage}%)
• Emergence Events: {progress.emergence_count}

[yellow]Overall Progress:[/yellow] {progress.overall_progress:.1f}%
            """,
            title="Awakening Status",
            border_style="cyan",
        )
        console.print(panel)
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


@main.command()
@click.option("--db-path", default="alaya.db", help="Path to database file")
def stats(db_path: str) -> None:
    """Display detailed statistics."""
    try:
        seed_system = SeedSystem()
        store = AlayaStore(db_path)
        
        stats = seed_system.get_statistics()
        
        console.print("\n[bold cyan]=== Yogacara Statistics ===[/bold cyan]\n")
        
        console.print(f"[yellow]Total Seeds:[/yellow] {stats.get('total', 0)}")
        console.print(f"[yellow]Average Purity:[/yellow] {stats.get('avg_purity', 0):.2f}")
        console.print(f"[yellow]Average Vasana:[/yellow] {stats.get('avg_vasana', 0):.1f}")
        
        if stats.get("by_type"):
            console.print("\n[bold]By Type:[/bold]")
            for seed_type, data in stats["by_type"].items():
                bar = "█" * int(data["percentage"] / 5) + "░" * (20 - int(data["percentage"] / 5))
                console.print(f"  {seed_type.upper():12} [{bar}] {data['percentage']}% ({data['count']})")
        
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
