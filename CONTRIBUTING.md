# Contributing to App Store Icon Hunter

We love your input! We want to make contributing to App Store Icon Hunter as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Any contributions you make will be under the MIT Software License

In short, when you submit code changes, your submissions are understood to be under the same [MIT License](http://choosealicense.com/licenses/mit/) that covers the project. Feel free to contact the maintainers if that's a concern.

## Report bugs using GitHub's [issues](https://github.com/Garyku0/app-store-icon-hunter/issues)

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/username/app-store-icon-hunter/issues/new); it's that easy!

## Write bug reports with detail, background, and sample code

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Development Setup

### Requirements

- Python 3.8+
- Git
- Virtual environment tool (venv, conda, etc.)

### Setup Steps

```bash
# 1. Fork and clone the repository
git clone https://github.com/Garyku0/app-store-icon-hunter.git
cd app-store-icon-hunter

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install in development mode
pip install -e ".[dev]"

# 4. Install pre-commit hooks (if available)
pre-commit install

# 5. Run tests to ensure everything works
pytest
```

### Development Dependencies

The development dependencies include:
- `pytest` - Testing framework
- `pytest-cov` - Coverage reporting
- `black` - Code formatting
- `flake8` - Linting
- `mypy` - Type checking

## Code Style

We use several tools to maintain code quality:

### Formatting
```bash
# Format all code
black app_store_icon_hunter/
black tests/
```

### Linting
```bash
# Check code style
flake8 app_store_icon_hunter/
flake8 tests/
```

### Type Checking
```bash
# Run type checker
mypy app_store_icon_hunter/
```

## Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app_store_icon_hunter

# Run specific test file
pytest tests/test_cli.py

# Run tests matching a pattern
pytest -k "test_search"
```

### Writing Tests

- Write tests for new features
- Ensure existing tests pass
- Add integration tests for CLI commands
- Mock external API calls in tests

Example test structure:
```python
def test_search_functionality():
    """Test that search returns expected results."""
    # Arrange
    search_term = "test app"
    
    # Act
    results = search_apps(search_term)
    
    # Assert
    assert len(results) > 0
    assert all('name' in app for app in results)
```

## Project Structure

Understanding the project structure will help you contribute effectively:

```
app_store_icon_hunter/
├── __init__.py           # Package initialization
├── cli/                  # Command-line interface
│   ├── __init__.py
│   └── main.py          # CLI commands and logic
├── api/                  # REST API server
│   ├── __init__.py
│   └── main.py          # FastAPI application
├── core/                 # Core functionality
│   ├── __init__.py
│   ├── app_store.py     # App Store API integration
│   ├── google_play.py   # Google Play API integration
│   └── downloader.py    # Icon downloading logic
└── utils/                # Utility functions
    ├── __init__.py
    └── helpers.py       # Helper functions
```

## Areas for Contribution

### High Priority
- **Performance improvements** - Optimize icon downloading
- **Error handling** - Better error messages and recovery
- **Documentation** - Improve examples and guides
- **Testing** - Increase test coverage

### Medium Priority
- **New features** - SVG support, image optimization
- **Platform support** - Windows-specific improvements
- **API enhancements** - New endpoints, better responses

### Low Priority
- **UI improvements** - Better CLI experience
- **Integrations** - Support for more app stores
- **Advanced features** - Batch processing, custom workflows

## Git Workflow

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation updates
- `refactor/description` - Code refactoring

### Commit Messages
Follow conventional commit format:
```
type(scope): description

[optional body]

[optional footer]
```

Examples:
- `feat(cli): add interactive app selection`
- `fix(api): handle invalid search terms`
- `docs(readme): update installation instructions`

### Pull Request Process

1. **Create Issue** - Discuss the change you want to make
2. **Fork & Branch** - Create a feature branch from main
3. **Develop** - Make your changes with tests
4. **Test** - Ensure all tests pass
5. **Document** - Update relevant documentation
6. **Submit PR** - Create pull request with description

### Pull Request Template
```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
- [ ] Tests pass locally
- [ ] New tests added (if applicable)
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or clearly documented)
```

## Getting Help

- **GitHub Issues** - For bugs and feature requests
- **Discussions** - For questions and general discussion
- **Discord/Slack** - For real-time chat (if available)

## Code of Conduct

### Our Pledge
We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards
Examples of behavior that contributes to creating a positive environment include:
- Being respectful and inclusive
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

### Enforcement
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting the project maintainers. All complaints will be reviewed and investigated.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask questions! The maintainers are here to help. You can:
- Open an issue with the `question` label
- Reach out to maintainers directly
- Start a discussion in the GitHub Discussions section

Thank you for contributing to App Store Icon Hunter! 🚀
