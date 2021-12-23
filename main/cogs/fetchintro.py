import sqlite3
import discord
from discord.ext import commands


class FetchIntro(commands.Cog):

    # Initialization
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cursor: sqlite3.Connection = client.cursor

    # Setup Kartus
    @commands.command()
    async def fetchintro(self, ctx: commands.Context):
        if ctx.guild.id == 865211274567483434:
            loadmsg = await ctx.send("Loading....")
            loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
            del ctx.message.raw_mentions[0]
            if len(ctx.message.raw_mentions) == 0:
                name = []
                tag = []
                name.append(ctx.author.name)
                tag.append(ctx.author.discriminator)
            else:
                name = []
                tag = []
                for a in ctx.message.raw_mentions:
                    member = await self.client.fetch_user(a)
                    name.append(member.name)
                    tag.append(member.discriminator)
            channel = await self.client.fetch_channel(865450006337421383)
            temp_data = ""
            completed = []
            async for message in channel.history(limit=None, oldest_first=True):
                if message.author.name in name:
                    bits = message.content.split("\n")
                    temp_data += f"@{message.author.name}'s Intro\n"
                    for a in bits:
                        temp_data += f"> {a}\n"
                    temp_data += "\n\n"
                    completed.append(message.author.name)
            names = []
            if len(set(completed)) != len(set(name)):
                for n in name:
                    if n not in completed:
                        names.append(n)
                names = ", ".join(names)
                temp_data += f"Intro For {names} not found. Go type yo goddamm intro man..."
                print(name)
                print(names)
                print(completed)

            await loadmsg.delete()
            await loadgif.delete()
            await ctx.send(temp_data)


def setup(bot):
    bot.add_cog(FetchIntro(bot))
