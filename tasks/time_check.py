"""
Scheduled channel management tasks for the Discord Scheduled Channel Manager Bot.

This module handles the periodic checking and management of scheduled channels,
including creation, deletion, and locking based on time configurations.
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any

import discord
import pytz
from discord.ext import tasks

from client import client
from configuration import TIMEZONE, TASK_INTERVAL_MINUTES
from database import database

logger = logging.getLogger(__name__)

# File for storing temporary channel deletion data
CHANNEL_DELETE_FILE = 'channel_delete.json'


def load_channel_data() -> Dict[str, Any]:
    """
    Load channel deletion data from JSON file.
    
    Returns:
        Dictionary containing channel deletion schedule data
    """
    if os.path.exists(CHANNEL_DELETE_FILE):
        try:
            with open(CHANNEL_DELETE_FILE, 'r') as file:
                data = json.load(file)
                logger.debug(f"Loaded channel data from {CHANNEL_DELETE_FILE}")
                return data
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Failed to load channel data: {e}")
            return {}
    return {}


def save_channel_data(channel_data: Dict[str, Any]) -> None:
    """
    Save channel deletion data to JSON file.
    
    Args:
        channel_data: Dictionary containing channel deletion schedule data
    """
    try:
        with open(CHANNEL_DELETE_FILE, 'w') as file:
            json.dump(channel_data, file, indent=4)
            logger.debug(f"Saved channel data to {CHANNEL_DELETE_FILE}")
    except IOError as e:
        logger.error(f"Failed to save channel data: {e}")


# Global channel data storage
channel_data = load_channel_data()

@tasks.loop(minutes=TASK_INTERVAL_MINUTES)
async def scheduled_channel_management_task() -> None:
    """
    Main scheduled task that runs periodically to manage channels.
    
    This task checks for:
    - Channels that need to be created
    - Channels that need to be deleted
    - Channels that need to be locked
    """
    try:
        now = datetime.now(pytz.timezone(TIMEZONE))
        
        time_str = now.strftime("%H:%M")
        time_str_12h = now.strftime("%I:%M %p %Z")
        logger.info(f"Running scheduled task - Current time: {time_str} {TIMEZONE} ({time_str_12h})")

        for guild in client.guilds:
            try:
                guild_id = guild.id
                logger.debug(f"Processing guild: {guild.name} (ID: {guild_id})")
                
                # Connect to database for this guild's operations
                database.connect()

                # Get all channel creation configurations for this guild
                channels = database.get_all_channel_creations(guild_id)
                
                # Process scheduled channel operations
                await create_channels_if_scheduled(guild, channels, now)
                await delete_expired_channels(guild, now)
                await check_and_lock_channels(guild, now)

                database.close()

            except Exception as e:
                logger.error(f"Error processing guild {guild.name} (ID: {guild_id}): {e}", exc_info=True)
                continue
                
        logger.info("Scheduled task completed")
        print("=" * 80)

    except Exception as e:
        logger.error(f"Unexpected error in scheduled task: {e}", exc_info=True)

async def create_channels_if_scheduled(
    guild: discord.Guild, 
    channels: List[tuple], 
    now: datetime
) -> None:
    """
    Create channels if they are scheduled for the current time.
    
    Args:
        guild: Discord guild to create channels in
        channels: List of channel configuration tuples from database
        now: Current datetime
    """
    for channel_config in channels:
        try:
            # Unpack channel configuration
            (config_id, guild_id, category_id, daily_creation_time, 
             close_after_minutes, channel_name, channel_text, 
             channel_role, lock_after_minutes, created_at) = channel_config
            
            # Check if it's time to create the channel
            if daily_creation_time == now.strftime("%H:%M"):
                logger.info(f"Creating scheduled channel '{channel_name}' in guild {guild.name}")
                
                # Get the category
                category = discord.utils.get(guild.categories, id=category_id)
                if not category:
                    logger.error(f"Category {category_id} not found in guild {guild.name}")
                    continue

                # Set up permissions (hidden by default)
                overwrites = {
                    guild.default_role: discord.PermissionOverwrite(view_channel=False)
                }
                
                # Create the channel
                created_channel = await category.create_text_channel(
                    name=channel_name,
                    topic=channel_text,
                    overwrites=overwrites
                )

                # Send initial message
                if channel_text:
                    await created_channel.send(f"{channel_text}")
                
                # Handle role permissions
                if channel_role:
                    await _handle_role_permissions(guild, created_channel, channel_role, channel_text)
                
                logger.info(f"✅ Created channel '{created_channel.name}' in guild {guild.name}")
                
                # Schedule channel deletion if specified
                if close_after_minutes and close_after_minutes > 0:
                    await _schedule_channel_deletion(
                        guild, created_channel, daily_creation_time, 
                        close_after_minutes, now
                    )
                
                # Schedule channel locking if specified
                if lock_after_minutes and lock_after_minutes > 0:
                    database.add_channel_lock(
                        guild.id, created_channel.id, 
                        lock_after_minutes, channel_role
                    )
                    logger.info(f"🔒 Scheduled lock for channel '{created_channel.name}' after {lock_after_minutes} minutes")
                    
        except Exception as e:
            logger.error(f"Error creating scheduled channel: {e}", exc_info=True)
            continue


async def _handle_role_permissions(
    guild: discord.Guild, 
    channel: discord.TextChannel, 
    channel_role: int, 
    channel_text: str
) -> None:
    """
    Handle role-based permissions for a channel.
    
    Args:
        guild: Discord guild
        channel: Created channel
        channel_role: Role ID to grant access
        channel_text: Text to send in DM notifications
    """
    try:
        role = guild.get_role(channel_role)
        if not role:
            logger.warning(f"Role {channel_role} not found in guild {guild.name}")
            return
            
        # Grant role access to the channel
        await channel.set_permissions(
            role, 
            view_channel=True, 
            read_messages=True
        )
        logger.info(f"✅ Granted access to role '{role.name}' for channel '{channel.name}'")
        
        # Send DM notifications to role members
        if channel_text:
            await _send_dm_notifications(guild, role, channel, channel_text)
            
    except Exception as e:
        logger.error(f"Error handling role permissions: {e}", exc_info=True)


async def _send_dm_notifications(
    guild: discord.Guild, 
    role: discord.Role, 
    channel: discord.TextChannel, 
    channel_text: str
) -> None:
    """
    Send DM notifications to members with a specific role.
    
    Args:
        guild: Discord guild
        role: Role whose members to notify
        channel: Channel that was created
        channel_text: Message text
    """
    try:
        members_with_role = [member for member in guild.members if role in member.roles]
        
        embed_dm = discord.Embed(
            title="📢 Channel Access",
            description=channel_text,
            color=discord.Color.blue()
        )
        embed_dm.add_field(name="Channel:", value=channel.mention, inline=False)
        embed_dm.set_footer(text=f"Guild: {guild.name}")
        
        success_count = 0
        for member in members_with_role:
            try:
                await member.send(embed=embed_dm)
                success_count += 1
            except (discord.Forbidden, discord.HTTPException) as e:
                logger.debug(f"Failed to send DM to {member}: {e}")
                continue
                
        logger.info(f"📧 Sent DM notifications to {success_count}/{len(members_with_role)} members")
        
    except Exception as e:
        logger.error(f"Error sending DM notifications: {e}", exc_info=True)


async def _schedule_channel_deletion(
    guild: discord.Guild, 
    channel: discord.TextChannel, 
    creation_time_str: str, 
    close_after_minutes: int, 
    now: datetime
) -> None:
    """
    Schedule a channel for deletion.
    
    Args:
        guild: Discord guild
        channel: Channel to schedule for deletion
        creation_time_str: Time when channel was created (HH:MM format)
        close_after_minutes: Minutes to wait before deletion
        now: Current datetime
    """
    try:
        creation_time = datetime.strptime(creation_time_str, "%H:%M").time()
        creation_datetime = datetime.combine(now.date(), creation_time)
        creation_datetime = pytz.timezone(TIMEZONE).localize(creation_datetime)
        expiration_time = creation_datetime + timedelta(minutes=close_after_minutes)
        
        expiration_time_str = expiration_time.strftime("%H:%M")
        
        global channel_data
        if str(guild.id) not in channel_data:
            channel_data[str(guild.id)] = {}
        channel_data[str(guild.id)][str(channel.id)] = expiration_time_str
        save_channel_data(channel_data)
        
        logger.info(f"🗑️ Scheduled deletion for channel '{channel.name}' at {expiration_time_str}")
        
    except Exception as e:
        logger.error(f"Error scheduling channel deletion: {e}", exc_info=True)
        
async def delete_expired_channels(guild: discord.Guild, now: datetime) -> None:
    """
    Delete channels that have reached their expiration time.
    
    Args:
        guild: Discord guild to check for expired channels
        now: Current datetime
    """
    global channel_data 

    try:
        now_time_only = now.strftime("%H:%M")
        guild_id_str = str(guild.id)

        if guild_id_str in channel_data:
            # Create a copy of items to avoid modification during iteration
            channels_to_check = list(channel_data[guild_id_str].items())
            
            for channel_id_str, expiration_time_str in channels_to_check:
                try:
                    if now_time_only == expiration_time_str:
                        channel_id = int(channel_id_str)
                        channel = guild.get_channel(channel_id)
                        
                        if channel:
                            await channel.delete(reason="Scheduled deletion")
                            logger.info(f"🗑️ Deleted expired channel '{channel.name}' in guild {guild.name}")
                        else:
                            logger.warning(f"Channel {channel_id} not found for deletion in guild {guild.name}")

                        # Remove channel from tracking
                        del channel_data[guild_id_str][channel_id_str]
                        save_channel_data(channel_data)
                        
                except Exception as e:
                    logger.error(f"Error deleting expired channel {channel_id_str}: {e}", exc_info=True)
                    continue
                    
    except Exception as e:
        logger.error(f"Error processing expired channels for guild {guild.name}: {e}", exc_info=True)


async def check_and_lock_channels(guild: discord.Guild, now: datetime) -> None:
    """
    Check for and lock channels that have reached their lock time.
    
    Args:
        guild: Discord guild to check for channels to lock
        now: Current datetime
    """
    try:
        channel_locks = database.get_channel_lock_by_guild(guild.id)
        
        for lock_config in channel_locks:
            try:
                (lock_id, guild_id, channel_id, creation_time, 
                 lock_in, channel_role, created_at) = lock_config

                # Parse creation time
                creation_datetime = datetime.strptime(creation_time, "%Y-%m-%d %H:%M:%S")
                lock_time = creation_datetime + timedelta(minutes=lock_in)

                now_str = now.strftime("%H:%M")
                lock_time_str = lock_time.strftime("%H:%M")
                
                logger.debug(f"Checking lock: current={now_str}, lock_time={lock_time_str}")
                
                if now_str == lock_time_str:
                    channel = guild.get_channel(channel_id)
                    if not channel:
                        logger.warning(f"Channel {channel_id} not found for locking in guild {guild.name}")
                        # Clean up the lock record
                        database.delete_channel_lock(guild.id, channel_id)
                        continue

                    await _lock_channel_permissions(guild, channel, channel_role)
                    
                    # Remove the lock configuration from database
                    database.delete_channel_lock(guild.id, channel_id)
                    logger.info(f"🔒 Locked and removed lock config for channel '{channel.name}' in guild {guild.name}")
                    
            except Exception as e:
                logger.error(f"Error processing channel lock: {e}", exc_info=True)
                continue
                
    except Exception as e:
        logger.error(f"Error checking channel locks for guild {guild.name}: {e}", exc_info=True)


async def _lock_channel_permissions(
    guild: discord.Guild, 
    channel: discord.TextChannel, 
    channel_role: int
) -> None:
    """
    Lock all permissions for a channel.
    
    Args:
        guild: Discord guild
        channel: Channel to lock
        channel_role: Role that should also be locked
    """
    try:
        # Lock all existing overwrites
        overwrites = channel.overwrites.copy()
        
        for target, overwrite in overwrites.items():
            new_overwrite = discord.PermissionOverwrite.from_pair(
                overwrite.pair()[0], 
                overwrite.pair()[1]
            )
            new_overwrite.read_messages = False
            new_overwrite.view_channel = False
            await channel.set_permissions(target, overwrite=new_overwrite)

        # Ensure the specific role is also locked
        if channel_role:
            role = guild.get_role(channel_role)
            if role:
                await channel.set_permissions(
                    role, 
                    read_messages=False, 
                    view_channel=False
                )
                logger.info(f"🔒 Locked access for role '{role.name}' in channel '{channel.name}'")

        logger.info(f"🔒 Locked all permissions in channel '{channel.name}' in guild {guild.name}")
        
    except Exception as e:
        logger.error(f"Error locking channel permissions: {e}", exc_info=True)