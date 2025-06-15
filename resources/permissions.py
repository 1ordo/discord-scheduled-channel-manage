"""
Permission decorators and utilities for Discord commands.

This module provides permission checking decorators to ensure users
have the required permissions before executing commands.
"""

import logging
from typing import Any, Callable, List

import discord
from discord import app_commands

logger = logging.getLogger(__name__)


class MissingPermissions(app_commands.AppCommandError):
    """
    Exception raised when a user lacks required permissions.

    Attributes:
        missing_perms: List of permission names the user is missing
    """

    def __init__(self, missing_perms: List[str]) -> None:
        """
        Initialize the exception.

        Args:
            missing_perms: List of missing permission names
        """
        self.missing_perms = missing_perms
        super().__init__(f"Missing permissions: {', '.join(missing_perms)}")


def has_permissions(**perms: bool) -> Callable[[Any], Any]:
    """
    Decorator to check if a user has required permissions.

    Args:
        **perms: Keyword arguments of permission names and required values

    Returns:
        Decorator function that checks permissions

    Example:
        @has_permissions(manage_guild=True, manage_channels=True)
        async def my_command(interaction):
            pass
    """

    def predicate(interaction: discord.Interaction) -> bool:
        """
        Check if the user has the required permissions.

        Args:
            interaction: Discord interaction object

        Returns:
            True if user has permissions

        Raises:
            MissingPermissions: If user lacks required permissions
        """
        user = interaction.user

        # Administrators bypass all permission checks
        if user.guild_permissions.administrator:
            logger.debug(f"User {user} has administrator permissions")
            return True

        # Check each required permission
        missing_perms = []
        for perm, required_value in perms.items():
            user_has_perm = getattr(user.guild_permissions, perm, False)
            if user_has_perm != required_value:
                missing_perms.append(perm)

        if missing_perms:
            logger.warning(f"User {user} missing permissions: {missing_perms}")
            raise MissingPermissions(missing_perms)

        logger.debug(f"User {user} has required permissions: {list(perms.keys())}")
        return True

    return app_commands.check(predicate)


def is_guild_owner() -> Callable[[Any], Any]:
    """
    Decorator to check if the user is the guild owner.

    Returns:
        Decorator function that checks guild ownership
    """

    def predicate(interaction: discord.Interaction) -> bool:
        """
        Check if the user is the guild owner.

        Args:
            interaction: Discord interaction object

        Returns:
            True if user is guild owner

        Raises:
            MissingPermissions: If user is not the guild owner
        """
        if interaction.user.id == interaction.guild.owner_id:
            logger.debug(f"User {interaction.user} is guild owner")
            return True

        logger.warning(f"User {interaction.user} is not guild owner")
        raise MissingPermissions(["guild_owner"])

    return app_commands.check(predicate)


def has_any_role(*role_names: str) -> Callable[[Any], Any]:
    """
    Decorator to check if user has any of the specified roles.

    Args:
        *role_names: Role names to check for

    Returns:
        Decorator function that checks role membership
    """

    def predicate(interaction: discord.Interaction) -> bool:
        """
        Check if the user has any of the specified roles.

        Args:
            interaction: Discord interaction object

        Returns:
            True if user has at least one of the required roles

        Raises:
            MissingPermissions: If user lacks all specified roles
        """
        user_roles = [role.name for role in interaction.user.roles]

        if any(role_name in user_roles for role_name in role_names):
            logger.debug(f"User {interaction.user} has required role")
            return True

        logger.warning(f"User {interaction.user} missing roles: {role_names}")
        raise MissingPermissions([f"role:{role}" for role in role_names])

    return app_commands.check(predicate)
