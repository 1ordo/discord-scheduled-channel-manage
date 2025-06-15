"""
Configuration management for the Discord Scheduled Channel Manager Bot.

This module handles loading environment variables and configuration
settings from the .env file and environment.
"""

import os
import sys
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from configuration.env
load_dotenv(dotenv_path="configuration.env")

# Bot configuration
BOT_TOKEN: Optional[str] = os.getenv('BOT_TOKEN')
TIMEZONE: str = os.getenv("TIMEZONE", "UTC")  # Default to UTC if not specified

# Validate required configuration
if not BOT_TOKEN:
    print("❌ Error: BOT_TOKEN not found in environment variables!")
    print("Please create a configuration.env file with your bot token.")
    print("See configuration.env.template for an example.")
    sys.exit(1)

# Database configuration
DATABASE_FILE: str = os.getenv("DATABASE_FILE", "system_data.db")

# Logging configuration
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()
LOG_FILE: str = os.getenv("LOG_FILE", "bot.log")

# Task configuration
TASK_INTERVAL_MINUTES: int = int(os.getenv("TASK_INTERVAL_MINUTES", "1"))

print(f"✅ Configuration loaded successfully")
print(f"📍 Timezone: {TIMEZONE}")
print(f"📊 Database: {DATABASE_FILE}")
print(f"⏱️  Task interval: {TASK_INTERVAL_MINUTES} minute(s)")