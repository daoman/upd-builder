# Contributing to UPD Builder

Thank you for considering contributing to UPD Builder! Here's how you can help.

## Getting Started

### Fork & Clone

```bash
git clone https://github.com/yourusername/upd-builder.git
cd upd-builder
```

### Set Up Development Environment

```bash
# Create virtual environment
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install in development mode with all dependencies
pip install -e ".[dev]"
```

### Run Tests

```bash
pytest tests/
pytest tests/ --cov=upd_builder  # With coverage
```

### Check Code Quality

```bash
black .           # Format code
flake8 upd_builder tests
mypy upd_builder  # Type checking
```

## Making Changes

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use [Black](https://github.com/psf/black) for formatting
- Add type hints to all functions and methods
- Use docstrings in Google style

### Commit Messages

```
[FEATURE] Add new capability
[FIX] Correct bug in module
[DOCS] Update documentation
[TEST] Add new tests

Brief description of what changed and why.

More detailed explanation if needed.

Fixes #123
```

### Adding Features

1. Create a feature branch: `git checkout -b feature/my-feature`
2. Write tests first (TDD approach)
3. Implement the feature
4. Ensure all tests pass: `pytest`
5. Update documentation if needed
6. Create a pull request

### Reporting Issues

Include:
- Python version
- upd-builder version
- Minimal code to reproduce
- Expected vs actual behavior
- Full error traceback

## Testing Requirements

- All changes must include tests
- Tests must pass: `pytest`
- Try to maintain or improve code coverage
- Test edge cases and error scenarios

## Documentation

- Update README.md when adding features
- Add docstrings to all public functions/classes
- Include usage examples where helpful
- Update CHANGELOG.md

## Pull Request Process

1. Update your fork: `git pull origin main`
2. Create feature branch
3. Make your changes
4. Run tests and code quality checks
5. Update docs as needed
6. Push to your fork
7. Submit PR with clear description

### PR Requirements

- [ ] Tests included
- [ ] Documentation updated
- [ ] Code formatted (black)
- [ ] Type hints added
- [ ] No regression in coverage
- [ ] Commit messages are clear

## Development Tips

### Running Specific Tests

```bash
pytest tests/test_upd_builder.py::TestXmlGeneration::test_xml_generation
```

### Debugging

```python
import pdb
pdb.set_trace()  # Add this before the code you want to debug
```

### Type Checking

```bash
mypy upd_builder --strict
```

## Release Process

1. Update version in `upd_builder/__init__.py`
2. Update CHANGELOG.md
3. Merge to main branch
4. Tag release: `git tag v1.0.0`
5. Build and publish: `python -m build && twine upload dist/*`

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Feel free to open an issue or reach out to the maintainers.

Happy coding! 🚀
