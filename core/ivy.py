"""
Open source multi-purpose bot, built on discord.py
"""
from __future__ import annotations
from typing import (
    List, 
    Any, 
    Tuple,
    Optional,
    Union
)

from discord.ext import commands
from pathlib import Path

import discord
import config
import asyncio

from core.managers.context import Context

__all__: Tuple[str, ...] = ("Ivy",)

class Ivy(commands.Bot):
    """
    Open source multi-purpose bot, built on discord.py
    """
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(
            *args,
            **kwargs,
            intents=discord.Intents.all(),
            command_prefix=self.sync_get_prefix,
            help_command=None,
        )

    @property
    def features(self) -> List[str]:
        return [
            str(feature.with_suffix("")).replace("\\", ".").replace("/", ".")
            for feature in Path("./core/features").glob("**/[!__]*.py")
        ]

    async def get_prefix(self, message: discord.Message) -> Union[List[str], str]:
        """
        Retrieves the prefix for a guild from the Server cog
        """
        cog: Optional[commands.Cog] = self.get_cog("Server")
        return await cog.get_prefix(message) #type: ignore
    
    def sync_get_prefix(self, bot: commands.Bot, message: discord.Message) -> Union[List[str], str]:
        # "bot" is not accessed, but it's needed for `command_prefix=self.sync_get_prefix`
        # because the type checker is overly strict and requires compatibility 
        # with synchronous callable signatures for `command_prefix`
        return asyncio.run_coroutine_threadsafe(self.get_prefix(message), self.loop).result()

    async def get_context(self, message: discord.Message, *, cls=Context) -> commands.context.Context:
        return await super().get_context(message, cls=cls)

    async def setup_hook(self) -> None:
        await asyncio.gather(
            *(
                self.load_extension(feature)
                for feature 
                in self.features
            )
        )

    async def on_command_error(self, context: Context, error: Any) -> Optional[discord.Message]:
        """
        Handles errors raised during command execution
        """
        if isinstance(
            error, 
            (
                commands.MissingRequiredArgument,
                commands.MissingFlagArgument,
                commands.MissingRequiredAttachment,
                commands.MissingRequiredFlag
            )
        ):
            return await context.send_help()

        elif isinstance(error, commands.CommandOnCooldown):
            return await context.embed(
                f"You are on **cooldown!** Please wait **{error.retry_after:.2f}** seconds!",
                emoji="<:cooldown:1320600555420258314>",
                color=0x76C5F6,
                delete_after=5
            )

        elif isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.CommandError):
            return await context.warn(f"{str(error).strip('.')}")


    def run(self) -> None:
        super().run(config.Account.token)