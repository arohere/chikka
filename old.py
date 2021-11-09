
# pip install discord-py-slash-command


import asyncio
import discord
import os
import pickle
from tabulate import tabulate
from discord.ext import commands
from bs4 import BeautifulSoup
from datetime import datetime as dt, timedelta
from discord.embeds import Embed
from datetime import datetime
from pytz import timezone
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from discord_slash import SlashCommand
from discord_slash.context import MenuContext, ComponentContext, SlashContext
from discord_slash.model import ContextMenuType
from discord_slash.utils.manage_commands import create_choice, create_option
from discord_slash.utils.manage_components import create_select, create_select_option, create_actionrow
from discord_slash.utils.manage_components import create_button, create_actionrow
import uwuify

# from discord import channel


# from discord.enums import DefaultAvatar

# def uni(f):
#     for l in f:
#         yield l.decode("UTF-8")

intents = discord.Intents.all()
intents.members = True
# client = discord.Client(intents=intents)
client = commands.Bot(intents=intents, command_prefix=commands.when_mentioned)
slash = SlashCommand(client, sync_commands=True)
helpchnl = None
cmds = None
initated = False
data = {}


def check_and_read_data():
    global initated
    global data
    if os.path.exists("DiscordBotStorage.dat"):
        with open("DiscordBotStorage.dat", "rb") as f:
            data = pickle.load(f)
            initated = True
        return True

    else:
        data = {
            "server_bans": [],
            "server_warns": [],
            "total_deleted_msgs": 0,
            "del_chn": None,
            "logs_chn": None,
            "guild": None,
            "scheduledata": {}

        }


class TTscrap:  # object to scrap timetable data from HTML file

    def __init__(self, file):

        # initialising the sexy soup
        self.s = BeautifulSoup(file.decode("UTF-8"), 'html.parser')
        self.tables = self.s.find_all('table')  # finding all tables

    def get_data(self):
        if not self.tables:
            return "Wrong HTML"
        output = []
        rows = self.tables[0].find_all('tr')  # get all rows
        data2 = list(filter(None, [rows[b].find_all('td') for b in range(len(rows)) if b]))[:-1]  # remove the last <tr> which has total credits
        for b in range(len(data2)):  # extracting only required data
            try:
                # get only required data
                paras = [data2[b][c].find_all('p') for c in [2, 7, 8]]
                # get text from p tags
                output += [[paras[c][0].text+'' +
                            paras[c][1].text for c in range(3)]]
            except IndexError:  # catch indexing errors for possible future tables which have rows like total credits
                # do raise Warning() if you want bot to capture
                print(data2[b])
        return output


def ppschedule_get(data):
    morning_template = [['Start\nEnd', '08:00 AM\n08:50 AM', '08:50 AM\n09:45 AM', '09:50 AM\n10:40 AM', '10:40 AM\n11:35 AM', '11:40 AM\n12:30 PM', '12:30 PM\n01:25 PM'], ['MON', 'A1 L1', 'F1 L2', 'D1 L3', 'TB1 L4', 'TG1 L5', 'S11 L6'], ['TUE', 'B1 L7', 'G1 L8', 'E1 L9', 'TC1 L10', 'TAA1 L11', 'L12'], ['WED', 'C1 L13', 'A1 L14','F1 L15', 'TD1 L16', 'TBB1 L17', 'L18'], ['THU', 'D1 L19', 'B1 L20', 'G1 L21', 'TE1 L22', 'TCC1 L23', 'L24'], ['FRI', 'E1 L25', 'C1 L26', 'TA1 L27', 'TF1 L28', 'TDD1 L29', 'S15 L30'], ['SAT', 'X11 L71', 'X12 L72', 'Y11 L73', 'Y12 L74', 'S8 L75', 'L76'], ['SUN', 'Y11 L83', 'Y12 L84', 'X11 L85', 'X12 L86', 'S10 L87', 'L88']]
    afternoon_template = [['Start\nEnd', '02:00 PM\n02:50 PM', '02:50 PM\n03:45 PM', '03:50 PM\n04:40 PM', '04:40 PM\n05:35 PM', '05:40 PM\n06:30 PM', '06:30 PM\n07:25 PM'], ['MON', 'A2 L31', 'F2 L32', 'D2 L33', 'TB2 L34', 'TG2 L35', 'S3 L36'], ['TUE', 'B2 L37', 'G2 L38', 'E2 L39', 'TC2 L40', 'TAA2 L41', 'S1 L42'], ['WED', 'C2 L43', 'A2 L44', 'F2 L45', 'TD2 L46', 'TBB2 L47', 'S4 L48'], ['THU', 'D2 L49', 'B2 L50', 'G2 L51', 'TE2 L52', 'TCC2 L53', 'S2 L54'], ['FRI', 'E2 L55', 'C2 L56', 'TA2 L57', 'TF2 L58', 'TDD2 L59', 'L60'], ['SAT', 'X21 L77', 'Z21 L78', 'Y21 L79', 'W21 L80', 'W22 L81', 'L82'], ['SUN', 'Y21 L89', 'Z21 L90', 'X21 L91', 'W21 L92', 'W22 L93', 'L94']]

    footnotes = []
    try:
        for a in data:
            status = False
            for b in a[1].split(" - ")[0].split("+"):
                for c in range(len(morning_template)):
                    for d in range(len(morning_template[c])):
                        if b in morning_template[c][d].split():
                            morning_template[c][d] = a[0].split()[0]
                            status = True
                for c in range(len(afternoon_template)):
                    for d in range(len(afternoon_template[c])):
                        if b in afternoon_template[c][d].split():
                            afternoon_template[c][d] = a[0].split()[0]
                            status = True
            if status:
                footnotes.append([a[0].split(" (")[0], a[2]])

    except Exception as e:
        print(e)
        return ("Wrong Format", e)

    table1 = (
        tabulate(morning_template[1:], tablefmt="pretty", headers=morning_template[0]))

    table2 = (tabulate(
        afternoon_template[1:], tablefmt="pretty", headers=afternoon_template[0]))

    table3 = (tabulate(footnotes, tablefmt="pretty"))

    return table1, table2, table3


