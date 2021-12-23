import os
import discord
from discord.ext import commands
import sqlite3

from discord_slash import SlashCommand
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
                # yep, did this cuz i don't have a command to add prefix.
                # thought i'll include it in setup_commands but moved on to sign_up
                # and also any other better way to append to database rather than using separator?
                # create new table?
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
client.slash = SlashCommand(client, sync_commands=True)

#################
#   OVERRIDES   #
#################

temp = client.slash.context_menu


def func(*args, **kwargs):
    if "guild_ids" not in kwargs:
        data = client.cursor.execute("Select guild_id from guilds_info;")
        data = [a[0] for a in data]
        kwargs["guild_ids"] = data
    return temp(*args, **kwargs)


client.slash.context_menu = func

#####################
#   END OVERRIDES   #
#####################

DiscordComponents(client)


@client.event
async def on_ready():
    print("Ready")
    emote_guild = client.get_guild(885046938171506688)
    client.emotes = {
        "full_heart": discord.utils.get(emote_guild.emojis, id=911538231911276604),
        "half_heart": discord.utils.get(emote_guild.emojis, id=911538231860953108),
        "no_heart": discord.utils.get(emote_guild.emojis, id=911538231928057906),
    }
    client.aro = client.get_user(608276451074113539)
    client.DEV_SERVER_BUGS_CHANNEL = client.get_channel(908662707824238602)


@client.command()
async def loadext(ctx: commands.Context, extention: str):
    if extention + ".py" in os.listdir("./main/cogs"):  # when running from home dir
        client.load_extension(f"cogs.{extention}")
        await ctx.send("Extension successfully loaded.")
    else:
        await ctx.send("Loading extension failed.")


@client.command()
async def unloadext(ctx: commands.Context, extention: str):
    if extention + ".py" in os.listdir("./main/cogs"):  # when running from home dir
        client.unload_extension(f"cogs.{extention}")
        await ctx.send("Extension successfully unloaded.")
    else:
        await ctx.send("Unloading extension failed.")


@client.command()
async def reloadext(ctx: commands.Context, extention: str):
    if extention + ".py" in os.listdir("./main/cogs"):  # when running from home dir
        client.reload_extension(f"cogs.{extention}")
        await ctx.send("Extension successfully Reloaded.")
    else:
        await ctx.send("Reloading extension failed.")


@client.command()
async def ping(ctx):
    await ctx.send("Pong! {0:.2f}ms".format(client.latency * 1000))


@client.check  # global check to see if kartus is setup in the guild
def Initialization_Check(ctx: commands.Context):
    data = client.cursor.execute("SELECT guild_id FROM guilds_info;").fetchall()
    if (str(ctx.guild.id),) not in data and ctx.command.name not in ("help", "setup"):
        ctx.ReasonForError = "Not Initialized"
        return False
    return True


@client.event
async def on_command_error(ctx: commands.Context, err):
    if type(err) == commands.errors.CheckFailure:
        if "ReasonForError" in dir(ctx) and ctx.ReasonForError == "Not Initialized":  # catches error from check
            await ctx.send("Setup kartus using ka!setup to use this command.")
        else:  # any other check error then raise
            raise err
    else:
        raise err


for a in os.listdir("./main/cogs"):  # loads all ext in cogs folder
    if a.endswith(".py"):
        client.load_extension(f"cogs.{a[:-3]}")
        print("loaded " + a)


client.run("ODg1Mzk5NzM1NTg0ODI5NDYw.YTmewg.NQTOOFMxEYMu_HE7VCHFeC_a_rw")
