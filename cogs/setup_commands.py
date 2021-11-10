import sqlite3
import discord
from discord.ext import commands


class SetupCommands(commands.Cog):

    # Initialization
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cursor: sqlite3.Connection = client.cursor

    # Setup Kartus
    @commands.command()
    async def setup(self, ctx: commands.Context):
        guilds = self.cursor.execute("SELECT guild_id FROM guilds_info").fetchall()
        if (str(ctx.guild.id),) in guilds:
            ctx.send("Kartus is already set-up and running")
            return
        overwrites = {
            ctx.guild.owner: discord.PermissionOverwrite(view_channel=True),
            ctx.guild.default_role: discord.PermissionOverwrite(view_channel=False),
        }
        kartus_category = await ctx.guild.create_category(
            "kartus", overwrites=overwrites, position=1
        )
        await kartus_category.edit(position=0)
        kartus_logs = await ctx.guild.create_text_channel(
            "kartus-logs", category=kartus_category
        )
        kartus_deleted_messages = await ctx.guild.create_text_channel(
            "deleted-messages", category=kartus_category
        )
        self.cursor.execute(
            f"""INSERT INTO guilds_info(guild_id,logs_channel_id,deleted_messages_channel_id) values( 
            '{ctx.guild.id}', 
            '{kartus_logs.id}', 
            '{kartus_deleted_messages.id}'
        )"""
        )
        self.cursor.commit()
        await kartus_logs.send(
            embed=discord.Embed(
                description="Logs channel successfully created. This channel is currently only visible to the guild owner."
            )
        )

    @commands.command()
    async def reset(self, ctx: commands.Context):
        if ctx.author != ctx.guild.owner:
            await ctx.send("Only guild owner and authorized members can reset guilds.")
            return
        guilds = self.cursor.execute("SELECT guild_id FROM guilds_info").fetchall()
        msg = await ctx.send("This Command Will Reset Kartus. Do you want to Proceed?")
        choice = await self.client.add_reactions_and_wait(ctx, msg)
        if choice:
            self.cursor.execute(
                f"""DELETE FROM guilds_info WHERE guild_id = '{ctx.guild.id}'"""
            )
            self.cursor.commit()
            await msg.edit(content="Reset Successful 👍")
        else:
            await msg.edit(content="Reset Canceled 👎")


def setup(bot):
    bot.add_cog(SetupCommands(bot))