def ppschedule_today(data, users, day="today"):
    slots = ['A1 L1', 'F1 L2', 'D1 L3', 'TB1 L4', 'TG1 L5', 'S11 L6', 'B1 L7', 'G1 L8', 'E1 L9', 'TC1 L10', 'TAA1 L11', 'L12', 'C1 L13', 'A1 L14', 'F1 L15', 'TD1 L16', 'TBB1 L17', 'L18', 'D1 L19', 'B1 L20', 'G1 L21', 'TE1 L22', 'TCC1 L23', 'L24', 'E1 L25', 'C1 L26', 'TA1 L27', 'TF1 L28', 'TDD1 L29', 'S15 L30', 'X11 L71', 'X12 L72', 'Y11 L73', 'Y12 L74', 'S8 L75', 'L76', 'Y11 L83', 'Y12 L84', 'X11 L85', 'X12 L86', 'S10 L87', 'L88',
             'A2 L31', 'F2 L32', 'D2 L33', 'TB2 L34', 'TG2 L35', 'S3 L36', 'B2 L37', 'G2 L38', 'E2 L39', 'TC2 L40', 'TAA2 L41', 'S1 L42', 'C2 L43', 'A2 L44', 'F2 L45', 'TD2 L46', 'TBB2 L47', 'S4 L48', 'D2 L49', 'B2 L50', 'G2 L51', 'TE2 L52', 'TCC2 L53', 'S2 L54', 'E2 L55', 'C2 L56', 'TA2 L57', 'TF2 L58', 'TDD2 L59', 'L60', 'X21 L77', 'Z21 L78', 'Y21 L79', 'W21 L80', 'W22 L81', 'L82', 'Y21 L89', 'Z21 L90', 'X21 L91', 'W21 L92', 'W22 L93', 'L94']
    now = dt.now(timezone("Asia/Kolkata"))
    if day == "today":
        day = now.strftime("%a").upper()
    else:
        day = day.upper()
    morning_template = [['Start\nEnd', '08:00 AM\n08:50 AM', '08:50 AM\n09:45 AM', '09:50 AM\n10:40 AM', '10:40 AM\n11:35 AM', '11:40 AM\n12:30 PM', '12:30 PM\n01:25 PM'], ['MON', 'A1 L1', 'F1 L2', 'D1 L3', 'TB1 L4', 'TG1 L5', 'S11 L6'], ['TUE', 'B1 L7', 'G1 L8', 'E1 L9', 'TC1 L10', 'TAA1 L11', 'L12'], ['WED', 'C1 L13', 'A1 L14',
                                                                                                                                                                                                                                                                                                                 'F1 L15', 'TD1 L16', 'TBB1 L17', 'L18'], ['THU', 'D1 L19', 'B1 L20', 'G1 L21', 'TE1 L22', 'TCC1 L23', 'L24'], ['FRI', 'E1 L25', 'C1 L26', 'TA1 L27', 'TF1 L28', 'TDD1 L29', 'S15 L30'], ['SAT', 'X11 L71', 'X12 L72', 'Y11 L73', 'Y12 L74', 'S8 L75', 'L76'], ['SUN', 'Y11 L83', 'Y12 L84', 'X11 L85', 'X12 L86', 'S10 L87', 'L88']]
    afternoon_template = [['Start\nEnd', '02:00 PM\n02:50 PM', '02:50 PM\n03:45 PM', '03:50 PM\n04:40 PM', '04:40 PM\n05:35 PM', '05:40 PM\n06:30 PM', '06:30 PM\n07:25 PM'], ['MON', 'A2 L31', 'F2 L32', 'D2 L33', 'TB2 L34', 'TG2 L35', 'S3 L36'], ['TUE', 'B2 L37', 'G2 L38', 'E2 L39', 'TC2 L40', 'TAA2 L41', 'S1 L42'], [
        'WED', 'C2 L43', 'A2 L44', 'F2 L45', 'TD2 L46', 'TBB2 L47', 'S4 L48'], ['THU', 'D2 L49', 'B2 L50', 'G2 L51', 'TE2 L52', 'TCC2 L53', 'S2 L54'], ['FRI', 'E2 L55', 'C2 L56', 'TA2 L57', 'TF2 L58', 'TDD2 L59', 'L60'], ['SAT', 'X21 L77', 'Z21 L78', 'Y21 L79', 'W21 L80', 'W22 L81', 'L82'], ['SUN', 'Y21 L89', 'Z21 L90', 'X21 L91', 'W21 L92', 'W22 L93', 'L94']]

    morning_template = [morning_template[0]] + \
        [a for a in morning_template if a[0] == day]
    afternoon_template = [afternoon_template[0]] + \
        [a for a in afternoon_template if a[0] == day]

    keys = {}

    for a in range(len(users)):
        for b in data[a]:
            for d in b[1].split(" - ")[0].split("+"):
                for e in slots:
                    if d in e.split():
                        if e in keys:
                            temp = b[0].split(" - ")[0]
                            keys[e][0] += f"{temp} \n-@{users[a]}\n"
                            keys[e][1] += ((b[0], b[2]),)
                        else:
                            temp = b[0].split(" - ")[0]
                            keys[e] = [
                                f"{temp} \n-@{users[a]}\n", ((b[0], b[2]),)]

    footnotes = set()
    try:
        for b in keys:
            # status = False
            for c in range(len(morning_template)):
                for d in range(len(morning_template[c])):
                    if b == morning_template[c][d]:
                        morning_template[c][d] = keys[b][0]
                        for row in keys[b][1]:
                            footnotes.add(row)
                        # status = True
            for c in range(len(afternoon_template)):
                for d in range(len(afternoon_template[c])):
                    if b == afternoon_template[c][d]:
                        afternoon_template[c][d] = keys[b][0]
                        for row in keys[b][1]:
                            footnotes.add(row)
                        # status = True
            # if status:
            #     footnotes.append([a[0].split(" (")[0],a[2]])
    except Exception as e:
        print(e)
        return ("Wrong Format", e)

    table1 = (
        tabulate(morning_template[1:], tablefmt="pretty", headers=morning_template[0]))

    table2 = (tabulate(
        afternoon_template[1:], tablefmt="pretty", headers=afternoon_template[0]))

    table3 = (tabulate(tuple(footnotes), tablefmt="pretty"))

    return table1, table2, table3


guild = None
del_chn = None
logs_chn = None
admin_ver = None

client.remove_command("help")


@client.event
async def on_ready():
    if check_and_read_data():
        global del_chn
        global logs_chn
        global admin_ver
        global guild
        guild = await client.fetch_guild(data["guild"])
        del_chn = client.get_channel(data["del_chn"])
        logs_chn = client.get_channel(data["logs_chn"])
        admin_ver = client.get_channel(data["admin_ver"])
    print("Ready")
    global helpchnl
    helpchnl = client.get_guild(892288041908076564)
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="DM to Contact Staff", start=dt.now()))
    global cmds
    cmds = {"uploadschedule": f"**Syntax:- ** {client.user.mention} uploadschedule\n\n**Description:-**\nUse This Command To Upload your Schedule to {client.user.mention}. Step By Step Instructions will be Displayed after the Command is Executed.",
            "weekschedule": f"**Syntax:- ** {client.user.mention} weekschedule [user]\n\n**Aliases:- ** `ws`,`wschedule`\n\n**Description:-**\nUse This Command To Retrive Weekly Schedule of the mentioned user from {client.user.mention}. If no user is mentioned then the authors schedule is retrived.",
            "dayschedule": f"**Syntax:- ** {client.user.mention} dayschedule [user1] [user2]...[usern] [day]\n\n**Aliases:- ** `ds`,`dschedule`\n\n**Description:-**\nUse This Command To Retrive Schedules of the mentioned users from {client.user.mention} for a paticular day. If no user is mentioned then the authors schedule is retrived. If no day is Mentioned then present days schedule is retrived.",
            "scanschedule": f"**Syntax:- **scanschedule\n\n**Description:-**\nUse This Command To Find Members with Same Courses as you.",
            "countmein": [f"CountMeIn is a feature in {client.user.mention} which is used to keep track of events happening in VIT-C Server. Events are Announced by Admins/Mods and intrested members can register using this command.", f"```\ncountmein stats\ncountmein <Event Name>```\n", [["countmein stats", "Retrives List of Ongoing Events and Registered Members"], ["countmein <Event Name>", "Registers Yourself for an Ongoing Event. To Backof From an Event Enter this Command Again."]]],
            "addgif": f"**Syntax:- ** {client.user.mention} addgif <KeyWord> <GIF Link>\n\n**Description:-**\nThis Command assigns a GIF to a keyword. Pinging Kartus with the keyword, like '{client.user.mention} vibe',makes Kartus Post the Respective Keywords GIF**",
            "listgifs": f"**Syntax:- ** {client.user.mention} listgifs\n\n**Description:-**\nThis Command Retrives Existing GIFs with its Respective Keyword and Creator.",
            "removegif": f"**Syntax:- ** {client.user.mention} removegif\n\n**Description:-**\n GIFs can only be removed by mods.",
            "fetchintro": f"**Syntax:- ** {client.user.mention} fetchintro [user1] [user2]...[usern]\n\n**Description:-**\nThis Command Searches and returns introduction of the mentioned users from {client.get_channel(865450006337421383).mention}"}
    # myLoop.start()


