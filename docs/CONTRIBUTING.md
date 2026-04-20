# Contributing to Yogacara

Thank you for your interest in contributing to Yogacara! This document provides guidelines and instructions for contributing.

---

## Code of Conduct

By participating in this project, you agree to maintain a welcoming and respectful environment for all contributors, regardless of background or experience level.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- Basic understanding of Yogacara philosophy (see README.md)

### Setting Up Development Environment

1. **Fork the repository** on GitHub

2. **Clone your fork:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/yogacara.git
   cd yogacara
   ```

3. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   .\venv\Scripts\activate  # Windows
   ```

4. **Install dependencies:**
   ```bash
   pip install -e ".[dev,cli]"
   ```

5. **Install pre-commit hooks:**
   ```bash
   pre-commit install
   ```

---

## Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/your-bug-fix
```

Branch naming conventions:
- `feature/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation changes
- `refactor/` - Code refactoring
- `test/` - Test additions/changes

### 2. Make Changes

- Write code following the project's style guidelines
- Add/update tests for new functionality
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=yogacara --cov-report=html

# Run specific test file
pytest tests/test_seed_system.py

# Run tests matching a pattern
pytest -k "test_seed"
```

### 4. Code Quality Checks

```bash
# Format code
black yogacara tests examples

# Sort imports
isort yogacara tests examples

# Type checking
mypy yogacara

# Linting
flake8 yogacara tests examples
```

### 5. Commit Changes

Follow the conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Refactoring
- `test` - Testing
- `chore` - Maintenance

Example:
```
feat(seed-system): add support for custom seed metadata

- Add metadata field to Seed dataclass
- Update AlayaStore to persist metadata
- Add tests for metadata handling

Closes #42
```

### 6. Push and Create Pull Request

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub with:
- Clear title and description
- Reference to related issues
- Description of changes

---

## Project Structure

```
yogacara/
├── yogacara/              # Main package
│   ├── __init__.py       # Package exports
│   ├── cli.py            # CLI interface
│   ├── config.py         # Configuration
│   ├── logger.py         # Logging utilities
│   ├── core/             # Core modules
│   │   ├── __init__.py
│   │   ├── seed_system.py
│   │   ├── alaya_store.py
│   │   ├── emergence.py
│   │   └── awakening.py
│   ├── adapters/         # Adapter layer
│   ├── docs/             # Documentation
│   ├── papers/           # Research papers
│   └── examples/         # Example scripts
├── tests/                # Test suite
├── docs/                 # Documentation files
├── scripts/              # Utility scripts
├── pyproject.toml        # Project configuration
└── README.md             # Project overview
```

---

## Coding Guidelines

### Python Version

- Use Python 3.8+ syntax
- No type comments (use type annotations instead)

### Type Annotations

All functions must have type annotations:

```python
# Good
def create_seed(type: SeedType, content: str) -> Optional[Seed]:
    ...

# Bad
def create_seed(type, content):
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def method(arg1: str, arg2: int) -> bool:
    """
    Short description.

    Longer description if needed.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: When arg2 is invalid
    """
    pass
```

### Dataclasses

Use `@dataclass` for data structures:

```python
@dataclass
class Emergence:
    seed_ids: List[str]
    emergence_type: EmergenceType
    strength: float
    insight: Optional[str] = None
```

### Error Handling

- Use specific exceptions
- Include meaningful error messages
- Log errors appropriately

```python
# Good
if purity < 0.0 or purity > 1.0:
    raise ValueError(f"Purity must be between 0.0 and 1.0, got {purity}")

# Bad
if purity < 0:
    return None
```

### Testing Guidelines

- Use `pytest` framework
- Name test files: `test_*.py`
- Name test classes: `Test*`
- Name test functions: `test_*`
- Use fixtures for common setup
- Aim for meaningful assertions

```python
class TestSeed:
    def test_create_seed_with_defaults(self):
        """Test creating a seed with default values."""
        seed = Seed(type=SeedType.WISDOM, content="Test")
        
        assert seed.purity == 0.7
        assert seed.weight == 0.5
```

---

## Documentation Guidelines

### README

Keep the README.md updated with:
- Clear project description
- Quick start guide
- Key features
- Installation instructions

### Docstrings

Document all public APIs:
- Classes and their purpose
- Methods with parameters and return values
- Examples when helpful

### API Reference

Update `docs/API_REFERENCE.md` when adding/modifying APIs.

---

## Reporting Issues

When reporting issues, please include:

1. **Issue type** (Bug, Feature, Documentation)
2. **Yogacara version**
3. **Python version**
4. **Environment details**
5. **Steps to reproduce**
6. **Expected vs actual behavior**
7. **Error messages/logs**

---

## Questions?

- Open an issue for bugs/features
- Check existing issues before creating new ones
- Be responsive to feedback on your contributions

---

## Recognition

Contributors will be recognized in:
- The project's README.md contributors section
- Release notes for significant contributions
- GitHub's contributor graph

Thank you for contributing to Yogacara! 🙏
