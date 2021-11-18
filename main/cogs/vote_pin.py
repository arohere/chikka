from discord.ext import commands
import discord
from datetime import datetime
from discord_slash.context import MenuContext
from discord_slash.model import ContextMenuType
import asyncio


class VotePin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

        @self.bot.slash.context_menu(target=ContextMenuType.MESSAGE, name="Vote pin")
        async def vote_pin(ctx: MenuContext):
            attachments = ctx.target_message.attachments
            text = ctx.target_message.content
            server = ctx.target_message.guild
            channel = ctx.target_message.channel
            author = ctx.target_message.author
            avatar = author.avatar_url
            link = f"https://discordapp.com/channels/{server.id}/{channel.id}/{ctx.target_message.id}"
            embed = discord.Embed(title="Pin", description=text)
            embed.set_author(name=author, icon_url=avatar)
            embed.add_field(
                name="Jump to message", value=f"[Link]({link})", inline=False
            )
            embed.add_field(name="Channel", value=f"<#{channel.id}>", inline=False)
            embed.add_field(name="Server", value=server)
            embed.add_field(
                name="Time", value=f"<t:{int(datetime.now().timestamp())}:F>"
            )
            if attachments:
                for i, j in enumerate(attachments):
                    embed.add_field(
                        name=f"Attachment {i+1}", value=f"[Link]({j.url})", inline=False
                    )

            msg = await ctx.send(embed=embed)

            TIMEOUT = 10
            REACTIONS = 3

            await msg.add_reaction(tick := "☑️")
            try:
                await self.bot.wait_for("message_delete", timeout=TIMEOUT)
                await msg.edit(
                    embed=discord.Embed(
                        title="Pin", description="Message deleted. Kill the author plz"
                    )
                )
                await msg.clear_reactions()
            except asyncio.TimeoutError:
                cache_msg = discord.utils.get(bot.cached_messages, id=msg.id)
                for reaction in cache_msg.reactions:
                    if reaction.emoji == tick and reaction.count >= REACTIONS:
                        await ctx.target_message.pin()
                    else:
                        await msg.edit(
                            embed=discord.Embed(
                                title="Pin",
                                description=f"Message not pinned. It needs atleast {REACTIONS} reactions.",
                            )
                        )

        VotePin.vote_pin = vote_pin


def setup(bot):
    bot.add_cog(VotePin(bot))
