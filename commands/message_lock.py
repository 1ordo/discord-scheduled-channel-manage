from client import client
from resources.permissions import has_permissions
from discord import app_commands, Interaction, Embed, Color, utils, File
import discord 
from typing import Optional as op

@client.tree.command(name="lock_channel_for_others", description="Allows a specific role to view the current channel and optionally send DMs to the role members")
@has_permissions(manage_channels=True)
async def lock_channel_for_others(
        interaction: Interaction,
        role: op[discord.Role],
        channel:op[discord.TextChannel],
        dm_message: op[str] = None):
    await interaction.response.defer()
    channel = channel if channel else interaction.channel
    guild = interaction.guild 

    try:
        if role:
            await channel.set_permissions(role, read_messages=True, send_messages=True)
            if dm_message:
                members_with_role = [member for member in guild.members if role in member.roles]
                
                embed_dm = Embed(
                    title="Channel Access",
                    description=dm_message,
                    color=Color.blue()
                )
                if channel:
                    embed_dm.add_field(name="Channel:",value=channel.mention)
                for member in members_with_role:
                    try:
                        await member.send(embed=embed_dm)
                    except Exception as e:
                        print(f"Failed to send DM to {member}: {e}")
                        continue
        else:
            role = None
        overwrites = channel.overwrites

        
        for target, overwrite in overwrites.items():
            if isinstance(target, discord.Role) and target != role:
                
                if overwrite.read_messages is not None and overwrite.read_messages:
                    # Lock out the role (remove view permission)
                    await channel.set_permissions(target, read_messages=False)

        # Lock out the default role as well
        await channel.set_permissions(guild.default_role, read_messages=False)

        if role:
            embed = Embed(
                title="Channel Access Updated",
                description=f"Channel access updated: **{role.name}** can now view this channel.\nOther roles have been locked out.",
                color=Color.green()
            )
            if dm_message:
                embed.add_field(name="DM Sent", value=f"DMs have been sent to all members with the **{role.name}** role.")
                await channel.send(role.mention)
        else:
            embed = Embed(
                title="Channel lockdown Updated",
                description="Channel lockdown activated, no one can send in this/that channel anymore.")
            
        await interaction.followup.send(embed=embed)

    except Exception as e:
        await interaction.followup.send(f"An error occurred: {e}")
        print(e)