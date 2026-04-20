"""
Yogacara Configuration Module

Provides configuration management for the Yogacara framework.
Supports loading from YAML, JSON, and environment variables.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Union
import json
import os
import yaml


@dataclass
class SeedSystemConfig:
    """Configuration for Seed System."""
    purity_threshold: float = 0.3
    weight_decay_rate: float = 0.01
    max_seeds: int = 10000


@dataclass
class AlayaStoreConfig:
    """Configuration for Alaya Store."""
    db_path: str = "alaya.db"
    auto_backup: bool = False
    backup_dir: str = "backups"
    fts_enabled: bool = True


@dataclass
class EmergenceConfig:
    """Configuration for Emergence Engine."""
    min_seeds: int = 3
    synergy_threshold: float = 0.6
    strength_threshold: float = 0.7
    emergence_cooldown: int = 10  # steps between emergence checks


@dataclass
class AwakeningConfig:
    """Configuration for Awakening Tracker."""
    level_up_cooldown: int = 100  # steps between level ups
    progress_decay: float = 0.001


@dataclass
class YogacaraConfig:
    """
    Main configuration class for Yogacara framework.
    
    All components can be configured individually or loaded from file.
    """
    seed_system: SeedSystemConfig = field(default_factory=SeedSystemConfig)
    alaya_store: AlayaStoreConfig = field(default_factory=AlayaStoreConfig)
    emergence: EmergenceConfig = field(default_factory=EmergenceConfig)
    awakening: AwakeningConfig = field(default_factory=AwakeningConfig)
    
    # Logging configuration
    log_level: str = "INFO"
    log_file: Optional[str] = None
    log_dir: Optional[str] = None
    
    # General settings
    version: str = "0.1.0"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "seed_system": {
                "purity_threshold": self.seed_system.purity_threshold,
                "weight_decay_rate": self.seed_system.weight_decay_rate,
                "max_seeds": self.seed_system.max_seeds,
            },
            "alaya_store": {
                "db_path": self.alaya_store.db_path,
                "auto_backup": self.alaya_store.auto_backup,
                "backup_dir": self.alaya_store.backup_dir,
                "fts_enabled": self.alaya_store.fts_enabled,
            },
            "emergence": {
                "min_seeds": self.emergence.min_seeds,
                "synergy_threshold": self.emergence.synergy_threshold,
                "strength_threshold": self.emergence.strength_threshold,
                "emergence_cooldown": self.emergence.emergence_cooldown,
            },
            "awakening": {
                "level_up_cooldown": self.awakening.level_up_cooldown,
                "progress_decay": self.awakening.progress_decay,
            },
            "log_level": self.log_level,
            "log_file": self.log_file,
            "log_dir": self.log_dir,
            "version": self.version,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "YogacaraConfig":
        """Create configuration from dictionary."""
        seed_config = SeedSystemConfig(**data.get("seed_system", {}))
        store_config = AlayaStoreConfig(**data.get("alaya_store", {}))
        emerge_config = EmergenceConfig(**data.get("emergence", {}))
        awake_config = AwakeningConfig(**data.get("awakening", {}))
        
        return cls(
            seed_system=seed_config,
            alaya_store=store_config,
            emergence=emerge_config,
            awakening=awake_config,
            log_level=data.get("log_level", "INFO"),
            log_file=data.get("log_file"),
            log_dir=data.get("log_dir"),
            version=data.get("version", "0.1.0"),
        )
    
    @classmethod
    def from_yaml(cls, path: Union[str, Path]) -> "YogacaraConfig":
        """Load configuration from YAML file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        
        return cls.from_dict(data or {})
    
    @classmethod
    def from_json(cls, path: Union[str, Path]) -> "YogacaraConfig":
        """Load configuration from JSON file."""
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"Config file not found: {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return cls.from_dict(data)
    
    def save_yaml(self, path: Union[str, Path]) -> None:
        """Save configuration to YAML file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            yaml.dump(self.to_dict(), f, default_flow_style=False)
    
    def save_json(self, path: Union[str, Path], indent: int = 2) -> None:
        """Save configuration to JSON file."""
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, indent=indent)
    
    @classmethod
    def from_env(cls, prefix: str = "YOGACARA_") -> "YogacaraConfig":
        """
        Load configuration from environment variables.
        
        Environment variables should be prefixed with YOGACARA_
        and use uppercase with underscores.
        
        Example:
            YOGACARA_SEED_SYSTEM_PURITY_THRESHOLD=0.5
        """
        config = cls()
        
        # Map environment variables to config fields
        env_mappings = {
            "SEED_SYSTEM_PURITY_THRESHOLD": ("seed_system", "purity_threshold", float),
            "SEED_SYSTEM_WEIGHT_DECAY_RATE": ("seed_system", "weight_decay_rate", float),
            "SEED_SYSTEM_MAX_SEEDS": ("seed_system", "max_seeds", int),
            "ALAYA_STORE_DB_PATH": ("alaya_store", "db_path", str),
            "EMERGENCE_MIN_SEEDS": ("emergence", "min_seeds", int),
            "EMERGENCE_SYMMETRY_THRESHOLD": ("emergence", "synergy_threshold", float),
            "LOG_LEVEL": ("log_level", None, str),
        }
        
        for env_var, (section, field, type_fn) in env_mappings.items():
            full_name = f"{prefix}{env_var}"
            value = os.environ.get(full_name)
            if value is not None:
                try:
                    typed_value = type_fn(value)
                    if section == "log_level":
                        config.log_level = typed_value
                    elif section:
                        setattr(getattr(config, section), field, typed_value)
                except (ValueError, TypeError):
                    pass
        
        return config
    
    @classmethod
    def default_config_path(cls) -> Path:
        """Get the default configuration file path."""
        return Path.home() / ".config" / "yogacara" / "config.yaml"
    
    @classmethod
    def load(
        cls,
        path: Optional[Union[str, Path]] = None,
        create_default: bool = False,
    ) -> "YogacaraConfig":
        """
        Load configuration with automatic path detection.
        
        Search order:
        1. Explicit path
        2. Environment variable YOGACARA_CONFIG
        3. ~/.config/yogacara/config.yaml
        4. ./config.yaml
        5. Default configuration
        
        Args:
            path: Explicit configuration file path
            create_default: Create default config if not found
            
        Returns:
            YogacaraConfig instance
        """
        # Check explicit path
        if path:
            path = Path(path)
            if path.exists():
                return cls.from_yaml(path) if path.suffix in (".yaml", ".yml") else cls.from_json(path)
        
        # Check environment variable
        env_path = os.environ.get("YOGACARA_CONFIG")
        if env_path:
            env_path = Path(env_path)
            if env_path.exists():
                return cls.from_yaml(env_path) if env_path.suffix in (".yaml", ".yml") else cls.from_json(env_path)
        
        # Check default locations
        default_path = cls.default_config_path()
        if default_path.exists():
            return cls.from_yaml(default_path)
        
        local_path = Path("config.yaml")
        if local_path.exists():
            return cls.from_yaml(local_path)
        
        # Return default or create
        if create_default:
            config = cls()
            config.save_yaml(default_path)
            return config
        
        return cls()
