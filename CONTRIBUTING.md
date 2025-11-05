# Contributing to Robotics Industry Projections 2026

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. **Fork and Clone**
   ```bash
   git clone https://github.com/yourusername/robotics_2026.git
   cd robotics_2026
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. **Run Tests**
   ```bash
   pytest tests/
   ```

## Code Style

- Follow PEP 8 style guide
- Use type hints where possible
- Write docstrings for all functions and classes
- Keep functions focused and small
- Add comments for complex logic

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage
- Use descriptive test names

## Pull Request Process

1. Create a feature branch from `master`
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes
3. Add tests if applicable
4. Update documentation if needed
5. Ensure all tests pass
6. Commit with clear messages
   ```bash
   git commit -m "Add feature: description"
   ```

7. Push and create Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

## Commit Messages

Use clear, descriptive commit messages:
- `Add feature: interactive dashboard`
- `Fix bug: data loading error`
- `Update docs: add API examples`
- `Refactor: improve error handling`

## Questions?

Open an issue for questions or discussions about the project.

