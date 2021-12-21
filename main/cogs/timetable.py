import sqlite3
import discord
from discord.ext import commands
from cogs.utility.timetable import timetable

class TimeTableCommands(commands.Cog):

    # Initialization
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cursor: sqlite3.Connection = client.cursor

    @commands.command(aliases=("ws","week"))
    async def weeklyschedule(self,ctx:commands.Context):
        user = ctx.author
        data = self.cursor.execute(
            f"""Select * from schedule_display_data where client_id = "{user.id}";
            """
        ).fetchall()
        tt = timetable.TimeTable(data[0])
        tt.set_theme()
        tt._set_footers()
        tt._set_timetable()
        await ctx.channel.send(file=discord.File(tt.export_png(),filename="tt.png"))

def setup(bot):
    bot.add_cog(TimeTableCommands(bot))
