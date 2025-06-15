"""
Discord Scheduled Channel Manager Bot

A Discord bot that automatically creates, manages, and schedules text channels
based on time configurations. Perfect for temporary announcements, daily standup
channels, or time-based community events.

Author: GitHub Copilot Enhanced
License: MIT
"""

import asyncio
import inspect
import logging
import sys
from typing import Optional

import discord
from discord import app_commands

from client import client
from configuration import BOT_TOKEN
from database import database
from resources.permissions import MissingPermissions
from tasks.time_check import scheduled_channel_management_task

# Import command modules to register them
import commands.channel_creation
import commands.message_lock
import tasks.time_check

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

def initialize_database() -> None:
    """Initialize the database and create necessary tables."""
    try:
        database.connect()
        database.create_table()
        database.close()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}")
        raise


@client.event
async def on_ready() -> None:
    """Event handler for when the bot is ready and connected to Discord."""
    try:
        # Sync command tree with Discord
        await client.tree.sync()
        logger.info("Command tree synced successfully")
        
        # Set bot presence (optional)
        activity = discord.Activity(
            type=discord.ActivityType.watching, 
            name="for scheduled channels"
        )
        await client.change_presence(activity=activity)
        
        if not client.user:
            raise RuntimeError("on_ready() called before Client.user was set!")
            
        logger.info(f"Bot logged in as {client.user} (ID: {client.user.id})")
        print("=" * 80)
        print(f"✅ {client.user} is now online!")
        print(f"📊 Connected to {len(client.guilds)} guild(s)")
        print("=" * 80)
        
        # Start scheduled tasks
        if not scheduled_channel_management_task.is_running():
            scheduled_channel_management_task.start()
            logger.info("Scheduled channel management task started")
            
    except Exception as e:
        logger.error(f"Error in on_ready: {e}")
        raise
    


@client.tree.error
async def on_app_command_error(
    interaction: discord.Interaction, 
    error: app_commands.AppCommandError
) -> None:
    """Global error handler for application commands."""
    try:
        if isinstance(error, MissingPermissions):
            missing_perms = ', '.join(error.missing_perms)
            embed = discord.Embed(
                title="❌ Permission Error",
                description=f"You are missing the following permissions to execute this command:\n`{missing_perms}`",
                color=discord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.warning(f"Permission error for user {interaction.user}: {missing_perms}")
            
        elif isinstance(error, app_commands.CommandOnCooldown):
            embed = discord.Embed(
                title="⏰ Command on Cooldown",
                description=f"This command is on cooldown. Try again in {error.retry_after:.2f} seconds.",
                color=discord.Color.orange()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            
        else:
            embed = discord.Embed(
                title="❌ Error",
                description="An unexpected error occurred while processing the command. Please try again or contact support.",
                color=discord.Color.red()
            )
            
            # Try to respond if we haven't already
            if not interaction.response.is_done():
                await interaction.response.send_message(embed=embed, ephemeral=True)
            else:
                await interaction.followup.send(embed=embed, ephemeral=True)
                
            logger.error(f"Unhandled command error: {error}", exc_info=True)
            
    except Exception as e:
        logger.error(f"Error in error handler: {e}", exc_info=True)


async def main() -> None:
    """Main function to run the bot."""
    try:
        # Validate configuration
        if not BOT_TOKEN:
            logger.error("BOT_TOKEN not found in environment variables")
            sys.exit(1)
            
        # Initialize database
        initialize_database()
        
        # Start the bot
        logger.info("Starting Discord bot...")
        await client.start(BOT_TOKEN)
        
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)
    finally:
        # Cleanup
        if not client.is_closed():
            await client.close()
        logger.info("Bot shutdown complete")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested")
    except Exception as e:
        logger.error(f"Failed to start bot: {e}", exc_info=True)
        sys.exit(1)
