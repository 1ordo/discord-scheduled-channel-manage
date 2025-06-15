#!/usr/bin/env python3
"""
Setup script for Discord Scheduled Channel Manager Bot.

This script helps users set up the bot with the necessary configuration
and dependencies.
"""

import os
import shutil
import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required.")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python version: {sys.version.split()[0]}")


def install_dependencies():
    """Install required Python dependencies."""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
        )
        print("✅ Dependencies installed successfully!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        sys.exit(1)


def create_config_file():
    """Create configuration file from template."""
    config_file = "configuration.env"
    template_file = "configuration.env.template"

    if os.path.exists(config_file):
        print(f"⚠️  Configuration file {config_file} already exists.")
        response = input("Do you want to overwrite it? (y/N): ").lower()
        if response != "y":
            print("Skipping configuration file creation.")
            return

    if not os.path.exists(template_file):
        print(f"❌ Template file {template_file} not found.")
        return

    print(f"\n📝 Creating configuration file...")
    shutil.copy(template_file, config_file)

    print(f"✅ Created {config_file}")
    print("\n⚠️  IMPORTANT: Please edit the configuration file and add your bot token!")
    print(
        f"   Edit {config_file} and replace 'your_discord_bot_token_here' with your actual bot token."
    )


def create_directories():
    """Create necessary directories."""
    directories = ["logs", "backups"]

    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"📁 Created directory: {directory}")


def display_next_steps():
    """Display next steps for the user."""
    print("\n" + "=" * 60)
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Edit configuration.env with your Discord bot token")
    print("2. Set your preferred timezone in configuration.env")
    print("3. Invite your bot to your Discord server with appropriate permissions:")
    print("   - Read Messages")
    print("   - Send Messages")
    print("   - Manage Channels")
    print("   - View Channels")
    print("   - Manage Roles (if using role-based permissions)")
    print("4. Run the bot with: python main.py")
    print("\n📚 For more information, see README.md")
    print(
        "🐛 For issues, visit: https://github.com/yourusername/discord-scheduled-channel-manager/issues"
    )


def main():
    """Main setup function."""
    print("🚀 Discord Scheduled Channel Manager Bot Setup")
    print("=" * 50)

    # Check Python version
    check_python_version()

    # Install dependencies
    install_dependencies()

    # Create configuration file
    create_config_file()

    # Create directories
    create_directories()

    # Display next steps
    display_next_steps()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Setup cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
