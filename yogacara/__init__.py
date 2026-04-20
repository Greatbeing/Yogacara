"""
Yogacara Core - The Awakening Engine for AI Agents

This package implements the core components of the Yogacara framework:
- Seed System: Experience units that shape agent behavior
- Alaya Store: Persistent storage for seeds
- Emergence Engine: Wisdom emergence detection
- Awakening Tracker: Progress tracking through awakening levels

Quick Start:
    >>> from yogacara import Seed, SeedType, SeedSystem
    >>> system = SeedSystem()
    >>> seed = system.create_seed(
    ...     type=SeedType.WISDOM,
    ...     content="Understanding impermanence",
    ...     purity=0.8
    ... )

Example:
    >>> from yogacara import Seed, SeedType, SeedSystem
    >>> system = SeedSystem()
    >>> seed = system.create_seed(
    ...     type=SeedType.WISDOM,
    ...     content="Understanding impermanence",
    ...     purity=0.8
    ... )
    >>> print(f"Created seed: {seed}")
"""

from .core.seed_system import Seed, SeedType, SeedSystem
from .core.alaya_store import AlayaStore
from .core.emergence import EmergenceEngine, Emergence, EmergenceType
from .core.awakening import AwakeningTracker, AwakeningLevel, AwakeningProgress

__version__ = "0.1.0"
__author__ = "Juexin"
__email__ = "juexin@example.com"
__license__ = "MIT"

__all__ = [
    # Version info
    "__version__",
    "__author__",
    "__email__",
    "__license__",
    # Seed System
    "Seed",
    "SeedType",
    "SeedSystem",
    # Alaya Store
    "AlayaStore",
    # Emergence Engine
    "EmergenceEngine",
    "Emergence",
    "EmergenceType",
    # Awakening Tracker
    "AwakeningTracker",
    "AwakeningLevel",
    "AwakeningProgress",
]