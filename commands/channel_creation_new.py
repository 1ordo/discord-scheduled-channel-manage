"""
Channel creation commands for the Discord Scheduled Channel Manager Bot.

This module provides slash commands for managing scheduled channel creation,
deletion, and configuration display.
"""

import logging
import re
from datetime import datetime
from typing import Optional

import discord
from discord import Color, Embed, Interaction, app_commands

from client import client
from configuration import TIMEZONE
from database import database
from resources.permissions import has_permissions

logger = logging.getLogger(__name__)


def convert_to_minutes(time_str: str) -> Optional[int]:
    """
    Convert time string to minutes.

    Args:
        time_str: Time string in format like "2h 30m", "90m", "1h"

    Returns:
        Total minutes as integer, or None if invalid format

    Examples:
        "2h 30m" -> 150
        "90m" -> 90
        "1h" -> 60
    """
    if not time_str:
        return 0

    pattern = r"(?:(\d+)h)?\s*(?:(\d+)m)?"
    match = re.match(pattern, time_str.lower().strip())

    if not match or not any(match.groups()):
        return None

    hours = int(match.group(1)) if match.group(1) else 0
    minutes = int(match.group(2)) if match.group(2) else 0
    return hours * 60 + minutes


def validate_time_format(time_str: str) -> Optional[str]:
    """
    Validate and convert AM/PM time to 24-hour format.

    Args:
        time_str: Time string in 12-hour format (e.g., "2:30 PM")

    Returns:
        Time in 24-hour format (HH:MM) or None if invalid
    """
    if not time_str:
        return None

    try:
        parsed_time = datetime.strptime(time_str.strip(), "%I:%M %p")
        return parsed_time.strftime("%H:%M")
    except ValueError:
        try:
            # Try without AM/PM for 24-hour format
            parsed_time = datetime.strptime(time_str.strip(), "%H:%M")
            return parsed_time.strftime("%H:%M")
        except ValueError:
            return None


@client.tree.command(
    name="scheduled_channel_create",
    description="Create, show, or remove scheduled channel configurations",
)
@has_permissions(manage_guild=True)
@app_commands.choices(
    action=[
        app_commands.Choice(name="Set", value=1),
        app_commands.Choice(name="Remove", value=2),
        app_commands.Choice(name="Show", value=3),
    ]
)
async def scheduled_channel_create(
    interaction: Interaction,
    action: int,
    category: Optional[discord.CategoryChannel] = None,
    daily_time: Optional[str] = None,
    delete_after: Optional[str] = None,
    lock_after: Optional[str] = None,
    channel_name: Optional[str] = None,
    channel_text: Optional[str] = None,
    channel_role: Optional[discord.Role] = None,
    id: Optional[int] = None,
) -> None:
    """
    Main command for managing scheduled channel creation.

    Args:
        interaction: Discord interaction object
        action: Action to perform (1=Set, 2=Remove, 3=Show)
        category: Category where channels will be created
        daily_time: Time to create channels (12-hour format)
        delete_after: Time before deletion (e.g., "2h 30m")
        lock_after: Time before locking (e.g., "1h")
        channel_name: Name for created channels
        channel_text: Initial message for channels
        channel_role: Role that gets access
        id: Configuration ID for removal
    """
    guild_id = interaction.guild.id

    try:
        database.connect()

        if action == 1:  # Set configuration
            await handle_set_action(
                interaction,
                guild_id,
                category,
                daily_time,
                delete_after,
                lock_after,
                channel_name,
                channel_text,
                channel_role,
            )
        elif action == 2:  # Remove configuration
            await handle_remove_action(interaction, guild_id, id)
        elif action == 3:  # Show configurations
            await handle_show_action(interaction, guild_id)

    except Exception as e:
        logger.error(f"Error in scheduled_channel_create command: {e}", exc_info=True)

        error_embed = Embed(
            title="❌ Error",
            description="An error occurred while processing your request. Please try again.",
            color=Color.red(),
        )

        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    embed=error_embed, ephemeral=True
                )
            else:
                await interaction.followup.send(embed=error_embed, ephemeral=True)
        except:
            pass
    finally:
        database.close()


