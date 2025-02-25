"""
RecruitMe Cog
"""

# Standard Library
import logging

# Third Party
import discord
from discord.embeds import Embed
from discord.ext import commands

# Django
from django.conf import settings
from django.utils import timezone

# Alliance Auth Discord Bot
from aadiscordbot import app_settings
from aadiscordbot.utils import auth

logger = logging.getLogger(__name__)


class RecruitMe(commands.Cog):
    """
    Thread Tools for recruiting!
    """

    def __init__(self, bot):
        """
        Initialize the RecruitMe cog

        :param bot: The bot instance
        :type bot: discord.ext.commands.Bot
        """

        self.bot = bot

    async def open_ticket(self, ctx: discord.Interaction, member: discord.Member):
        """
        Open a recruitment ticket

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :param member: The member requesting a recruiter
        :type member: discord.Member
        :return: None
        :rtype: None
        """

        auth_user = auth.get_auth_user(user=member, guild=ctx.guild)
        main_character = auth_user.profile.main_character

        ch = ctx.guild.get_channel(settings.TNNT_DISCORDBOT_COGS_RECRUITING_CHANNEL)
        th = await ch.create_thread(
            name=f"{main_character} | Recruitment | {timezone.now().strftime('%Y-%m-%d %H:%M')}",
            auto_archive_duration=10080,
            type=discord.ChannelType.private_thread,
            reason=None,
        )
        msg = (
            f"Dragging in: <@&{settings.TNNT_DISCORDBOT_COGS_LEADERSHIP_ROLE_ID}> "
            f"and <@&{settings.TNNT_DISCORDBOT_COGS_RECRUITER_ROLE_ID}> …\n\n"
            f"Hello <@{member.id}>! :wave:\n\n"
            "Someone from the recruitment team will get in touch with you soon!"
        )
        embd = Embed(
            title="Private Thread Guide",
            description=(
                "To add a person to this thread simply `@ping` them. "
                "This works with `@groups` as well to bulk add people to the channel. "
                "Use wisely, abuse will not be tolerated.\n\n"
                "This is a beta feature if you experience issues please "
                "contact the admins. :heart:"
            ),
        )

        await th.send(content=msg, embed=embd)
        await ctx.response.send_message(
            content="Recruitment thread created!", view=None, ephemeral=True
        )

    @commands.slash_command(name="recruit_me", guild_ids=app_settings.get_all_servers())
    async def slash_recruit_me(self, ctx):
        """
        Get hold of a recruiter

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :return: None
        :rtype: None
        """

        if settings.TNNT_DISCORDBOT_COGS_APPLICANT_ROLE_ID not in [
            role.id for role in ctx.user.roles
        ]:
            return await ctx.respond(
                (
                    "You are not in the Applicants group. Please open the "
                    "[groups page](https://auth.terra-nanotech.de/groups/) and join "
                    "the `TN-NT Applicant` group first …"
                ),
                ephemeral=True,
            )

        await self.open_ticket(ctx=ctx, member=ctx.user)

    @commands.message_command(
        name="Create Recruitment Thread", guild_ids=app_settings.get_all_servers()
    )
    async def reverse_recruit_msg_context(self, ctx, message):
        """
        Help a new guy get recruiter

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :param message: The message that triggered the command
        :type message: discord.Message
        :return: None
        :rtype: None
        """

        # Check if the user is a recruiter and if the user is different from the target user
        if settings.TNNT_DISCORDBOT_COGS_RECRUITER_ROLE_ID not in [
            role.id for role in ctx.user.roles
        ] and int(ctx.user.id) != int(message.author.id):
            return await ctx.respond(
                (
                    "You are not a recruiter for Terra Nanotech and "
                    "cannot use this command on this user …"
                ),
                ephemeral=True,
            )

        # Check if the target user is in the Applicants group
        if settings.TNNT_DISCORDBOT_COGS_APPLICANT_ROLE_ID not in [
            role.id for role in message.author.roles
        ]:
            return await ctx.respond(
                f"{message.author.mention} is not in the Applicants group …",
                ephemeral=True,
            )

        await self.open_ticket(ctx=ctx, member=message.author)

    @commands.user_command(
        name="Recruit Member", guild_ids=app_settings.get_all_servers()
    )
    async def reverse_recruit_user_context(self, ctx, user):
        """
        Help a new guy get recruiter

        :param ctx: The context of the command
        :type ctx: discord.Interaction
        :param user: The user that triggered the command
        :type user: discord.User
        :return: None
        :rtype: None
        """

        # Check if the user is a recruiter and if the user is different from the target user
        if settings.TNNT_DISCORDBOT_COGS_RECRUITER_ROLE_ID not in [
            role.id for role in ctx.user.roles
        ] and int(ctx.user.id) != int(user.id):
            return await ctx.respond(
                (
                    "You are not a recruiter for Terra Nanotech and "
                    "cannot use this command on this user …"
                ),
                ephemeral=True,
            )

        # Check if the target user is in the Applicants group
        if settings.TNNT_DISCORDBOT_COGS_APPLICANT_ROLE_ID not in [
            role.id for role in user.roles
        ]:
            return await ctx.respond(
                f"{user.mention} is not in the Applicants group …",
                ephemeral=True,
            )

        await self.open_ticket(ctx=ctx, member=user)


def setup(bot):
    """
    Set up the RecruitMe cog

    :param bot:
    :type bot:
    :return:
    :rtype:
    """

    if bot.get_cog("RecruitMe") is None:
        bot.add_cog(RecruitMe(bot))
