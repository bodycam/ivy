from __future__ import annotations
from typing import List

from discord.ext import commands

import discord
import inspect
import config

from core.ivy import Ivy
from core.managers.context import Context


class Developer(commands.Cog):
    bot: Ivy = Ivy()

    async def cog_check(self: Developer, context: Context) -> bool:
        return context.author.id in config.Account.developers


    @commands.group(
        name="cog",
        brief="Manage cogs",
        usage="(arguments)",
        example="reload moderation",
        aliases=[
            "feature"
        ],
        invoke_without_command=True
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def cog(self, context: Context) -> discord.Message:
        """
        Manage cogs
        """
        return await context.send_help()


    @cog.command(
        name="load",
        brief="Load a cog",
        usage="(cog)",
        example="moderation",
        aliases=[
            "loadup"
        ]
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def load(self, context: Context, name: str) -> discord.Message:
        """
        Load a cog
        """
        await self.bot.load_extension(f"core.features.{name}")
        return await context.approve(f"Loaded the **{name}** feature!")


    @cog.command(
        name="reload",
        brief="Reload a cog",
        usage="(cog)",
        example="moderation"
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def reload(self, context: Context, name: str) -> discord.Message:
        """
        Reload a cog
        """
        await self.bot.reload_extension(f"core.features.{name}")
        return await context.approve(f"Reloaded the **{name}** feature!")


    @cog.command(
        name="unload",
        brief="Unload a cog",
        usage="(cog)",
        example="moderation"
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    async def unload(self, context: Context, name: str) -> discord.Message:
        """
        Unload a cog
        """
        await self.bot.unload_extension(f"core.features.{name}")
        return await context.approve(f"Unloaded the **{name}** feature!")


async def setup(bot: Ivy):
    return await bot.add_cog(Developer(bot))