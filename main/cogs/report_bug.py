from discord.ext import commands
import discord
from datetime import datetime


class ReportBug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="reportbug")
    async def report(self, ctx: commands.Context, *, text: str = ""):
        """For reporting bugs to the developer server in proper channel"""
        text = text.strip()
        server = ctx.guild
        channel = ctx.channel
        author = ctx.author
        avatar = author.avatar_url
        link = (
            f"https://discordapp.com/channels/{server.id}/{channel.id}/{ctx.message.id}"
        )
        if len(text) < 10:
            await ctx.send(
                "Please send a bug report of atleast 10 characters explaining the bug."
            )
        else:
            embed = discord.Embed(title="Bug", description=text)
            embed.set_author(name=author, icon_url=avatar)
            embed.add_field(
                name="Jump to message", value=f"[Link]({link})", inline=False
            )
            embed.add_field(name="Channel", value=f"<#{channel.id}>", inline=False)
            embed.add_field(name="Server", value=server)
            embed.add_field(
                name="Time", value=f"<t:{int(datetime.now().timestamp())}:F>"
            )
            await self.bot.DEV_SERVER_BUGS_CHANNEL.send(embed=embed)


def setup(bot):
    bot.add_cog(ReportBug(bot))
