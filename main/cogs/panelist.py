import sqlite3
import discord
from discord.ext import commands
import csv

THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/872059879379050527/889749015938334730/Copy_of_VITC25.png"


class Panel(commands.Cog):

    # Initialization
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cursor: sqlite3.Connection = client.cursor

    @commands.command()
    async def panel(self, ctx: commands.Context, regno:str):
        f = open("main/cogs/Resources/panel/panel detail.csv",encoding="UTF-8")
        reader = csv.reader(f)
        for row in reader:
            if row[1] == regno:
                break
        else:
            await ctx.message.reply("Reg No not found :(")
            f.close()
            return
        username = row[2]
        facultyname = row[3]
        f.close()
        
        f = open("main/cogs/Resources/panel/faculty contact.csv",encoding="UTF-8")
        reader = csv.reader(f)
        for row in reader:
            if row[3] == facultyname:
                break
        else:
            await ctx.message.reply("Faculty not found :(")
            f.close()
            return
        f.close()
        
        embed = discord.Embed(title = "Pannelist Info",colour=discord.Colour.from_rgb(207, 68, 119))
        embed.add_field(name = "Student Name",value = username,inline=True)
        embed.add_field(name = "Student Reg No",value = regno,inline=True)
        embed.add_field(name = "Faculty Name",value = facultyname,inline = False)
        embed.add_field(name = "Faculty Number",value = row[5],inline = True)
        embed.add_field(name = "Faculty Email",value = row[6],inline = True)
        embed.set_thumbnail(url = THUMBNAIL_URL)
        embed.set_image(url = "https://cdn.discordapp.com/attachments/905886505770303488/923460471108038696/unknown.png")

        await ctx.send(embed =embed)

def setup(bot):
    bot.add_cog(Panel(bot))
