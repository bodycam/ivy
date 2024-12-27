from __future__ import annotations
from typing import Optional

from discord.ext import commands

import discord

from core.ivy import Ivy
from core.managers.convert import Member, Time
from core.managers.context import Context


class Moderation(commands.Cog):
    # A lot of type ignores in here,
    # sorry for that.

    @commands.command(
        name="ban",
        brief="Ban a member",
        usage="(member) <reason>",
        example="Evie disrespected Ivy",
        aliases=[
            "banish",
            "fuckoff"
        ]
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def ban(
        self: Moderation, 
        context: Context,
        member: Member,
        reason: Optional[str] = 'N/A'
    ) -> discord.Message:
        """
        Ban a member
        """
        await context.guild.ban(user=member, reason=f"{context.author.name} {reason}") #type: ignore
        return await context.send(":thumbsup:")


    @commands.command(
        name="kick",
        brief="Kick a member",
        usage="(member) <reason>",
        example="Evie disrespected Ivy"
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_permissions(ban_members=True)
    async def kick(
        self: Moderation, 
        context: Context,
        member: Member,
        reason: Optional[str] = 'N/A'
    ) -> discord.Message:
        """
        Kick a member
        """
        await context.guild.kick(user=member, reason=f"{context.author.name} {reason}") #type: ignore
        return await context.send(":thumbsup:")


    @commands.command(
        name="mute",
        brief="Mute a member",
        usage="(member) (duration) <reason>",
        example="@Evie 10m called Ivy stinky",
        aliases=[
            "timeout",
            "m",
            "cockslap"
        ]
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_permissions(moderate_members=True)
    async def mute(
        self: Moderation, 
        context: Context, 
        member: Member, 
        duration: Time, 
        *,
        reason: Optional[str] = 'N/A'
    ) -> discord.Message:
        """
        Mute a member
        """
        await member.timeout(duration, reason) #type: ignore
        return await context.send(":thumbsup:")


    @commands.command(
        name="unmute",
        brief="Unmute a member",
        usage="(member)",
        example="@Evie",
        aliases=[
            "untimeout",
            "unm"
        ]
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_permissions(moderate_members=True)
    async def unmute(
        self: Moderation,
        context: Context, 
        member: Member
    ) -> discord.Message:
        """
        Unmute a member
        """
        await member.timeout(None) #type: ignore
        return await context.send(":thumbsup:")


    @commands.command(
        name="purge",
        brief="Purge your or everyones messages",
        usage="<member> (amount)",
        example="@evie 1337",
        aliases=[
            "c",
            "clear"
        ]
    )
    @commands.cooldown(1, 4, commands.BucketType.user)
    @commands.has_permissions(manage_messages=True)
    async def purge(
        self: Moderation, 
        context: Context, 
        member: Optional[discord.Member] = None,
        amount: int = 100
    ) -> discord.Message:
        """
        Purge your or everyones messages
        """

        await context.channel.purge( #type: ignore
            limit=amount, 
            check=(
                lambda m: not member 
                or m.author == member
            )
        )
        if member == None and amount > len(
            [
                message async for message
                in context.channel.history(
                    limit=amount
                )
            ]
        ):
            return await context.embed(
                "You cleared more messages **than there even is**, consider using `,nuke` next time for **faster** results!",
                emoji="<:information:1321456503714091070>",
                color=0x75CFD8
            )

        return await context.send(":thumbsup:")


async def setup(bot: Ivy):
    return await bot.add_cog(Moderation(bot))