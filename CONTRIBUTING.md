# Contributing to Discord Scheduled Channel Manager Bot

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## Table of Contents
- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Submitting Changes](#submitting-changes)
- [Code Style Guidelines](#code-style-guidelines)
- [Testing](#testing)

## Code of Conduct

This project adheres to a code of conduct that we expect all contributors to follow. Please be respectful and constructive in all interactions.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Set up the development environment
4. Create a branch for your changes
5. Make your changes
6. Test your changes
7. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- A Discord bot token for testing

### Environment Setup

1. **Clone your fork:**
   ```bash
   git clone https://github.com/yourusername/discord-scheduled-channel-manager.git
   cd discord-scheduled-channel-manager
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `configuration.env` file with your test bot token:
   ```env
   BOT_TOKEN=your_test_bot_token_here
   TIMEZONE=America/New_York
   ```

## Making Changes

### Branch Naming
Use descriptive branch names:
- `feature/add-new-command` for new features
- `bugfix/fix-channel-deletion` for bug fixes
- `docs/update-readme` for documentation changes
- `refactor/improve-database-handling` for code improvements

### Commit Messages
Write clear, concise commit messages:
- Use the present tense ("Add feature" not "Added feature")
- Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
- Limit the first line to 72 characters or less
- Reference issues and pull requests liberally after the first line

Example:
```
Add channel locking functionality

- Implement channel permission locking after specified time
- Add database table for tracking channel locks
- Update scheduled task to handle lock operations
- Fixes #123
```

## Submitting Changes

### Pull Request Process

1. **Update documentation** if needed
2. **Test your changes** thoroughly
3. **Update the changelog** if your changes are user-facing
4. **Create a pull request** with:
   - Clear title and description
   - Reference to related issues
   - Screenshots/examples if applicable
   - List of changes made

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
- [ ] Tested locally
- [ ] Added/updated tests
- [ ] All tests pass

## Related Issues
Fixes #(issue number)

## Screenshots (if applicable)
```

## Code Style Guidelines

### Python Code Style
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to functions and classes
- Keep functions focused and small
- Use type hints where appropriate

### Example:
```python
async def create_scheduled_channel(
    guild: discord.Guild,
    category: discord.CategoryChannel,
    name: str,
    role: Optional[discord.Role] = None
) -> discord.TextChannel:
    """
    Create a scheduled channel in the specified category.
    
    Args:
        guild: The Discord guild to create the channel in
        category: The category to place the channel in
        name: The name for the new channel
        role: Optional role to grant access to the channel
        
    Returns:
        The created text channel
        
    Raises:
        discord.HTTPException: If channel creation fails
    """
    # Implementation here
```

### File Organization
- Keep imports organized (standard library, third-party, local)
- Use consistent indentation (4 spaces)
- Add comments for complex logic
- Group related functions together

### Error Handling
- Use specific exception types when possible
- Log errors appropriately
- Provide meaningful error messages to users
- Don't suppress exceptions without good reason

## Testing

### Manual Testing
1. Test bot commands in a development Discord server
2. Verify scheduled tasks work correctly
3. Test edge cases and error conditions
4. Check database operations

### Test Checklist
- [ ] Bot starts without errors
- [ ] Commands respond correctly
- [ ] Scheduled tasks execute as expected
- [ ] Database operations work properly
- [ ] Error handling works as intended
- [ ] Permissions are enforced correctly

## Documentation

### Code Documentation
- Add docstrings to all public functions and classes
- Include parameter and return type information
- Document any side effects or important behavior

### User Documentation
- Update README.md for user-facing changes
- Add examples for new features
- Update command documentation
- Keep installation instructions current

## Questions and Support

If you have questions about contributing:
1. Check existing issues and pull requests
2. Review this contributing guide
3. Create an issue for discussion
4. Ask in the project's Discord server (if available)

## Recognition

Contributors will be recognized in:
- The project's README
- Release notes for significant contributions
- The project's contributors page

Thank you for contributing to making this project better!
