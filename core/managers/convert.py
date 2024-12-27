"""
Custom converters for Ivy
"""
from __future__ import annotations
from typing import (
    Any, 
    List,
    Dict
)

import discord

from discord.ext import commands
from core.managers.context import Context


class Member(commands.MemberConverter):
    async def convert(self, context: Context, argument: Any) -> discord.Member:
        member: discord.Member = await super().convert(
            ctx=context, 
            argument=argument
        )
        if (
            member == context.author
            or member == context.bot.user
            or member == context.guild.owner
            or (
                member.top_role >= context.author.top_role #type: ignore
                and context.author != context.guild.owner
            )
        ):
            raise commands.CommandError("You cannot do this!")

        return member


class Status(commands.Converter):
    async def convert(self, argument: str) -> bool:
        if argument.lower() in (
            "enable", 
            "on",
            "yes"
        ):
            return True

        elif argument.lower() in (
            "disable", 
            "no",
            "off"
        ):
            return False

        else:
            raise commands.CommandError("Please specify **yes** or **no**")


class Module(commands.Converter):
    async def convert(self, argument: str) -> str:
        allowed: List[str] = [
            "ban",
            "kick",
            "channels",
            "roles",
            "webhooks",
            "botadd"
        ]

        if argument.lower() in allowed:
            return argument.lower()
        else:
            raise commands.CommandError(f"Invalid **module!**")


class Punishment(commands.Converter):
    async def convert(self, argument: str) -> str:
        allowed: List[str] = [
            "ban",
            "kick",
            "mute",
            "timeout",
            "strip", 
            "stripstaff"
        ]

        if argument.lower() in allowed:
            return argument.lower()
        else:
            raise commands.CommandError(f"Invalid **punishment!**")


class Time(commands.Converter):
    async def convert(self, argument: str) -> int:
        units: Dict[str, int] = {
            "s": 1,
            "m": 60,
            "h": 3600,
            "d": 86400
        }
        try:
            unit: str = argument[-1]
            value: int = int(
                argument[
                    :-1
                ]
            )
            if unit not in units:
                raise ValueError

            return value * units[unit]

        except (ValueError, IndexError):
            raise commands.CommandError("Invalid time **format!** Use `10m`, `2h`, etc")