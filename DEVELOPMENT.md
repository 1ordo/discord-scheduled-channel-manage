# Discord Scheduled Channel Manager Bot - Development Guide

## Development Setup

### Prerequisites
- Python 3.8 or higher
- Git
- Discord Bot Token
- IDE/Editor (VS Code recommended)

### Local Development

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/discord-scheduled-channel-manager.git
   cd discord-scheduled-channel-manager
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up configuration:**
   ```bash
   cp configuration.env.template configuration.env
   # Edit configuration.env with your bot token
   ```

5. **Run the bot:**
   ```bash
   python main.py
   ```

### Development Tools

#### Code Formatting
```bash
# Install formatting tools
pip install black isort flake8

# Format code
black .
isort .

# Check linting
flake8 .
```

#### Type Checking
```bash
pip install mypy
mypy . --ignore-missing-imports
```

#### Testing
```bash
# Test configuration loading
python -c "from configuration import BOT_TOKEN; print('Config OK')"

# Test database
python -c "from database import database; database.connect(); database.create_table(); print('DB OK')"
```

## Project Structure

```
├── main.py                 # Bot entry point
├── client.py              # Discord client setup
├── configuration.py       # Environment configuration
├── database.py           # Database operations
├── requirements.txt      # Python dependencies
├── setup.py             # Setup script
├── Dockerfile           # Docker configuration
├── docker-compose.yml   # Docker Compose setup
├── commands/
│   ├── channel_creation.py  # Channel management commands
│   └── message_lock.py      # Message locking functionality
├── resources/
│   └── permissions.py       # Permission decorators
├── tasks/
│   └── time_check.py        # Scheduled task management
└── .github/
    └── workflows/
        └── ci-cd.yml        # GitHub Actions CI/CD
```

## Adding New Features

### Adding a New Command

1. Create a new file in `commands/` directory
2. Import necessary modules:
   ```python
   from client import client
   from discord import app_commands, Interaction
   from resources.permissions import has_permissions
   ```

3. Define your command:
   ```python
   @client.tree.command(name="your_command", description="Your description")
   @has_permissions(manage_guild=True)
   async def your_command(interaction: Interaction):
       # Your command logic here
       pass
   ```

4. Import the command in `main.py`:
   ```python
   import commands.your_new_command
   ```

### Adding Database Operations

1. Add methods to the `Database` class in `database.py`
2. Follow existing patterns for error handling and logging
3. Use type hints and docstrings
4. Test your database operations

### Adding Scheduled Tasks

1. Add your task function in `tasks/` directory
2. Use the `@tasks.loop()` decorator
3. Start your task in the `on_ready` event in `main.py`

## Code Style Guidelines

### Python Style
- Follow PEP 8
- Use type hints
- Add docstrings to all functions and classes
- Use meaningful variable names
- Keep functions small and focused

### Import Organization
```python
# Standard library imports
import os
import logging

# Third-party imports
import discord
from discord.ext import tasks

# Local imports
from client import client
from database import database
```

### Error Handling
```python
try:
    # Your code here
    logger.info("Operation successful")
except SpecificException as e:
    logger.error(f"Specific error: {e}")
    # Handle specific error
except Exception as e:
    logger.error(f"Unexpected error: {e}", exc_info=True)
    # Handle general error
```

### Logging
```python
import logging
logger = logging.getLogger(__name__)

# Use appropriate log levels
logger.debug("Debug information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error message")
```

## Testing

### Manual Testing Checklist
- [ ] Bot starts without errors
- [ ] Commands respond correctly
- [ ] Database operations work
- [ ] Scheduled tasks execute
- [ ] Error handling works
- [ ] Permissions are enforced

### Environment Testing
- [ ] Development environment
- [ ] Docker container
- [ ] Different Python versions
- [ ] Different operating systems

## Docker Development

### Build and run locally:
```bash
docker build -t discord-bot .
docker run -e BOT_TOKEN=your_token discord-bot
```

### Using Docker Compose:
```bash
cp configuration.env.template configuration.env
# Edit configuration.env
docker-compose up -d
```

### View logs:
```bash
docker-compose logs -f discord-bot
```

## Git Workflow

### Branch Naming
- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation changes

### Commit Messages
```
type: short description

Longer description if needed

- Change 1
- Change 2
- Change 3

Fixes #issue_number
```

### Pull Request Process
1. Create feature branch from `develop`
2. Make your changes
3. Test thoroughly
4. Update documentation
5. Create pull request to `develop`
6. Address review feedback
7. Merge when approved

## Deployment

### Production Checklist
- [ ] Environment variables set
- [ ] Database backed up
- [ ] Logs configured
- [ ] Health checks working
- [ ] Resource limits set
- [ ] Security scan passed

### Monitoring
- Check bot status regularly
- Monitor logs for errors
- Track database growth
- Monitor resource usage

## Troubleshooting

### Common Issues

**Bot won't start:**
- Check bot token validity
- Verify all dependencies installed
- Check configuration file

**Commands not responding:**
- Ensure bot has necessary permissions
- Check if commands are synced
- Verify slash command registration

**Database errors:**
- Check file permissions
- Verify database file exists
- Check for SQLite version compatibility

**Scheduled tasks not running:**
- Check timezone configuration
- Verify task loop is started
- Check for errors in logs

### Debug Mode
Set `LOG_LEVEL=DEBUG` in configuration for verbose logging.

### Getting Help
1. Check the logs first
2. Review this development guide
3. Check existing issues on GitHub
4. Create a new issue with:
   - Clear description
   - Steps to reproduce
   - Expected vs actual behavior
   - Log output
   - Environment details

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## Security

See [SECURITY.md](SECURITY.md) for security guidelines and reporting vulnerabilities.
