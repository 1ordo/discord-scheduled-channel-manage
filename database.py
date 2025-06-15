"""
Database management for the Discord Scheduled Channel Manager Bot.

This module handles all database operations including table creation,
channel creation configurations, and channel lock management.
"""

import logging
import sqlite3
from datetime import datetime
from typing import Any, List, Optional, Tuple

import pytz

from configuration import DATABASE_FILE, TIMEZONE

logger = logging.getLogger(__name__)


class Database:
    """
    Database handler for the Discord Scheduled Channel Manager Bot.

    Manages SQLite database operations for channel creation configurations
    and channel lock scheduling.
    """

    def __init__(self, db_name: str = DATABASE_FILE) -> None:
        """
        Initialize the database handler.

        Args:
            db_name: Name of the SQLite database file
        """
        self.db_name = db_name
        self.conn: Optional[sqlite3.Connection] = None
        self.c: Optional[sqlite3.Cursor] = None

    def connect(self) -> None:
        """Establish connection to the SQLite database."""
        try:
            self.conn = sqlite3.connect(self.db_name)
            self.c = self.conn.cursor()
            logger.debug(f"Connected to database: {self.db_name}")
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to database: {e}")
            raise e

    def create_table(self) -> None:
        """Create necessary database tables if they don't exist."""
        try:
            # Channel creation configurations table
            self.c.execute(
                """
            CREATE TABLE IF NOT EXISTS channel_creation (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                category_id INTEGER NOT NULL,
                daily_creation_time TEXT NOT NULL,
                close_after INTEGER,
                channel_name TEXT NOT NULL,
                channel_start_text TEXT,
                channel_role INTEGER,
                lock_after INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
            )

            # Channel lock scheduling table
            self.c.execute(
                """
            CREATE TABLE IF NOT EXISTS channel_lock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                guild_id INTEGER NOT NULL,
                channel_id INTEGER NOT NULL,
                creation_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                lock_in INTEGER NOT NULL,
                channel_role INTEGER,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE (guild_id, channel_id)
            )
            """
            )

            self.conn.commit()
            logger.info("Database tables created/verified successfully")

        except sqlite3.Error as e:
            logger.error(f"Failed to create database tables: {e}")
            raise e

    def add_channel_creation(
        self,
        guild_id: int,
        category_id: int,
        daily_creation_time: str,
        close_after: Optional[int],
        channel_name: str,
        channel_start_text: Optional[str],
        channel_role: Optional[int],
        lock_after: Optional[int],
    ) -> None:
        """
        Add a new channel creation configuration.

        Args:
            guild_id: Discord guild ID
            category_id: Discord category ID where channels will be created
            daily_creation_time: Time to create channel (HH:MM format)
            close_after: Minutes after which to delete the channel
            channel_name: Name for the created channel
            channel_start_text: Initial message to post in the channel
            channel_role: Role ID that gets access to the channel
            lock_after: Minutes after which to lock the channel
        """
        try:
            self.c.execute(
                """
            INSERT INTO channel_creation 
            (guild_id, category_id, daily_creation_time, close_after, 
             channel_name, channel_start_text, channel_role, lock_after)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
                (
                    guild_id,
                    category_id,
                    daily_creation_time,
                    close_after,
                    channel_name,
                    channel_start_text,
                    channel_role,
                    lock_after,
                ),
            )
            self.conn.commit()
            logger.info(f"Added channel creation config for guild {guild_id}")

        except sqlite3.Error as e:
            logger.error(f"Failed to add channel creation config: {e}")
            raise e

    def get_channel_creation(self, guild_id: int, id: int) -> Optional[Tuple[Any, ...]]:
        """
        Retrieve a specific channel creation configuration.

        Args:
            guild_id: Discord guild ID
            id: Configuration ID

        Returns:
            Channel creation configuration tuple or None
        """
        try:
            self.c.execute(
                "SELECT * FROM channel_creation WHERE guild_id = ? AND id = ?",
                (guild_id, id),
            )
            result = self.c.fetchone()
            logger.debug(f"Retrieved channel creation config {id} for guild {guild_id}")
            return result

        except sqlite3.Error as e:
            logger.error(f"Failed to get channel creation config: {e}")
            return None

    def get_all_channel_creations(self, guild_id: int) -> List[Tuple[Any, ...]]:
        """
        Get all channel creation configurations for a guild.

        Args:
            guild_id: Discord guild ID

        Returns:
            List of channel creation configuration tuples
        """
        try:
            self.c.execute(
                "SELECT * FROM channel_creation WHERE guild_id = ?", (guild_id,)
            )
            results = self.c.fetchall()
            logger.debug(
                f"Retrieved {len(results)} channel creation configs for guild {guild_id}"
            )
            return results

        except sqlite3.Error as e:
            logger.error(f"Failed to get all channel creation configs: {e}")
            return []

    def delete_channel_creation(self, id: int, guild_id: int) -> bool:
        """
        Delete a channel creation configuration.

        Args:
            id: Configuration ID
            guild_id: Discord guild ID

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            self.c.execute(
                "DELETE FROM channel_creation WHERE id = ? AND guild_id = ?",
                (id, guild_id),
            )
            self.conn.commit()

            if self.c.rowcount > 0:
                logger.info(
                    f"Deleted channel creation config {id} for guild {guild_id}"
                )
                return True
            else:
                logger.warning(
                    f"No channel creation config found with id {id} for guild {guild_id}"
                )
                return False

        except sqlite3.Error as e:
            logger.error(f"Failed to delete channel creation config: {e}")
            return False

    def get_channel_lock_by_guild(self, guild_id: int) -> List[Tuple[Any, ...]]:
        """
        Get all channel locks for a guild.

        Args:
            guild_id: Discord guild ID

        Returns:
            List of channel lock configuration tuples
        """
        try:
            self.c.execute("SELECT * FROM channel_lock WHERE guild_id = ?", (guild_id,))
            results = self.c.fetchall()
            logger.debug(f"Retrieved {len(results)} channel locks for guild {guild_id}")
            return results

        except sqlite3.Error as e:
            logger.error(f"Failed to get channel locks: {e}")
            return []

    def update_channel_lock(self, guild_id: int, channel_id: int, lock_in: int) -> bool:
        """
        Update an existing channel lock configuration.

        Args:
            guild_id: Discord guild ID
            channel_id: Discord channel ID
            lock_in: Minutes to wait before locking

        Returns:
            True if update was successful, False otherwise
        """
        try:
            self.c.execute(
                """
            UPDATE channel_lock SET lock_in = ? WHERE guild_id = ? AND channel_id = ?
            """,
                (lock_in, guild_id, channel_id),
            )
            self.conn.commit()

            if self.c.rowcount > 0:
                logger.info(
                    f"Updated channel lock for channel {channel_id} in guild {guild_id}"
                )
                return True
            else:
                logger.warning(
                    f"No channel lock found for channel {channel_id} in guild {guild_id}"
                )
                return False

        except sqlite3.Error as e:
            logger.error(f"Failed to update channel lock: {e}")
            return False

    def add_channel_lock(
        self, guild_id: int, channel_id: int, lock_in: int, channel_role: Optional[int]
    ) -> bool:
        """
        Add a new channel lock configuration.

        Args:
            guild_id: Discord guild ID
            channel_id: Discord channel ID
            lock_in: Minutes to wait before locking
            channel_role: Role ID that should be locked

        Returns:
            True if addition was successful, False otherwise
        """
        try:
            tz = pytz.timezone(TIMEZONE)
            creation_time = datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")

            self.c.execute(
                """
            INSERT OR REPLACE INTO channel_lock 
            (guild_id, channel_id, lock_in, channel_role, creation_time)
            VALUES (?, ?, ?, ?, ?)
            """,
                (guild_id, channel_id, lock_in, channel_role, creation_time),
            )

            self.conn.commit()
            logger.info(
                f"Added/updated channel lock for channel {channel_id} in guild {guild_id}"
            )
            return True

        except sqlite3.Error as e:
            logger.error(f"Failed to add channel lock: {e}")
            return False

    def get_all_channel_locks(self) -> List[Tuple[Any, ...]]:
        """
        Get all channel locks across all guilds.

        Returns:
            List of all channel lock configuration tuples
        """
        try:
            self.c.execute("SELECT * FROM channel_lock")
            results = self.c.fetchall()
            logger.debug(f"Retrieved {len(results)} total channel locks")
            return results

        except sqlite3.Error as e:
            logger.error(f"Failed to get all channel locks: {e}")
            return []

    def delete_channel_lock(self, guild_id: int, channel_id: int) -> bool:
        """
        Delete a channel lock configuration.

        Args:
            guild_id: Discord guild ID
            channel_id: Discord channel ID

        Returns:
            True if deletion was successful, False otherwise
        """
        try:
            self.c.execute(
                "DELETE FROM channel_lock WHERE guild_id = ? AND channel_id = ?",
                (guild_id, channel_id),
            )
            self.conn.commit()

            if self.c.rowcount > 0:
                logger.info(
                    f"Deleted channel lock for channel {channel_id} in guild {guild_id}"
                )
                return True
            else:
                logger.warning(
                    f"No channel lock found for channel {channel_id} in guild {guild_id}"
                )
                return False

        except sqlite3.Error as e:
            logger.error(f"Failed to delete channel lock: {e}")
            return False

    def close(self) -> None:
        """Close the database connection."""
        try:
            if self.conn:
                self.conn.close()
                self.conn = None
                self.c = None
                logger.debug("Database connection closed")

        except sqlite3.Error as e:
            logger.error(f"Error closing database connection: {e}")

    def __enter__(self):
        """Context manager entry."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.close()


# Global database instance
database = Database()