@client.command()
async def help(ctx, *, cmd=""):
    if not cmd:
        emb = Embed(description="Kartus is VIT-C Student's Clubs Custom-Made Bot.\nYoroshiku Onegaishimasu<:gojo:885934411701440513>\n\nNote: Use help <command> to get indepth info about the command.",
                    title="Kartus Help", colour=discord.Colour.from_rgb(207, 68, 119))
        emb.add_field(name="Schedule Commands",
                      value="```\nuploadschedule\ndayschedule\nweekschedule\nscanschedule```", inline=False)
        emb.add_field(name="CountMeIn",
                      value="```\ncountmein\ncountmein stats```", inline=False)
        emb.add_field(name="GIF Related",
                      value="```\naddgif\nlistgifs\nremovegif```", inline=False)
        emb.add_field(name="Miscellaneous",
                      value="```\nping\nfetchintro```", inline=False)
        emb.set_author(name="Kartus", icon_url=client.user.avatar_url_as())
        emb.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/887988341998514176/893748283791527936/VITC25.png")
        emb.set_footer(icon_url=ctx.author.avatar_url_as(
        ), text=f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.channel.send(embed=emb)

    elif cmd.split(" ")[0] in cmds:
        cmd = cmd.split(" ")[0]

        if type(cmds[cmd]) == list:
            emb = Embed(description=cmds[cmd][0], title=cmd,
                        colour=discord.Colour.from_rgb(207, 68, 119))
            emb.add_field(name="Available Commands",
                          value=cmds[cmd][1], inline=False)
            for a, b in cmds[cmd][2]:
                emb.add_field(name=a, value=b, inline=False)
        else:
            emb = Embed(description=cmds[cmd], title=cmd,
                        colour=discord.Colour.from_rgb(207, 68, 119))

        emb.set_author(name="Kartus", icon_url=client.user.avatar_url_as())
        emb.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/887988341998514176/893748283791527936/VITC25.png")
        emb.set_footer(icon_url=ctx.author.avatar_url_as(
        ), text=f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.channel.send(embed=emb)
    else:
        await ctx.send(f"Docs for {cmd.split(' ')[0]} Not Found.")


@client.after_invoke
async def myLoop(ctx):
    global data
    print(
        f'Backup Taken! {dt.now(timezone("Asia/Kolkata")).strftime("%m/%d/%Y, %H:%M:%S")}')
    with open("DiscordBotStorage.dat", "wb") as f:
        pickle.dump(data, f)


@client.command()
async def countmein(ctx, *contents):
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    auth = ctx.author

    if contents[0] == "reset" and mod in auth.roles and len(contents) == 2:
        if contents[1] in data["countmein"]:
            temp_msg = await ctx.send(f"Entry For {contents[1]} Will Be Erased. Do you wanna proceed?")
            tick = "☑️"
            x = "❌"
            await temp_msg.add_reaction(tick)
            await temp_msg.add_reaction(x)

            def check(reaction, user):
                return user == ctx.message.author and reaction.emoji in (tick, x)
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                if reaction.emoji == x:
                    await temp_msg.edit(content="Database Unchanged.")
                    return
            except asyncio.TimeoutError:
                await temp_msg.edit(content="Database Unchanged.")
                return
            del data["countmein"][contents[1]]
            await ctx.send(f"Entry for {contents[1]} has been deleted.")
        else:
            await ctx.send(f"Man No count for `{contents[0]}` is happening. Getouttahere!")

    elif contents[0] == "stats":
        desc = ""
        for a in data["countmein"]:
            members = []
            desc += f"Members For **{a}**\n"
            for b in data["countmein"][a][0]:
                member = await client.fetch_user(b)
                members.append(member.mention)
            desc += "\n".join(members)
            desc += "\n\n"
        embed = Embed(description=desc, title="CountMeIn Stats")
        await ctx.send(embed=embed)
    elif contents[0] == "startcount" and len(contents) == 2:
        if mod in auth.roles:
            if contents[1] in data["countmein"]:
                temp_msg = await ctx.send(f"Count for {contents[1]} is ongoing. Do you want to Reset it?")
                tick = "☑️"
                x = "❌"
                await temp_msg.add_reaction(tick)
                await temp_msg.add_reaction(x)

                def check(reaction, user):
                    return user == ctx.message.author and reaction.emoji in (tick, x)
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                    if reaction.emoji == x:
                        await temp_msg.edit(content="Stats Unchanged.")
                        return
                except asyncio.TimeoutError:
                    await temp_msg.edit(content="Stats Unchanged.")
                    return
            data["countmein"][contents[1]] = [[], auth.id, datetime.now(
                timezone("Asia/Kolkata")).strftime("%m/%d/%Y, %H:%M")]
            await ctx.send("Entry Successfully Registered.")
        else:
            await ctx.send("Only Mods can Start Counts For An Event.")

    elif len(contents) == 1:
        if contents[0] in data["countmein"]:
            if auth.id in data["countmein"][contents[0]][0]:
                temp_msg = await ctx.send("You Have already been registered. Do You wanna Deregister?")
                tick = "☑️"
                x = "❌"
                await temp_msg.add_reaction(tick)
                await temp_msg.add_reaction(x)

                def check(reaction, user):
                    return user == ctx.message.author and reaction.emoji in (tick, x)
                try:
                    reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                    if reaction.emoji == x:
                        await temp_msg.edit(content="Registraction Intact.")
                        return
                except asyncio.TimeoutError:
                    await temp_msg.edit(content="Registration Intact.")
                    return
                else:
                    data["countmein"][contents[0]][0].remove(auth.id)
                    await ctx.send("Your Registration Has Been Canceled.")
                    return
            else:
                data["countmein"][contents[0]][0].append(auth.id)
                await ctx.send("Registration Successfull.")
        else:
            await ctx.send(f"Man No count for `{contents[0]}` is happening. Getouttahere!")
    else:
        await ctx.send("Wrong Syntax.")


@client.event
async def on_message(msg):

    if msg.content == "uwuify" and msg.reference:
        await msg.channel.send(uwuify.uwu(msg.reference.cached_message.content))
        await msg.delete()

    if "invite" in msg.content and "this server" in msg.content:
        await msg.reply("Here You Go!\n\nhttps://discord.gg/K5UMjshn63")

    if str(msg.channel.type) == "private" and msg.author.bot == False:
        opendm = discord.utils.get(helpchnl.categories, id=892291812016930817)
        if msg.channel.id in data["staffchat"]:
            chnl = helpchnl.get_channel(data["staffchat"][msg.channel.id])
            webhook = await chnl.webhooks()
            if chnl.category_id == 892291844170473483:
                await chnl.edit(category=opendm)
                data["staffchatdmstats"][msg.channel.id] = "first"
            webhook = webhook[0]
        else:
            chnl = await helpchnl.create_text_channel(name=f"{msg.author.name}-{msg.author.discriminator}", category=opendm)
            webhook = await chnl.create_webhook(name=msg.author.name)
            data["staffchat"][msg.channel.id] = chnl.id
            data["staffchatdmstats"][msg.channel.id] = "first"
        if msg.attachments:
            files = []
            for fp in msg.attachments:
                content = await fp.read()
                with open(fp.filename, "wb") as f:
                    f.write(content)
                files.append(discord.File(fp.filename))
            await chnl.send(msg.content, files=files)
            os.remove(fp.filename)
        else:
            await webhook.send(msg.content, username=msg.author.name, avatar_url=msg.author.avatar_url_as())

        return
    elif msg.channel.id in data["staffchat"].values() and msg.author.bot == False:
        for a in data["staffchat"]:
            if data["staffchat"][a] == msg.channel.id:
                chnl = client.get_channel(a)
                if "closedm" in msg.content and client.user in msg.mentions:
                    if data["staffchatdmstats"][a] == "closed":
                        await msg.channel.send(embed=Embed(description="DM is Already Closed", color=discord.Color.random()))
                        return
                    closeddm = discord.utils.get(
                        helpchnl.categories, id=892291844170473483)
                    data["staffchatdmstats"][a] = "closed"
                    await msg.channel.send(embed=Embed(description="This DM is Closed.", color=discord.Color.random()))
                    await msg.channel.edit(category=closeddm)
                    return
                if "opendm" in msg.content and client.user in msg.mentions:
                    if data["staffchatdmstats"][a] == "open":
                        await msg.channel.send(embed=Embed(description="DM is Already Open", color=discord.Color.random()))
                        return
                    opendm = discord.utils.get(
                        helpchnl.categories, id=892291812016930817)
                    data["staffchatdmstats"][a] = "first"
                    await msg.channel.send(embed=Embed(description="This DM is Opened.", color=discord.Color.random()))
                    await msg.channel.edit(category=opendm)
                    return
                if data["staffchatdmstats"][a] == "first":
                    await chnl.send(embed=Embed(description=f"You are now texting with {msg.author.mention}", color=discord.Color.random()))
                    data["staffchatdmstats"][a] = "open"
                elif data["staffchatdmstats"][a] == "closed":
                    await msg.channel.send(embed=Embed(description=f"This DM is Closed. Use '{client.user.mention} opendm' to Open DM.", color=discord.Color.random()))
                    return

                if msg.attachments:
                    files = []
                    for fp in msg.attachments:
                        content = await fp.read()
                        with open(fp.filename, "wb") as f:
                            f.write(content)
                        files.append(discord.File(fp.filename))
                    await chnl.send(msg.content, files=files)

                    os.remove(fp.filename)
                else:
                    await chnl.send(msg.content)
                break
    if "69" in msg.content:
        try:
            await msg.add_reaction("😏")
        except:
            pass
    try:
        if msg.content.split()[1].lower() in data["gifs"] and client.user in msg.mentions:
            await msg.channel.send(data["gifs"][msg.content.split()[1].lower()][0])
            await msg.delete()
            return
    except IndexError:
        pass

    if msg.channel.id == 881697347128668200 and msg.author.id == 356268235697553409:
        await msg.delete(delay=5)

    msg.content = " ".join([a for a in msg.content.split(" ") if a])
    await client.process_commands(msg)
    if initated:     # Delete Links in Chat And Warn
        lst = ["chat.whatsapp.com", "discord.gg", "t.me"]
        roles = await msg.guild.fetch_roles()
        mod = discord.utils.get(roles, name="Moderator")
        for a in lst:
            if a in msg.content and msg.channel != del_chn and mod not in msg.author.roles:
                await msg.delete()
                await msg.channel.send(f"LOL Refrain From Sending Links :)\n\n{msg.author.mention}")
                break


@client.command(aliases=["invite"])
async def fetchinvite(ctx):
    await ctx.message.reply("Here You Go!\n\nhttps://discord.gg/K5UMjshn63")


@client.command()
async def addgif(ctx, name, gif):
    commands = [a.name for a in client.commands]
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    author = ctx.author
    if name in commands:
        await ctx.send(f"`{name}` is a Command Used by the Bot. Try Again With a Different Keyword")
        return
    elif name in data["gifs"] and mod not in author.roles:
        await ctx.send(f"Keyword `{name}` is in use. Request a Moderator to change the gif for the Designated keyword.")
        return
    if "https://" in gif and "gif" in gif:
        data["gifs"][name.lower()] = [gif, ctx.author.name]
        embed = Embed(description="Gif Has Been Successfully Added",
                      colour=discord.Colour.from_rgb(207, 68, 119))
        await ctx.message.delete()
        await ctx.send(embed=embed)
        await logs_chn.send(embed=Embed(description=f"{ctx.author.mention} added a GIF to a keyword `{name}`"))
    else:
        await ctx.send("Wrong Format! @Kartus addgif <keyword> <gif link>")


@client.command()
async def removegif(ctx, name):
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    if name.lower() in data["gifs"]:
        if mod in ctx.author.roles:
            del data["gifs"][name.lower()]
            await ctx.send(embed=Embed(description="GIF removed Successfully"))
        else:
            await ctx.send(f"You don't have the Permission to remove GIFs. Request a Moderator For Assistance.")
    else:
        await ctx.send("GIF not found.")


@client.command()
async def listgifs(ctx):
    desc = "\n".join(
        [f"[{a}]({data['gifs'][a][0]}) - @{data['gifs'][a][1]}" for a in data["gifs"]])
    await ctx.send(embed=Embed(description=desc))


@client.command()
async def ping(ctx):
    await ctx.send('Pong! {0:.2f}ms'.format(client.latency*1000))


@client.command()
async def start_kartus(ctx, *, content):
    global del_chn
    global logs_chn
    global initated
    global guild
    msg = ctx.message
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    if mod not in ctx.author.roles:
        await msg.channel.send("Only Moderators can use this command.")
        return
    try:
        reference = content.strip().split()
        guild = ctx.guild
        del_chn = guild.get_channel(int(reference[0][2:-1]))
        logs_chn = guild.get_channel(int(reference[1][2:-1]))

        data["del_chn"] = int(reference[0][2:-1])
        data["logs_chn"] = int(reference[1][2:-1])
        data["guild"] = int(guild.id)

        with open("DiscordBotStorage.dat", "wb") as f:
            # print(data)
            pickle.dump(data, f)

        await msg.channel.send("Bot Initiated", delete_after=1.0)
        await msg.delete(delay=1)
        initated = True
    except Exception as e:
        print(e)
        await msg.channel.send("Wrong Syntax \n\n> #s1art #deleted_channel #logs_channel", delete_after=3.0)
        return


@client.command()
async def fetchintro(ctx, *content):
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
            member = await client.fetch_user(a)
            name.append(member.name)
            tag.append(member.discriminator)
    channel = await client.fetch_channel(865450006337421383)
    temp_data = ''
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


@client.command()
async def uploadschedule(ctx):
    global data
    if not initated:
        return
    id = ctx.message.author.id
    if id in data["scheduledata"]:
        temp_msg = await ctx.channel.send(f"Schedule for {ctx.message.author.mention} Already Found In DataBase. Do You Want To Update it?")
        tick = "☑️"
        x = "❌"
        await temp_msg.add_reaction(tick)
        await temp_msg.add_reaction(x)

        def check(reaction, user):
            return user == ctx.message.author and reaction.emoji in (tick, x)
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
            if reaction.emoji == x:
                await temp_msg.edit(content="Schedule Unchanged.")
                return
        except asyncio.TimeoutError:
            await temp_msg.edit(content="Schedule Unchanged.")
            return
    if ctx.message.attachments == []:
        aro = await ctx.guild.fetch_member(608276451074113539)
        emb = discord.Embed(title="Schedule Upload",
                            description=f"Drag and Drop The HTML File\n\n[Click Here](https://media.giphy.com/media/iUn97XJCrPO9a5KF1w/source.gif) to View The GIF in a Better Quality\n\nThis bot is still Being Tested, so please dm {aro.mention} if u find bugs\n\nNote:- While Saving the file, Select 'Complete HTML' in the drop down menu. Watch the GIF in a better Quality For Refrence")
        emb.set_image(
            url="https://media.giphy.com/media/iUn97XJCrPO9a5KF1w/giphy.gif")
        temp_msg = await ctx.channel.send(embed=emb)

        def check(m):
            return m.author == ctx.message.author and m.attachments != []
        try:
            msg = await client.wait_for('message', timeout=200, check=check)
        except asyncio.TimeoutError:
            await temp_msg.edit(content="No attachement Found.")
            return
        dat2 = await msg.attachments[0].read()
        await msg.delete()
    else:
        dat2 = await ctx.message.attachments[0].read()
    obj = TTscrap(dat2)
    retrived_data = obj.get_data()
    if retrived_data[0] == "Wrong Format":
        await ctx.channel.send(f"{ctx.author.mention} The File Uploaded wasn't of Supported Format. If the problem Persists ping {aro.mention} with the following error.\n\n```\n{retrived_data[1]}\n```")
        return
    try:
        tempdata = [retrived_data]
        users = [ctx.author.name]
        day = "mon"
        ppschedule_today(tempdata, users, day)
        await ctx.channel.send(f"{ctx.author.mention} Schedule Has Been Succesfully Updated. Debug info- {id}")
        data["scheduledata"][id] = retrived_data
        await client._after_invoke(ctx)
        verified = discord.utils.get(ctx.guild.roles, name="Verified")
        await ctx.author.add_roles(verified)
        await logs_chn.send(embed=Embed(description=f"{ctx.author.mention} Uploaded their schedule"))
    except:
        await ctx.channel.send(f"{ctx.author.mention} Schedule Has Been Succesfully Updated. Debug info- {id}")


@client.command()
async def uwu(ctx, *, content=""):
    if content:
        await ctx.send(uwuify.uwu(content))
    elif ctx.message.reference:
        await ctx.send(uwuify.uwu(ctx.message.reference.cached_message.content))


@client.command()
async def deleteschedule(ctx, user):
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    if len(ctx.message.mentions) >= 2:
        if mod not in ctx.author.roles:
            await ctx.send("Only Mods can delete others schedule.")
            return
        else:
            temp_msg = await ctx.channel.send(f"Schedule for {ctx.message.mentions[1].mention} will be erased from our DataBase. Do You Want To proceed?")
            tick = "☑️"
            x = "❌"
            await temp_msg.add_reaction(tick)
            await temp_msg.add_reaction(x)

            def check(reaction, user):
                return user == ctx.message.author and reaction.emoji in (tick, x)
            try:
                reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
                if reaction.emoji == x:
                    await temp_msg.edit(content="Schedule Unchanged.")
                    return
            except asyncio.TimeoutError:
                await temp_msg.edit(content="Schedule Unchanged.")
                return
            id = ctx.message.mentions[1].id
            del data["scheduledata"][id]
            await temp_msg.edit(content="Schedule erased successfully")
            await logs_chn.send(embed=Embed(description=f"{ctx.message.mentions[1].mention} was erased from the database."))
            return

    temp_msg = await ctx.channel.send(f"Schedule for {ctx.author.mention} will be erased from our DataBase. Do You Want To proceed?")
    tick = "☑️"
    x = "❌"
    await temp_msg.add_reaction(tick)
    await temp_msg.add_reaction(x)

    def check(reaction, user):
        return user == ctx.message.author and reaction.emoji in (tick, x)
    try:
        reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
        if reaction.emoji == x:
            await temp_msg.edit(content="Schedule Unchanged.")
            return
    except asyncio.TimeoutError:
        await temp_msg.edit(content="Schedule Unchanged.")
        return
    id = ctx.author.id
    del data["scheduledata"][id]
    await logs_chn.send(embed=Embed(description=f"{ctx.author.mention} was erased from the database."))
    await temp_msg.edit("Schedule erased successfully")


@client.command()
async def scanschedule(ctx, user=""):
    loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
    if not user:
        id = ctx.author.id
        member = ctx.author
    elif len(ctx.message.mentions) >= 2:
        id = ctx.message.mentions[1].id
        member = ctx.message.mentions[1]
    if id not in data["scheduledata"]:
        await loadgif.edit(content=f"Schedule For {member.mention} Not Found. Upload Your Schedule Using '/uploadschedule' command")
        return
    auth_data = [(a[0].split(" - ")[0], a[2].strip())
                 for a in data["scheduledata"][id] if a[0].split(" - ")[0] != "BMEE103N"]
    # print(auth_data)
    mates = {}

    for member_id in data["scheduledata"]:
        mem = ""
        member_data = [(a[0].split(" - ")[0], a[2].strip())
                       for a in data["scheduledata"][member_id]]
        for course in member_data:
            for row in auth_data:
                if row == course:
                    if not mem:
                        mem = client.get_user(member_id)
                    if row in mates:
                        if mem not in mates[row]:
                            mates[row] += [mem]
                    else:
                        mates[row] = [mem]
                    break

    emb = Embed(
        description=f"Members with same courses as {member.mention} are displayed below.")
    for lst in mates:
        mentions = '\n'.join([a.mention for a in mates[lst]])
        emb.add_field(name=" by ".join(lst), value=f"{mentions}", inline=False)
    emb.set_author(name="Kartus", icon_url=client.user.avatar_url_as())
    emb.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/887988341998514176/893748283791527936/VITC25.png")
    emb.set_footer(icon_url=ctx.author.avatar_url_as(
    ), text=f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
    await loadgif.edit(content="", embed=emb)


@client.command()
async def listschedules(ctx):
    await ctx.send(embed=Embed(title="Members who had uploaded their Schedule.", description="\n".join([client.get_user(a).mention for a in data["scheduledata"]])))


@client.command(aliases=["ws", "wschedule"])
async def weekschedule(ctx, *person):
    loadmsg = await ctx.send("Loading....")
    loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
    if not person:
        member = ctx.author
        id = int(member.id)
        print(id)
    elif person[0][:3] == '<@!':
        id = int(person[0][3:-1])
        print(id)
        member = ctx.message.mentions[1]
    else:
        await loadmsg.delete()
        await loadgif.delete()
        await ctx.channel.send("Wrong Syntax. Mention atleast one Person")
        return
    if id in data["scheduledata"]:
        temp = ppschedule_get(data["scheduledata"][id])
        if temp[0] != "Wrong Format":
            table1, table2, table3 = temp
            member = await ctx.guild.fetch_member(id)
            txt = ''
            txt += f"@{member.name}'s Morning Schedule\n\n{table1}\n\n"
            txt += f"@{member.name}'s Afternoon Schedule\n\n{table2}\n\n"
            txt += f"Keys:-\n\n{table3}"
            font = ImageFont.truetype("CascadiaCode.ttf", 20)
            h, w = font.getsize_multiline(txt, spacing=5)
            difference = 80
            h += difference
            w += difference
            img = Image.new('RGB', (h, w), color=(44, 47, 51))

            draw = ImageDraw.Draw(img)
            draw.multiline_text((difference//2, difference//2), txt,
                                (255, 255, 255), font=font, align="center", spacing=5)
            fp = dt.now().strftime("%M %S.png")
            img.save(fp)
            await loadmsg.delete()
            await loadgif.delete()
            await ctx.send(file=discord.File(fp=fp))
            os.remove(fp)

        else:
            await loadmsg.delete()
            await loadgif.delete()
            aro = await ctx.guild.fetch_member(608276451074113539)
            await ctx.channel.send(f"An error has occured While Retrieving your Data. Contact {aro.mention} with The following Time.\n\n`{dt.now()}`")
    else:
        await loadmsg.delete()
        await loadgif.delete()
        await ctx.channel.send(f"Schedule For {member.mention} Not Found. Upload Your Schedule Using '{client.user.mention} uploadschedule' command")


@client.command(aliases=["ds", "dschedule"])
async def dayschedule(ctx, *content):
    day = ""
    if len(ctx.message.mentions) > 1:
        id = []
        users = []
        for a in content:
            if a[:3] == "<@!":
                id.append(int(a[3:-1]))
        try:
            tempdata = []
            for i in id:
                member = await ctx.guild.fetch_member(i)
                users.append(member.name)
                tempdata.append(data["scheduledata"][i])
        except KeyError:
            await ctx.channel.send(f"Schedule For {member.mention} Not Found. Upload Your Schedule Using '{client.user.mention} uploadschedule' command")

    else:
        member = ctx.author
        id = int(member.id)
        if id not in data["scheduledata"]:
            await ctx.channel.send(f"Schedule For {member.mention} Not Found. Upload Your Schedule Using '{client.user.mention} uploadschedule' command")
            return
        tempdata = [data["scheduledata"][id]]
        users = [ctx.author.name]

    for a in content:
        if len(a) >= 3 and a[:3].lower() in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
            day = a[:3].lower()
            break
    else:
        day = "today"

    temp = ppschedule_today(tempdata, users, day)
    if temp[0] != "Wrong Format":
        table1, table2, table3 = temp
        txt = ''
        txt += f"Morning Schedule\n\n{table1}\n\n"
        txt += f"Afternoon Schedule\n\n{table2}\n\n"
        txt += f"Keys:-\n\n{table3}"
        loadmsg = await ctx.send("Loading....")
        loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
        font = ImageFont.truetype("CascadiaCode.ttf", 20)
        h, w = font.getsize_multiline(txt, spacing=5)
        difference = 80
        h += difference
        w += difference
        img = Image.new('RGB', (h, w), color=(44, 47, 51))

        draw = ImageDraw.Draw(img)
        draw.multiline_text((difference//2, difference//2), txt,
                            (255, 255, 255), font=font, align="center", spacing=5)
        fp = dt.now().strftime("%M %S.png")
        img.save(fp)
        await loadmsg.delete()
        await loadgif.delete()
        await ctx.send(file=discord.File(fp=fp))
        os.remove(fp)
    else:
        aro = await ctx.guild.fetch_member(608276451074113539)
        await ctx.channel.send(f"An error has occured While Retrieving your Data. Contact {aro.mention} with The following Time.\n\n'{dt.now()}'")


@client.event
async def on_raw_message_delete(msg):
    if (msg.cached_message != None):
        chnl = msg.cached_message.guild.get_channel(881697347128668200)
        chnl2 = msg.cached_message.guild.get_channel(891653703629697065)
    global del_chn
    if del_chn != None:
        # add feature to ignore bot command chanel
        if (msg.cached_message != None) and ((msg.cached_message.author == client.user) or (msg.cached_message.content[:6] == "#s1art") or msg.cached_message.channel in (chnl, chnl2)):
            return
        data["total_deleted_msgs"] += 1
        if msg.cached_message == None:
            await del_chn.send(f"a deleted message can't be retrived... ")
        elif msg.cached_message.attachments != []:
            files = []
            for fp in msg.cached_message.attachments:
                content = await fp.read()
                with open(fp.filename, "wb") as f:
                    f.write(content)
                files.append(discord.File(fp.filename))
            await del_chn.send("the following message has been deleted" + "\n\n" + "> " + msg.cached_message.content + f'\n\nChannel => {msg.cached_message.channel}\nAuthor => {msg.cached_message.author}', files=files)
            os.remove(fp.filename)

        else:
            # print(msg.cached_message.content)
            await del_chn.send("the following message has been deleted" + "\n\n" + "> " + msg.cached_message.content + f'\n\nChannel => {msg.cached_message.channel}\nAuthor => {msg.cached_message.author}')


@slash.context_menu(target=ContextMenuType.MESSAGE,
                    name="UwUify",
                    guild_ids=[865211274567483434])
async def slash_uwuify(ctx: MenuContext):
    await ctx.send(
        content=uwuify.uwu(ctx.target_message.content),
        hidden=False
    )


@slash.slash(
    name="uwu",
    description="UwUify your Texts",
    guild_ids=[865211274567483434],
    options=[
         create_option(
             name="text",
             description="Text to UwUify",
             option_type=3,
             required=True
         )
    ]
)
async def slash_uwu(ctx, text):
    await ctx.send(uwuify.uwu(text))


@slash.slash(
    name="UploadSchedule",
    description="Use This Command To Upload your VIT Schedule",
    guild_ids=[865211274567483434]
)
async def slash_uploadschedule(ctx: SlashContext):
    id = ctx.author.id
    temp_msg = None
    if id in data["scheduledata"]:
        temp_msg = await ctx.send(f"Schedule for {ctx.author.mention} Already Found In DataBase. Do You Want To Update it?")
        tick = "☑️"
        x = "❌"
        await temp_msg.add_reaction(tick)
        await temp_msg.add_reaction(x)

        def check(reaction, user):
            return user == ctx.author and reaction.emoji in (tick, x)
        try:
            reaction, user = await client.wait_for('reaction_add', timeout=10.0, check=check)
            if reaction.emoji == x:
                await temp_msg.edit(content="Schedule Unchanged.")
                return
        except asyncio.TimeoutError:
            await temp_msg.edit(content="Schedule Unchanged.")
            return
    aro = await ctx.guild.fetch_member(608276451074113539)
    emb = discord.Embed(title="Schedule Upload",
                        description=f"Drag and Drop The HTML File\n\n[Click Here](https://media.giphy.com/media/iUn97XJCrPO9a5KF1w/source.gif) to View The GIF in a Better Quality\n\nNote:- While Saving the file, Select 'Complete HTML' in the drop down menu. Watch the GIF in a better Quality For Refrence")
    emb.set_image(
        url="https://media.giphy.com/media/iUn97XJCrPO9a5KF1w/giphy.gif")
    if temp_msg:
        await temp_msg.edit(content="", embed=emb)
    else:
        temp_msg = await ctx.send(embed=emb)

    def check(m):
        return m.author == ctx.author and m.attachments != []
    try:
        msg = await client.wait_for('message', timeout=200, check=check)
    except asyncio.TimeoutError:
        await temp_msg.edit(content="No attachement Found.")
        return
    dat2 = await msg.attachments[0].read()
    await msg.delete()
    obj = TTscrap(dat2)
    retrived_data = obj.get_data()
    if retrived_data[0] == "Wrong Format":
        await ctx.channel.send(f"{ctx.author.mention} The File Uploaded wasn't of Supported Format. If the problem Persists ping {aro.mention} with the following error.\n\n")
        return

    try:
        tempdata = [retrived_data]
        users = [ctx.author.name]
        day = "mon"
        ppschedule_today(tempdata, users, day)
        await ctx.channel.send(f"{ctx.author.mention} Schedule Has Been Succesfully Updated. Debug info- {id}")
        data["scheduledata"][id] = retrived_data
        await client._after_invoke(ctx)
        verified = discord.utils.get(ctx.guild.roles, name="Verified")
        await ctx.author.add_roles(verified)
        await logs_chn.send(embed=Embed(description=f"{ctx.author.mention} uploaded their schedule"))
    except:
        await ctx.channel.send(f"{ctx.author.mention} The File Uploaded wasn't of Supported Format. If the problem Persists ping {aro.mention} with the following error.\n\n")


@slash.slash(
    name="weekschedule",
    description="Use This Command To Retrive Weekly Schedule of the mentioned user",
    guild_ids=[865211274567483434],
    options=[
        create_option(
            name="user",
            description="Select User Whose Schedule You Want to View. Leave Empty to return your Schedule.",
            option_type=6,
            required=False
        )
    ]
)
async def slash_weekschedule(ctx: SlashContext, user=""):
    user: discord.User
    loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
    if not user:
        user = ctx.author
    id = user.id
    if id in data["scheduledata"]:
        temp = ppschedule_get(data["scheduledata"][id])
        if temp[0] != "Wrong Format":
            table1, table2, table3 = temp
            txt = ''
            txt += f"@{user.name}'s Morning Schedule\n\n{table1}\n\n"
            txt += f"@{user.name}'s Afternoon Schedule\n\n{table2}\n\n"
            txt += f"Keys:-\n\n{table3}"
            font = ImageFont.truetype("CascadiaCode.ttf", 20)
            h, w = font.getsize_multiline(txt, spacing=5)
            difference = 80
            h += difference
            w += difference
            img = Image.new('RGB', (h, w), color=(44, 47, 51))

            draw = ImageDraw.Draw(img)
            draw.multiline_text((difference//2, difference//2), txt,
                                (255, 255, 255), font=font, align="center", spacing=5)
            fp = dt.now().strftime("%M %S.png")
            img.save(fp)
            # await loadgif.delete()
            await loadgif.edit(content=f"Schedule for @{user.name}", file=discord.File(fp=fp))
            os.remove(fp)

        else:
            # await loadgif.delete()
            aro = await ctx.guild.fetch_member(608276451074113539)
            await loadgif.edit(content=f"An error has occured While Retrieving your Data. Contact {aro.mention} with The following Time.\n\n`{dt.now()}`")
    else:
        # await loadgif.delete()
        await loadgif.edit(content=f"Schedule For {user.mention} Not Found. Upload Your Schedule Using '{client.user.mention} uploadschedule' command")


@slash.slash(
    name="dailyschedule",
    description="Use This Command To Retrive Schedules of the mentioned user for a paticular day",
    guild_ids=[865211274567483434],
    options=[
        create_option(
            name="user",
            description="Select User Whose Daily Schedule You Want to View. Leave Empty to return your Schedule.",
            option_type=6,
            required=False
        ),
        create_option(
            name="day",
            description="Select A Day. Leave Empty for Present Days Schedule",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                    name="Monday",
                    value="mon"
                ),
                create_choice(
                    name="Tuesday",
                    value="tue"
                ),
                create_choice(
                    name="Wednesday",
                    value="wed"
                ),
                create_choice(
                    name="Thursday",
                    value="thu"
                ),
                create_choice(
                    name="Friday",
                    value="fri"
                )
            ]
        )
    ]
)
async def slash_dailyschedule(ctx: SlashContext, user="", day="today"):
    global data
    user: discord.User
    if user:
        member = user
    else:
        member = ctx.author
    id = int(member.id)
    if id not in data["scheduledata"]:
        await ctx.send(f"Schedule For {member.mention} Not Found. Upload Your Schedule Using '{client.user.mention} uploadschedule' command")
        return
    tempdata = [data["scheduledata"][id]]
    users = [member.name]

    if len(day) >= 3 and day[:3].lower() in ("mon", "tue", "wed", "thu", "fri", "sat", "sun"):
        day = day[:3].lower()
    else:
        day = "today"
    temp = ppschedule_today(tempdata, users, day)
    if temp[0] != "Wrong Format":
        table1, table2, table3 = temp
        txt = f"Morning Schedule\n\n{table1}\n\n"
        txt += f"Afternoon Schedule\n\n{table2}\n\n"
        txt += f"Keys:-\n\n{table3}"
        loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
        font = ImageFont.truetype("CascadiaCode.ttf", 20)
        h, w = font.getsize_multiline(txt, spacing=5)
        difference = 80
        h += difference
        w += difference
        img = Image.new('RGB', (h, w), color=(44, 47, 51))

        draw = ImageDraw.Draw(img)
        draw.multiline_text((difference//2, difference//2), txt,
                            (255, 255, 255), font=font, align="center", spacing=5)
        fp = dt.now().strftime("%M %S.png")
        img.save(fp)
        await loadgif.edit(content=f"Schedule for @{member.name}", file=discord.File(fp=fp))
        os.remove(fp)
    else:
        aro = await ctx.guild.fetch_member(608276451074113539)
        await ctx.send(f"An error has occured While Retrieving your Data. Contact {aro.mention} with The following Time.\n\n'{dt.now()} Wrong Format'", hidden=True)


@slash.slash(
    name="help",
    description="How to Kartus 101 :)",
    guild_ids=[865211274567483434],
    options=[
        create_option(
            name="command",
            description="Command",
            option_type=3,
            required=False,
            choices=[
                create_choice(
                        name='uploadschedule',
                        value='uploadschedule'
                ),
                create_choice(
                    name='weekschedule',
                    value='weekschedule'
                ),
                create_choice(
                    name='dayschedule',
                    value='dayschedule'
                ),
                create_choice(
                    name='countmein',
                    value='countmein'
                ),
                create_choice(
                    name='addgif',
                    value='addgif'
                ),
                create_choice(
                    name='listgifs',
                    value='listgifs'
                ),
                create_choice(
                    name='fetchintro',
                    value='fetchintro'
                ),
                create_choice(
                    name='scanschedule',
                    value='scanschedule'
                )
            ]
        )
    ]
)
async def slash_help(ctx: SlashContext, command=""):
    cmd = command
    if not cmd:
        emb = Embed(description="Kartus is VIT-C Student's Clubs Custom-Made Bot.\nYoroshiku Onegaishimasu<:gojo:885934411701440513>",
                    title="Kartus Help", colour=discord.Colour.from_rgb(207, 68, 119))
        emb.add_field(name="Schedule Commands",
                      value="```\nuploadschedule\ndayschedule\nweekschedule```", inline=False)
        emb.add_field(name="CountMeIn",
                      value="```\ncountmein\ncountmein stats```", inline=False)
        emb.add_field(name="GIF Related",
                      value="```\naddgif\nlistgifs```", inline=False)
        emb.add_field(name="Miscellaneous",
                      value="```\nping\nfetchintro```", inline=False)
        emb.set_author(name="Kartus", icon_url=client.user.avatar_url_as())
        emb.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/887988341998514176/893748283791527936/VITC25.png")
        emb.set_footer(icon_url=ctx.author.avatar_url_as(
        ), text=f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=emb)

    else:
        cmd = cmd.split(" ")[0]
        if type(cmds[cmd]) == list:
            emb = Embed(description=cmds[cmd][0], title=cmd,
                        colour=discord.Colour.from_rgb(207, 68, 119))
            emb.add_field(name="Available Commands",
                          value=cmds[cmd][1], inline=False)
            for a, b in cmds[cmd][2]:
                emb.add_field(name=a, value=b, inline=False)
        else:
            emb = Embed(description=cmds[cmd], title=cmd,
                        colour=discord.Colour.from_rgb(207, 68, 119))

        emb.set_author(name="Kartus", icon_url=client.user.avatar_url_as())
        emb.set_thumbnail(
            url="https://cdn.discordapp.com/attachments/887988341998514176/893748283791527936/VITC25.png")
        emb.set_footer(icon_url=ctx.author.avatar_url_as(
        ), text=f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
        await ctx.send(embed=emb)


@slash.slash(
    name="addgif",
    description="This Command assigns a GIF to a keyword.",
    guild_ids=[865211274567483434],
    options=[
        create_option(
            name="keyword",
            description="Keyword to assign to GIF",
            option_type=3,
            required=True
        ),
        create_option(
            name="gif",
            description="Link to GIF",
            option_type=3,
            required=True
        )
    ]
)
async def slash_addgif(ctx, keyword, gif):
    commands = [a.name for a in client.commands]
    mod = discord.utils.get(ctx.guild.roles, name="Moderator")
    author = ctx.author
    if keyword in commands:
        await ctx.send(f"`{keyword}` is a Command Used by the Bot. Try Again With a Different Keyword")
        return
    elif keyword in data["gifs"] and mod not in author.roles:
        await ctx.send(f"Keyword `{keyword}` is in use. Request a Moderator to change the gif for the Designated keyword.")
        return
    if "https://" in gif and "gif" in gif:
        data["gifs"][keyword.lower()] = [gif, ctx.author.name]
        embed = Embed(description="Gif Has Been Successfully Added",
                      colour=discord.Colour.from_rgb(207, 68, 119))
        await ctx.send(embed=embed)
        await logs_chn.send(embed=Embed(description=f"{ctx.author.mention} added a GIF to a keyword `{keyword}`"))
        await client._after_invoke(ctx)
    else:
        await ctx.send("Wrong Format! @Kartus addgif <keyword> <gif link>")


@slash.slash(
    name="listgifs",
    description="This Command Retrives Existing GIFs with its Respective Keyword and Creator.",
    guild_ids=[865211274567483434]
)
async def slash_listgifs(ctx):
    desc = "\n".join(
        [f"[{a}]({data['gifs'][a][0]}) - @{data['gifs'][a][1]}" for a in data["gifs"]])
    await ctx.send(embed=Embed(description=desc))


@slash.slash(
    name="invite",
    description="Invite your fellow VITians!",
    guild_ids=[865211274567483434]
)
async def slash_fetchinvite(ctx):
    await ctx.send("Here You Go!\n\nhttps://discord.gg/K5UMjshn63")


@slash.slash(
    name="fetchintro",
    description="This Command Searches and returns introduction of the mentioned users from the #intro",
    guild_ids=[865211274567483434],
    options=[
        create_option(
            name="user",
            description="Select User Whose Intro You Want to View.",
            option_type=6,
            required=True
        )]
)
async def slash_fetchintro(ctx: SlashContext, user=""):
    loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
    if not user:
        user = ctx.author
    name = [user.name]
    tag = [user.discriminator]
    channel = await client.fetch_channel(865450006337421383)
    temp_data = ''
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

    await loadgif.edit(content=temp_data)


@slash.slash(
    name="scanschedule",
    description="Scans your schedule and finds members with common courses. Connecting VITians :)",
    guild_ids=[865211274567483434],
    options=[
        create_option(
            name="user",
            description="User",
            option_type=6,
            required=False
        )
    ]
)
async def slash_scanschedule(ctx: SlashContext, user=""):
    loadgif = await ctx.send("https://tenor.com/view/rikka-rolling-hand-gif-5040472")
    if not user:
        id = ctx.author.id
        member = ctx.author
    else:
        id = user.id
        member = user
    if id not in data["scheduledata"]:
        await loadgif.edit(content=f"Schedule For {member.mention} Not Found. Upload Your Schedule Using '/uploadschedule' command")
        return
    try:
        auth_data = [(a[0].split(" - ")[0], a[2].strip())
                     for a in data["scheduledata"][id] if a[0].split(" - ")[0] != "BMEE103N"]
    except:
        await loadgif.edit(content=f"Your schedule is not compatible with {client.mention}.")
        await logs_chn.send(embed=Embed(description=f"{ctx.author.mention} has faced an Error. [Message Link]({loadgif.jump_url})"))
    # print(auth_data)
    mates = {}

    for member_id in data["scheduledata"]:
        mem = ""
        try:
            member_data = [(a[0].split(" - ")[0], a[2].strip())
                           for a in data["scheduledata"][member_id]]
        except Exception as e:
            await logs_chn.send(embed=Embed(description=f"Error Occured While Scaning {client.get_user(member_id).mention}'s Schedule\n\n`{e}`"))
        for course in member_data:
            for row in auth_data:
                if row == course:
                    if not mem:
                        mem = client.get_user(member_id)
                    if row in mates:
                        if mem not in mates[row]:
                            mates[row] += [mem]
                    else:
                        mates[row] = [mem]
                    break

    emb = Embed(
        description=f"Members with same courses as {member.mention} are displayed below.")
    for lst in mates:
        mentions = '\n'.join([a.mention for a in mates[lst]])
        emb.add_field(name=" by ".join(lst), value=f"{mentions}", inline=False)
    emb.set_author(name="Kartus", icon_url=client.user.avatar_url_as())
    emb.set_thumbnail(
        url="https://cdn.discordapp.com/attachments/887988341998514176/893748283791527936/VITC25.png")
    emb.set_footer(icon_url=ctx.author.avatar_url_as(
    ), text=f"Requested By {ctx.author.name}#{ctx.author.discriminator}")
    await loadgif.edit(content="", embed=emb)


v_cooldown = dt.now(timezone("Asia/Kolkata")) - timedelta(minutes=5)


@slash.slash(
    name="pingvcmembers",
    description="Kartus pings all the members in the voice channel your currently in.",
    guild_ids=[865211274567483434]
)
async def slash_pingvcmembers(ctx: SlashContext):
    global v_cooldown
    if ctx.author.voice:
        verified = discord.utils.get(ctx.guild.roles, name="Moderator")
        if verified in ctx.author.roles:
            cooldown = dt.now(timezone("Asia/Kolkata")) - v_cooldown
            if cooldown > timedelta(minutes=5):
                await ctx.send(" ".join([a.mention for a in ctx.author.voice.channel.members]))
                v_cooldown = dt.now(timezone("Asia/Kolkata"))
                await logs_chn.send(embed=Embed(description=f"{ctx.author.mention} pinged {len(ctx.author.voice.channel.members)} members in a VC"))
            else:
                s = cooldown.seconds
                await ctx.send(f"This Comand is on Cooldown. Wait For {4 - (s//60)} mins {60-(s%60)} secs.", hidden=True)
        else:
            await ctx.send(f"Only Mods are able to use this command.")
    else:
        await ctx.send("You are not connected to a voice channel.", hidden=True)

client.run(os.getenv('TOKEN'))
# client.run("")