async def handle_set_action(
    interaction: Interaction,
    guild_id: int,
    category: Optional[discord.CategoryChannel],
    daily_time: Optional[str],
    delete_after: Optional[str],
    lock_after: Optional[str],
    channel_name: Optional[str],
    channel_text: Optional[str],
    channel_role: Optional[discord.Role],
) -> None:
    """Handle the 'Set' action for creating a new configuration."""
    # Validate required parameters
    if not all([category, daily_time, channel_name, channel_text]):
        await interaction.response.send_message(
            "❌ **Missing Required Fields**\n"
            "For 'Set' action, you must provide: `category`, `daily_time`, `channel_name`, and `channel_text`.",
            ephemeral=True,
        )
        return

    # Validate time format
    daily_time_24hr = validate_time_format(daily_time)
    if not daily_time_24hr:
        await interaction.response.send_message(
            "❌ **Invalid Time Format**\n"
            "Please provide time in 12-hour format (e.g., `3:00 PM`) or 24-hour format (e.g., `15:00`).",
            ephemeral=True,
        )
        return

    # Validate delete_after duration
    close_after_minutes = convert_to_minutes(delete_after) if delete_after else 0
    if close_after_minutes is None:
        await interaction.response.send_message(
            "❌ **Invalid Delete Duration**\n"
            "Please use format like `2h 30m`, `90m`, or `1h`.",
            ephemeral=True,
        )
        return

    # Validate lock_after duration
    lock_after_minutes = convert_to_minutes(lock_after) if lock_after else 0
    if lock_after_minutes is None:
        await interaction.response.send_message(
            "❌ **Invalid Lock Duration**\n"
            "Please use format like `2h 30m`, `90m`, or `1h`.",
            ephemeral=True,
        )
        return

    # Add configuration to database
    database.add_channel_creation(
        guild_id,
        category.id,
        daily_time_24hr,
        close_after_minutes,
        channel_name,
        channel_text,
        channel_role.id if channel_role else None,
        lock_after_minutes,
    )

    # Create success embed
    embed = Embed(
        title="✅ Scheduled Channel Creation Set",
        description=f"Successfully configured scheduled channel creation for **{channel_name}**",
        color=Color.green(),
    )

    embed.add_field(
        name="📋 Configuration Details",
        value=(
            f"**Category:** {category.mention}\n"
            f"**Daily Time:** {daily_time} ({daily_time_24hr} {TIMEZONE})\n"
            f"**Channel Name:** {channel_name}\n"
            f"**Initial Message:** {channel_text[:100]}{'...' if len(channel_text) > 100 else ''}\n"
            f"**Role Access:** {channel_role.mention if channel_role else 'None'}\n"
            f"**Delete After:** {format_duration(close_after_minutes)}\n"
            f"**Lock After:** {format_duration(lock_after_minutes)}"
        ),
        inline=False,
    )

    embed.set_footer(text=f"Timezone: {TIMEZONE}")
    await interaction.response.send_message(embed=embed)


async def handle_remove_action(
    interaction: Interaction, guild_id: int, config_id: Optional[int]
) -> None:
    """Handle the 'Remove' action for deleting a configuration."""
    if not config_id:
        await interaction.response.send_message(
            "❌ **Missing Configuration ID**\n"
            "You must provide the `id` parameter to remove a configuration.\n"
            "Use the 'Show' action to see all configuration IDs.",
            ephemeral=True,
        )
        return

    # Check if configuration exists
    config = database.get_channel_creation(guild_id, config_id)
    if not config:
        await interaction.response.send_message(
            f"❌ **Configuration Not Found**\n"
            f"No configuration found with ID `{config_id}` in this server.",
            ephemeral=True,
        )
        return

    # Remove configuration
    success = database.delete_channel_creation(config_id, guild_id)
    if success:
        embed = Embed(
            title="✅ Configuration Removed",
            description=f"Successfully removed scheduled channel configuration with ID `{config_id}`",
            color=Color.green(),
        )
        embed.add_field(
            name="Removed Configuration",
            value=f"**Channel Name:** {config[5]}\n**Daily Time:** {config[3]}",
            inline=False,
        )
    else:
        embed = Embed(
            title="❌ Removal Failed",
            description="Failed to remove the configuration. Please try again.",
            color=Color.red(),
        )

    await interaction.response.send_message(embed=embed)


async def handle_show_action(interaction: Interaction, guild_id: int) -> None:
    """Handle the 'Show' action for displaying all configurations."""
    configs = database.get_all_channel_creations(guild_id)

    if not configs:
        embed = Embed(
            title="📋 Scheduled Channel Configurations",
            description="No scheduled channel configurations found for this server.",
            color=Color.blue(),
        )
        embed.add_field(
            name="Getting Started",
            value="Use the 'Set' action to create your first scheduled channel configuration!",
            inline=False,
        )
        await interaction.response.send_message(embed=embed)
        return

    embed = Embed(
        title="📋 Scheduled Channel Configurations",
        description=f"Found {len(configs)} configuration(s) for this server:",
        color=Color.blue(),
    )

    for i, config in enumerate(configs[:10]):  # Limit to 10 to avoid embed limits
        try:
            (
                config_id,
                guild_id,
                category_id,
                daily_creation_time,
                close_after_minutes,
                channel_name,
                channel_text,
                channel_role,
                lock_after_minutes,
                created_at,
            ) = config
        except ValueError:
            # Handle older database format without created_at
            (
                config_id,
                guild_id,
                category_id,
                daily_creation_time,
                close_after_minutes,
                channel_name,
                channel_text,
                channel_role,
                lock_after_minutes,
            ) = config

        category_mention = f"<#{category_id}>"
        role_mention = f"<@&{channel_role}>" if channel_role else "None"

        field_value = (
            f"**ID:** {config_id}\n"
            f"**Category:** {category_mention}\n"
            f"**Daily Time:** {daily_creation_time} {TIMEZONE}\n"
            f"**Role Access:** {role_mention}\n"
            f"**Delete After:** {format_duration(close_after_minutes)}\n"
            f"**Lock After:** {format_duration(lock_after_minutes)}"
        )

        embed.add_field(name=f"🔹 {channel_name}", value=field_value, inline=True)

    if len(configs) > 10:
        embed.set_footer(
            text=f"Showing 10 of {len(configs)} configurations. Use pagination for more."
        )
    else:
        embed.set_footer(text=f"Timezone: {TIMEZONE}")

    await interaction.response.send_message(embed=embed)


def format_duration(minutes: int) -> str:
    """
    Format duration in minutes to a human-readable string.

    Args:
        minutes: Duration in minutes

    Returns:
        Formatted duration string
    """
    if minutes == 0:
        return "Never"

    hours, mins = divmod(minutes, 60)
    if hours > 0 and mins > 0:
        return f"{hours}h {mins}m"
    elif hours > 0:
        return f"{hours}h"
    else:
        return f"{mins}m"
