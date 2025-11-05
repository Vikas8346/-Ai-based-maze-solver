# Contributing to AI-Based Maze Solver

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. **Check existing issues** first to avoid duplicates
2. **Create a new issue** with:
   - Clear, descriptive title
   - Steps to reproduce
   - Expected vs. actual behavior
   - Your environment (OS, Python version)
   - Screenshots if applicable

### Suggesting Features

1. **Open an issue** with `[Feature Request]` in the title
2. **Describe the feature** clearly
3. **Explain the use case** and benefits
4. **Provide examples** if possible

### Pull Requests

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/YourFeature`
3. **Make your changes** following our code style
4. **Add tests** for new functionality
5. **Update documentation** as needed
6. **Commit with clear messages**: `git commit -m "Add feature: description"`
7. **Push to your fork**: `git push origin feature/YourFeature`
8. **Open a Pull Request** with description of changes

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/-Ai-based-maze-solver.git
cd -Ai-based-maze-solver

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install development dependencies
pip install pytest pytest-cov black flake8
```

## Code Style

- Follow **PEP 8** guidelines
- Use **type hints** where appropriate
- Write **docstrings** for all functions/classes
- Keep functions **focused and small**
- Use **meaningful variable names**

### Format Code

```bash
# Format with black
black src/ tests/

# Check with flake8
flake8 src/ tests/
```

## Testing

```bash
# Run all tests
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

## Documentation

- Update **README.md** for major features
- Update **docs/** for detailed explanations
- Add **docstrings** to new functions
- Include **examples** for new features

## Areas to Contribute

### Algorithms
- Implement new pathfinding algorithms (Jump Point Search, Theta*, etc.)
- Optimize existing algorithms
- Add new heuristic functions

### Visualization
- Improve GUI design
- Add animation controls (speed, pause, step-through)
- Implement 3D visualization

### Features
- Save/load maze functionality
- More maze generation algorithms
- Web-based interface
- Weighted graph support

### Documentation
- Improve existing docs
- Add tutorials
- Create video guides
- Translate to other languages

### Testing
- Increase test coverage
- Add performance benchmarks
- Create integration tests

## Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Help others learn
- Follow the golden rule

## Questions?

- Open an issue with `[Question]` tag
- Discuss in pull request comments
- Contact maintainers

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🎉
