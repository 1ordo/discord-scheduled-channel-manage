"""
Discord client configuration and setup.

This module contains the Discord client setup with proper intents
and command tree configuration for the scheduled channel manager bot.
"""

import discord
from discord import Client, Intents, app_commands


class ScheduledChannelBot(Client):
    """
    Custom Discord client for the Scheduled Channel Manager Bot.

    This client extends the base Discord.py client with a command tree
    for slash commands and proper intent configuration.
    """

    def __init__(self, *, intents: Intents) -> None:
        """
        Initialize the bot client.

        Args:
            intents: Discord intents configuration
        """
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self) -> None:
        """
        Setup hook called when the bot is starting up.

        This can be used for any initialization that needs to happen
        after the bot is logged in but before it's fully ready.
        """
        # This is called when the bot starts up
        # You can add any initialization code here if needed
        pass


# Configure intents
intents = discord.Intents.default()
intents.message_content = True  # Required for reading message content
intents.guilds = True  # Required for guild operations
intents.guild_messages = True  # Required for message operations

# Create the bot client instance
client = ScheduledChannelBot(intents=intents)
