# Contributing to Skill Router

Thank you for your interest in contributing to Skill Router!

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/01100001singh/skill-router.git
cd skill-router
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
```

3. Install development dependencies:
```bash
pip install -e ".[dev,all]"
```

4. Install pre-commit hooks:
```bash
pre-commit install
```

## Running Tests

```bash
pytest tests/ -v
```

With coverage:
```bash
pytest tests/ -v --cov=skill_router
```

## Code Style

We use:
- **ruff** for linting and formatting
- **mypy** for type checking

Run checks:
```bash
ruff check src/ tests/
mypy src/skill_router/
```

## Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Make your changes
4. Run tests and linting
5. Commit with a clear message
6. Push and create a PR

## Contributing Skills

See [skills/community/README.md](../skills/community/README.md) for guidelines on contributing skills.

## Reporting Issues

- Use the issue templates
- Include reproduction steps
- Include Python version and OS

## Code of Conduct

Be respectful and constructive in all interactions.
