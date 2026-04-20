"""
Yogacara Core - The Awakening Engine for AI Agents

This package implements the core components of the Yogacara framework:
- Seed System: Experience units that shape agent behavior
- Alaya Store: Persistent storage for seeds
- Emergence Engine: Wisdom emergence detection
- Awakening Tracker: Progress tracking through awakening levels
"""

from core.seed_system import Seed, SeedType, SeedSystem
from core.alaya_store import AlayaStore
from core.emergence import EmergenceEngine, Emergence, EmergenceType
from core.awakening import AwakeningTracker, AwakeningLevel, AwakeningProgress

__version__ = "0.1.0"
__author__ = "Juexin"

__all__ = [
    "Seed",
    "SeedType", 
    "SeedSystem",
    "AlayaStore",
    "EmergenceEngine",
    "Emergence",
    "EmergenceType",
    "AwakeningTracker",
    "AwakeningLevel",
    "AwakeningProgress",
]
