# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2024-01-01

### Added

#### Core Components
- **Seed System** (`yogacara.core.seed_system`)
  - `SeedType` enum with 4 seed types (WISDOM, COMPASSION, BELIEF, BEHAVIOR)
  - `Seed` dataclass with purity, weight, vasana tracking
  - `SeedSystem` class for seed creation and management
  
- **Alaya Store** (`yogacara.core.alaya_store`)
  - SQLite-based persistent storage
  - FTS5 full-text search for seed retrieval
  - Seed activation and vasana increment
  - Emergence history tracking

- **Emergence Engine** (`yogacara.core.emergence`)
  - `EmergenceType` enum (FUSION, TENSION, LEAP)
  - Synergy calculation based on seed diversity
  - Automatic insight generation
  - Strength threshold detection

- **Awakening Tracker** (`yogacara.core.awakening`)
  - 6 awakening levels (L0-L5)
  - Level progression based on wisdom, compassion, emergence
  - Progress visualization

#### Supporting Modules
- **Configuration** (`yogacara.config`)
  - `YogacaraConfig` dataclass
  - YAML/JSON/ENV configuration loading
  - Component-level configuration options

- **Logging** (`yogacara.logger`)
  - `YogacaraLogger` class
  - Structured logging with seed/emergence events
  - File and console output support

- **CLI** (`yogacara.cli`)
  - Interactive CLI tool
  - Commands: info, status, plant, activate, levels, check-level, stats
  - Rich terminal output

#### Testing
- Test suite for all core modules
- Pytest configuration
- Coverage tracking

#### Documentation
- README.md with philosophy and quick start
- ARCHITECTURE.md with system design
- API_REFERENCE.md with complete API docs
- CONTRIBUTING.md for developers

#### Project Configuration
- `pyproject.toml` with all settings
- `setup.py` for PyPI distribution
- `requirements.txt` with dependencies
- `.gitignore` for common patterns

### Examples
- `examples/basic_usage.py` - Fundamental concepts
- `examples/custom_seeds.py` - Advanced seed features
- `examples/awakening_journey.py` - Level progression simulation

---

## [Unreleased]

### Planned Features

#### v0.2.0
- [ ] LLM integration adapters (OpenAI, Anthropic, Local)
- [ ] Async support for Alaya Store
- [ ] PostgreSQL backend option
- [ ] Seed clustering for pattern detection
- [ ] Advanced emergence prediction

#### v0.3.0
- [ ] WebSocket API for real-time updates
- [ ] Dashboard for seed visualization
- [ ] Export/import seed banks
- [ ] Multi-agent seed sharing
- [ ] Advanced CLI with REPL

#### Future
- [ ] Docker containerization
- [ ] Kubernetes operator
- [ ] Cloud native deployment
- [ ] Plugin system for custom seed types
- [ ] GraphQL API

---

## Versioning

This project uses [Semantic Versioning](https://semver.org/):
- **MAJOR** version for incompatible API changes
- **MINOR** version for backwards-compatible functionality
- **PATCH** version for backwards-compatible bug fixes

---

## Migration Guides

### Upgrading from v0.0.x to v0.1.0

The v0.1.0 release introduces several breaking changes:

1. **Package structure changed:**
   ```python
   # Old
   from yogacara.seed_system import Seed
   
   # New
   from yogacara import Seed
   ```

2. **Seed creation changed:**
   ```python
   # Old
   seed = Seed.create(type="wisdom", content="...")
   
   # New
   seed = Seed(type=SeedType.WISDOM, content="...")
   ```

3. **Awakening levels are now enums:**
   ```python
   # Old
   tracker.set_level("L2")
   
   # New
   tracker.current_level = AwakeningLevel.L2_PRACTICE
   ```

---

## Deprecation Policy

- Deprecated features will be marked with warnings
- At least one minor version will pass before removal
- Migration guides will be provided
