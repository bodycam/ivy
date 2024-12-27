"""
Custom context for Ivy
"""
from __future__ import annotations
from typing import (
    Optional,
    Any
)

import discord
import config

from discord.ext import commands


class Context(commands.Context):
    command: commands.Command
    guild: discord.Guild


    async def approve(self, content: str, **kwargs: Any) -> discord.Message:
        return await self.send(
            embed=discord.Embed(
                description=f"{config.Emoji.approve} {self.author.mention} {content}",
                color=config.Color.green,
            ),
            **kwargs
        )

    async def deny(self, content: str, **kwargs: Any) -> discord.Message:
        return await self.send(
            embed=discord.Embed(
                description=f"{config.Emoji.deny} {self.author.mention} {content}",
                color=config.Color.red,
            ),
            **kwargs
        )

    async def warn(self, content: str, **kwargs: Any) -> discord.Message:
        return await self.send(
            embed=discord.Embed(
                description=f"{config.Emoji.warn} {self.author.mention} {content}",
                color=config.Color.yellow,
            ),
            **kwargs
        )

    async def embed(
        self: Context, 
        content: str, 
        emoji: Optional[str] = '', 
        color: Optional[int] = config.Color.info, 
        **kwargs: Any
    ) -> discord.Message:
        return await self.send(
            embed=discord.Embed(
                description=f"{emoji} {self.author.mention} {content}",
                color=color,
            ),
            **kwargs
        )

    async def send_help(self) -> discord.Message:
        example: str = getattr(self.command, "__original_kwargs__", {}).get("example", "")
        usage: str = self.command.usage if self.command.usage else ''

        return await self.send(
            embed=discord.Embed(
                color=config.Color.info,
                title="Command: " + self.command.qualified_name,
                description=(
                    (self.command.brief or "")
                    + f"```\nSyntax: {self.prefix}{self.command.name} {usage}"
                    + (
                        f"\nExample: {self.prefix}{self.command.name} {example}"
                        if example
                        else ""
                    )
                    + "```"
                ),
            ).set_author(
                name=self.bot.user.name,
                icon_url=self.bot.user.avatar,
            )
        )