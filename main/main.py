import os
import discord
from discord.ext import commands
import sqlite3

from initdb import create_database
import asyncio
from discord_components import (
    DiscordComponents,
    Button,
    ButtonStyle,
    Select,
    SelectOption,
)


SEPARATOR = "` `"

intents = discord.Intents.all()


class ClientWithDb(commands.Bot):
    def __init__(self, intents, database="Storage.db"):

        if database in os.listdir():
            # adding a method to client for database access
            self.cursor = sqlite3.connect(database)
        else:
            # create a new database with default layout
            self.cursor = create_database()
        super().__init__(intents=intents, command_prefix=self.get_prefix_from_db)

    def get_prefix_from_db(self, client, message: discord.Message):
        if not isinstance(message.channel, discord.channel.DMChannel):
            prefixes = self.cursor.execute(
                f"SELECT prefix FROM guilds_info WHERE guild_id = {message.guild.id}"
            ).fetchall()
            if prefixes:
                # ? sort while adding to database
                return sorted(prefixes[0][0].split(SEPARATOR), reverse=True)
            else:
                return "ka!"
        else:
            return "ka!"

    async def add_reactions_and_wait(
        self, ctx: commands.Context, temp_msg: discord.Message, timeout=30
    ):
        await temp_msg.add_reaction(tick := "☑️")
        await temp_msg.add_reaction(x := "❌")

        def check(reaction, user):
            return user == ctx.message.author and reaction.emoji in (tick, x)

        try:
            reaction, user = await self.wait_for(
                "reaction_add", timeout=timeout, check=check
            )
            if reaction.emoji == x:
                return False
            else:
                return True
        except asyncio.TimeoutError:
            return False


client = ClientWithDb(intents=intents)
DiscordComponents(client)


@client.event
async def on_ready():
    print("Ready")
    client.aro = client.get_user(608276451074113539)


@client.command()
async def loadext(ctx: commands.Context, extention: str):
    if extention + ".py" in os.listdir("./main/cogs"):
        client.load_extension(f"cogs.{extention}")
        await ctx.send("Extension successfully loaded.")
    else:
        await ctx.send("Loading extension failed.")


@client.command()
async def unloadext(ctx: commands.Context, extention: str):
    if extention + ".py" in os.listdir("./main/cogs"):
        client.unload_extension(f"cogs.{extention}")
        await ctx.send("Extension successfully unloaded.")
    else:
        await ctx.send("Unloading extension failed.")


@client.command()
async def reloadext(ctx: commands.Context, extention: str):
    if extention + ".py" in os.listdir("./main/cogs"):
        client.reload_extension(f"cogs.{extention}")
        await ctx.send("Extension successfully Reloaded.")
    else:
        await ctx.send("Reloading extension failed.")


@client.command()
async def ping(ctx):
    await ctx.send("Pong! {0:.2f}ms".format(client.latency * 1000))


@client.check
def Initialization_Check(ctx: commands.Context):
    data = client.cursor.execute("SELECT guild_id FROM guilds_info;").fetchall()
    if (str(ctx.guild.id),) not in data and ctx.command.name not in ("help", "setup"):
        ctx.ReasonForError = "Not Initialized"
        return False
    return True


@client.event
async def on_command_error(ctx: commands.Context, err):
    if type(err) == commands.errors.CheckFailure:
        if ctx.ReasonForError == "Not Initialized":
            await ctx.send("Setup kartus using ka!setup to use this command.")
        else:
            raise err
    else:
        raise err


for a in os.listdir("./main/cogs"):
    if a.endswith(".py"):
        client.load_extension(f"cogs.{a[:-3]}")
        print("loaded " + a)


client.run("ODg1Mzk5NzM1NTg0ODI5NDYw.YTmewg.NQTOOFMxEYMu_HE7VCHFeC_a_rw")
