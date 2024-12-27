from __future__ import annotations
from typing import (
    ClassVar,
    Union, 
    List
)

from discord.ext import commands

import discord
import sqlite3
import config

from core.ivy import Ivy
from core.managers.context import Context


class Server(commands.Cog):
    connection: ClassVar[sqlite3.Connection] = sqlite3.connect("sqlite3/server.db")
    cursor: ClassVar[sqlite3.Cursor] = connection.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS
        prefixes (
            server INTEGER,
            prefix TEXT,
            PRIMARY KEY (server)
        )
        '''
    )
#   cursor.execute(
#       '''
#       CREATE TABLE IF NOT EXISTS boosterroles (
#           user INTEGER,
#           server INTEGER,
#           role INTEGER,
#           PRIMARY KEY (user, server)
#       )
#       '''
#   )
    connection.commit()


    async def get_prefix(self, message: discord.Message) -> Union[List[str], str]:
        """
        Retrieves the guild prefix for a message
        """
        prefixes: List = []

        if message.guild:
            self.cursor.execute(
                '''
                SELECT prefix
                FROM prefixes
                WHERE server = ?
                ''',
                (
                    message.guild.id,
                )
            )
            guild_result = self.cursor.fetchone()
            if guild_result:
                prefixes.append(guild_result[0])

        if not prefixes:
            prefixes.append(config.Account.prefix)

        return prefixes


    @commands.group(
        name="prefix",
        brief="View guild prefix",
        invoke_without_command=True
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def prefix(self, context: Context) -> discord.Message:
        """
        View guild prefix
        """
        self.cursor.execute(
            '''
            SELECT prefix
            FROM prefixes
            WHERE server = ? 
            ''',
            (
                context.guild.id,
            )
        )
        self.connection.commit()

        result: str = self.cursor.fetchone()
        return await context.embed(f"Current prefix is `{result[0] if result else config.Account.prefix}`")


    @prefix.command(
        name="set",
        brief="Set a custom prefix",
        usage="(prefix)",
        example="!",
        aliases=[
            "change"
        ]
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def set(self, context: Context, prefix: str) -> discord.Message:
        """
        Set a custom prefix
        """
        self.cursor.execute(
            '''
            INSERT OR REPLACE INTO prefixes (
                server, 
                prefix
            ) 
            VALUES (?, ?)
            ''',
            (
                context.guild.id,
                prefix
            )
        )
        self.connection.commit()

        self.cursor.execute(
            '''
            SELECT prefix
            FROM prefixes
            WHERE server = ?
            ''',
            (
                context.guild.id,
            )
        )
        updated_prefix = self.cursor.fetchone()

        if updated_prefix and updated_prefix[0] == prefix:
            return await context.approve(f"Prefix successfully set to `{prefix}`")
        else:
            return await context.warn(f"Failed to update the **prefix**, please try again **later!**")


    @prefix.command(
        name="remove",
        brief="Remove the custom prefix",
        aliases=[
            "delete"
        ]
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_permissions(administrator=True)
    async def remove(self, context: Context) -> discord.Message:
        """
        Remove the custom prefix
        """
        self.cursor.execute(
            '''
            DELETE FROM prefixes
            WHERE server = ?
            ''',
            (
                context.guild.id,
            )
        )
        self.connection.commit()
        return await context.approve("The guild prefix has been removed!")


#   @commands.group(
#       name="boosterrole",
#       brief="Create your own booster role",
#       usage="(color) (name)",
#       example="#ffffff evie",
#       aliases=[
#           "br"
#       ],
#       invoke_without_command=True
#   )
#   @commands.cooldown(1, 4, commands.BucketType.user)
#   async def boosterrole(
#       self: Server, 
#       context: Context, 
#       color: str, *, 
#       name: str
#   ) -> discord.Message:
#       """
#       Create your own booster role
#       """
#       member: discord.Member = context.author
#       guild: discord.Guild = context.guild

#       if guild.premium_subscriber_role not in member.roles:
#           return await context.warn("Boost the server first!")

#       self.cursor.execute(
#           '''
#           SELECT role
#           FROM boosterroles
#           WHERE user = ? 
#           AND server = ?
#           ''',
#           (
#               member.id, 
#               guild.id
#           )
#       )
#       data = self.cursor.fetchone()
#       if data:
#           return await context.warn("You already have a booster role!")

#       try:
#           color = discord.Color(
#               int(
#                   color.strip('#'), 
#                   16
#               )
#           )

#       except ValueError:
#           return await context.warn(
#               "Invalid **color**! Use a valid hex code (e.g., `#ffffff`)"
#           )

#       role: discord.Role = await guild.create_role(
#           name=name, 
#           color=color, 
#           mentionable=True
#       )
#       await member.add_roles(role)
#       self.cursor.execute(
#           '''
#           INSERT INTO boosterroles (
#               user, 
#               server, 
#               role
#           )
#           VALUES (?, ?, ?)
#           ''',
#           (
#               member.id,
#               guild.id, 
#               role.id
#           )
#       )
#       self.connection.commit()
#       return await context.approve(f"Your booster role {role.mention} has been **created**")


#   @boosterrole.command(
#       name="remove",
#       brief="Remove your custom booster role",
#   )
#   @commands.cooldown(1, 4, commands.BucketType.user)
#   async def remove(self, context: Context) -> discord.Message:
#       """
#       Remove your custom booster role
#       """
#       member = context.author
#       guild = context.guild

#       self.cursor.execute(
#           '''
#           SELECT role
#           FROM boosterroles
#           WHERE user = ? 
#           AND server = ?
#           ''',
#           (
#               member.id, 
#               guild.id
#           )
#       )
#       data = self.cursor.fetchone()
#       if not data:
#           return await context.warn("You don't have a booster role to **remove**")

#       _role = data[0]
#       role = guild.get_role(_role)

#       if role:
#           await role.delete(reason="Booster role removed by user")

#           self.cursor.execute(
#               '''
#               DELETE FROM boosterroles
#               WHERE user = ? 
#               AND server = ?
#               ''',
#               (
#                   member.id,
#                   guild.id
#               )
#           )
#           self.connection.commit()
#           return await context.approve("Your booster role has been **removed**")


#   @boosterrole.command(
#       name="cleanup",
#       brief="Clean up unused booster roles"
#   )
#   @commands.cooldown(1, 4, commands.BucketType.guild)
#   @commands.has_permissions(manage_guild=True)
#   async def cleanup(self, context: Context) -> discord.Message:
#       """
#       Clean up unused booster roles
#       """
#       guild: discord.Guild = context.guild

#       self.cursor.execute(
#           '''
#           SELECT user, role
#           FROM boosterroles
#           WHERE server = ?
#           ''',
#           (
#               guild.id,
#           )
#       )
#       roles = self.cursor.fetchall()

#       count: int = 0
#       for user, role in roles:
#           role = guild.get_role(role)
#           if not role:
#               self.cursor.execute(
#                   '''
#                   DELETE FROM boosterroles
#                   WHERE user = ? 
#                   AND server = ?
#                   ''',
#                   (
#                       user, 
#                       guild.id
#                   )
#               )
#               count += 1

#       self.connection.commit()
#       return await context.approve(f"Cleaned up **{count}** unused booster roles")


async def setup(bot: Ivy):
    return await bot.add_cog(Server(bot))