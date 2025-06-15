# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] - 2025-06-15

### Added
- Initial release of Discord Scheduled Channel Manager Bot
- Scheduled channel creation with daily time configuration
- Automatic channel deletion after specified duration
- Channel locking functionality to prevent further messages
- Role-based permissions for channel access
- Timezone support for global server compatibility
- SQLite database for persistent data storage
- Command: `/scheduled_channel_create` with Set, Remove, and Show actions
- Support for 12-hour time format (AM/PM)
- Duration parsing for hours and minutes (e.g., "2h 30m")
- Direct message notifications to role members when channels are created
- Automatic database table creation on first run
- Comprehensive error handling and logging
- Permission validation for commands

### Technical Details
- Built with discord.py library
- Uses SQLite for data persistence
- Implements timezone-aware datetime handling with pytz
- Modular code structure with separate modules for commands, tasks, and resources
- Background task loop for channel management
- Custom permission decorator system
- Environment variable configuration support
