import sqlite3
from typing import DefaultDict
from bs4 import BeautifulSoup
import discord
from discord.ext import commands
from discord.message import Attachment
import discord_components
from discord_components import component, Select, SelectOption
from discord_components import client
from discord_components.component import Button, ButtonStyle
import asyncio
from discord_components.interaction import Interaction
from datetime import datetime
import csv
from difflib import SequenceMatcher as SM

# Relative Import
from cogs.Resources import selects_for_course  # import w.r.t CWD

"""
location for selects_course is kartus/main/cogs/Resources/selects_for_course.py
contains Select Options for Course selection during signup
"""


THUMBNAIL_URL = "https://cdn.discordapp.com/attachments/872059879379050527/889749015938334730/Copy_of_VITC25.png"


def format_timetable_row(lis: list, client_id: int, semester_list: list):
    for semester_id in semester_list:
        if (
            semester_id["value"]
            and semester_id["value"] == lis[6][: len(semester_id["value"])]
        ):
            break

    return [
        client_id,
        lis[2].split(" - ")[0],
        lis[2].split(" - ")[1],
        lis[3],
        lis[6],
        ",".join(lis[7].replace(" - ", "").split("+")),
        lis[8],
        lis[9].replace(" - ", ""),
        lis[10],
        semester_id["value"],
        semester_id.text,
        0
    ]

def embedded_course_check(row_data:list):
    data = DefaultDict(lambda: 0)
    for row in row_data:
        data[row[1]] += 1
    for row in row_data:
        row[11] = data[row[1]]
    return row_data


async def notify_devs(client:discord.Client,dm,regno,registernumber,fullname,csv_fullname,ratio=0):
    logs_chnl = client.get_channel(910108806254579722)
    await dm.send(
        embed = discord.Embed(
            title = "Your sign-up attempt has been queued.",
            description = "Verifying signup details might take a while. You'll be notified once it's done!"
        ).set_footer(text="You will not recieve any response if your details seem suspicious/fake.")
    )
    msg = await logs_chnl.send(embed = discord.Embed(
        description = f"User Tried Signup {client.aro.mention}. Details are as follows.\nEntered Name: - {fullname}\nFullname from CSV:- {csv_fullname}\nEntered Reg No:- {regno}\nRoll No in HTML:- {registernumber}\nRatio:- {ratio}"
    ))
    await msg.add_reaction(tick := "☑️")
    await msg.add_reaction(x := "❌")
    reaction , user = await client.wait_for("reaction_add",timeout=None,check = lambda m,u:u.id == 608276451074113539)
    if str(reaction.emoji) == "☑️":
        await msg.edit(content = "verified! ☑️")
        return True
    else:
        await msg.edit(content = "not verified ❌")
        return False

class SetupCommands(commands.Cog):

    # Initialization
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cursor: sqlite3.Connection = client.cursor

    @commands.command(name="signup")
    async def signup_with_schedule(self, ctx: commands.Context):

        data = self.cursor.execute(  # checks if user has already signed up
            f"SELECT COUNT(*) FROM client_info \
            WHERE client_id = '{ctx.author.id}'"
        ).fetchone()

        if data != (0,):
            await ctx.send(
                embed=discord.Embed(
                    title="Already signed up",
                    description="You have already signed up before. If you have made a mistake during signup then please dm the bot and we will get back to you.",
                    colour=discord.Colour.from_rgb(207, 68, 119),
                )
            )
            return

        dm: discord.TextChannel = await ctx.author.create_dm()
        dm = ctx.channel
        embed = discord.Embed(
            title="👋🏻 Hello from Team Kartus!",
            description="We would like to let you know data collected through Kartus will be stored safely and your privacy will not be compromised.",
            colour=discord.Colour.from_rgb(207, 68, 119),
        )

        embed.add_field(
            name="Data Collected By Kartus will include your",
            value=("⭐ Full Name\n" "⭐ Registration Number\n" "⭐ Registered Courses"),
            inline=False,
        )

        embed.add_field(
            name="Collected Data will be used to",
            value=(
                "⭐ Find Peers with similar Courses\n"
                "⭐ Conduct a short survey to rate faculties\n"
                "⭐ To View or Add Faculties to Blacklist/Whitelist \n"
                "⭐ Notify before a class starts (optional)"
            ),
            inline=False,
        )

        embed.set_thumbnail(url=THUMBNAIL_URL)

        try:
            # Try sending dm, or request to enable "server members dm option"
            await dm.send(
                embed=embed,
                components=[
                    [
                        Button(
                            label="Proceed", custom_id="agree", style=ButtonStyle.green
                        ),
                        Button(
                            label="Cancel Signup",
                            custom_id="disagree",
                            style=ButtonStyle.red,
                        ),
                    ]
                ],
            )
        except discord.errors.Forbidden:
            """
            ask users to enable messages from server members option in settings
            """
            await ctx.send(
                embed=discord.Embed(
                    description="Enable messages from server members in settings to sign-up.",
                    image_url="https://cdn.discordapp.com/attachments/885410368015446097/907901692836741120/unknown.png",
                )
            )
            return

        interaction = await self.client.wait_for(
            "button_click", check=lambda b: b.custom_id in ("agree", "disagree")
        )  # waits for agree and disagree buttons

        await interaction.disable_components()  # disables components after button click
        if interaction.custom_id == "disagree":
            await dm.send(
                embed=discord.Embed(
                    title="Signup Canceled.",
                    colour=discord.Colour.from_rgb(207, 68, 119),
                )
            )
            return  # returns if disagreed

        data = {}

        fullname_msg: discord.Message = await dm.send(
            embed=discord.Embed(
                title="Enter your full name below.",
                colour=discord.Colour.from_rgb(207, 68, 119),
            )
        )
        message = await self.client.wait_for(
            "message", check=lambda m: m.author == ctx.author and m.channel == dm
        )
        FULL_NAME = message.content.strip().title()  # capitalize each word
        await fullname_msg.edit(
            embed=discord.Embed(
                title=f"Name: {FULL_NAME}",
                colour=discord.Colour.from_rgb(207, 68, 119),
            )
        )
        data["name"] = FULL_NAME

        regno_msg: discord.Message = await dm.send(
            embed=discord.Embed(
                title="Enter your registration number below ",
                colour=discord.Colour.from_rgb(207, 68, 119),
            )
        )
        message = await self.client.wait_for(
            "message", check=lambda m: m.author == ctx.author and m.channel == dm
        )
        REG_NO = message.content.strip().upper()  # capitalize each word
        await regno_msg.edit(
            embed=discord.Embed(
                title=f"Registration number: {REG_NO}",
                colour=discord.Colour.from_rgb(207, 68, 119),
            )
        )
        data["regno"] = REG_NO

        await dm.send(
            embed=discord.Embed(
                title="Select your Campus", colour=discord.Colour.from_rgb(207, 68, 119)
            ),
            components=[
                Select(
                    placeholder="Campus Goes Here",
                    options=[
                        SelectOption(value="Vellore", label="Vellore"),
                        SelectOption(value="Chennai", label="Chennai"),
                    ],
                )
            ],
        )
        interaction = await self.client.wait_for("select_option")
        branch = interaction.values[0]  # retrieves selected value
        data["campus"] = branch
        """
        Refer the Structure of /kartus/main/cogs/Resources/selects_for_course.py
        to fully understand how lines 202 - 237 are executed.
        start from selects_for_course.select_options (line 720)
        Fold to level 3 for easier readability
        """

        emb = discord.Embed(
            title="Select your degree", colour=discord.Colour.from_rgb(207, 68, 119)
        )
        emb.add_field(name="Campus", value=f"{branch}")
        await interaction.respond(
            embed=emb, components=selects_for_course.select_options["Degree"], type=7
        )
        interaction = await self.client.wait_for("select_option")
        degree = interaction.values[0]
        data["degree"] = degree
        emb.add_field(name="Pursuing Degree", value=f"{degree}")

        if stream_components := selects_for_course.select_options[branch]["stream"][
            degree
        ]:
            """
            for chennai there are to streams for integrated courses,
            so selects_for_course.select_options["Chennai"]["stream"]["Integrated"] is []
            and directly moves to course selection
            """
            emb.title = "Select your Stream"
            await interaction.respond(embed=emb, components=stream_components, type=7)
            interaction = await self.client.wait_for("select_option")
            stream = interaction.values[0]
            emb.add_field(name="Stream", value=f"{stream}")
        else:
            stream = degree

        data["stream"] = stream
        emb.title = "Select your Course"
        await interaction.respond(
            embed=emb,
            components=selects_for_course.select_options[branch]["program"][degree][
                stream
            ],
            type=7,
        )
        interaction = await self.client.wait_for("select_option")
        course = interaction.values[0].replace(" spc.", " specialisation")
        emb.add_field(name="Course Name", value=f"{course}\n")
        emb.title = "Course Details"
        await interaction.respond(embed=emb, components=[], type=7)
        data["CourseName"] = course

        emb = discord.Embed(
            title="Upload Courses List",
            description=(
                "Upload the list of courses you've undertaken at VIT. "
                "This list will be used for finding connections and collecting information about facuties at VIT. "
                "Uploading your schedule to kartus means that you agree to take a survey every once in two months, "
                "where you will be allowed to rate/blacklist/whitelist your faculties. Try using a browser to upload. "
                "If the browser method dosen't work then try using an browser extension. If you are a linux user, you "
                "are recommended to download the extension to save the HTML file. "
            ),
            colour=discord.Colour.from_rgb(207, 68, 119),
        )
        emb.set_thumbnail(url=THUMBNAIL_URL)

        components = [
            [
                Button(label="Use Browser", custom_id="chrome", style=ButtonStyle.blue),
                Button(
                    label="Use Extension", custom_id="linux", style=ButtonStyle.blue
                ),
            ]
        ]

        msg = await dm.send(embed=emb, components=components)
        while True:

            (
                done,
                pending,
            ) = await asyncio.wait(  # waits for both attachment uploads and attachments for safety.. ppl tend to mess up here
                [
                    self.client.wait_for("message", check=lambda m: m.attachments),
                    self.client.wait_for(
                        "button_click",
                        check=lambda inter: inter.custom_id in ("chrome", "linux"),
                    ),
                ],
                return_when=asyncio.FIRST_COMPLETED,  # returns first action
                timeout=600,  # 10 mins
            )
            if not done:  # timeout
                for a in components[0]:
                    a.set_disabled(True)
                emb.title = "Signup Canceled"
                await msg.edit(embed=emb, components=components)
                return

            payload = done.pop().result()
            if isinstance(payload, discord.Message):
                await msg.reply(
                    embed=discord.Embed(
                        title="Select a method to upload",
                        colour=discord.Colour.from_rgb(207, 68, 119),
                    )
                )
                continue
            interaction = payload

            if interaction.custom_id == "linux":
                cur_emb = discord.Embed(
                    title="Upload Courses List",
                    description=(
                        "🎈 Click on the link above and install the extension.\n"
                        "🎈 Sign-In into VTop and go to the time table page.\n"
                        "🎈 Click on the Installed extension and save the HTML file.\n"
                        "🎈 Drag and Drop the Saved HTML Below. "
                    ),
                    colour=discord.Colour.from_rgb(207, 68, 119),
                ).set_thumbnail(url=THUMBNAIL_URL)
                cur_components = [
                    [
                        Button(label="Go Back"),
                        Button(
                            label="extension Link",
                            style=ButtonStyle.URL,
                            url="https://chrome.google.com/webstore/detail/save-page-we/dhhpefjklgkmgeafimnjhojgjamoafof",
                        ),
                    ]
                ]

            else:
                cur_emb = (
                    discord.Embed(
                        title="Upload Courses List",
                        description=(
                            "🎈 Open Vtop and go to the Time Table page.\n"
                            "🎈 Right Click and select Save As.\n"
                            "🎈 In the Drop Down, select 'Webpage, Complete' and save it.\n"
                            "🎈 Drag and Drop the Saved HTML Below.\n"
                            "🎈 [Watch the GIF in a better clarity](https://youtu.be/9ZQ3xF5JiFQ) for a clear walkthrough."
                        ),
                        colour=discord.Colour.from_rgb(207, 68, 119),
                    )
                    .set_thumbnail(url=THUMBNAIL_URL)
                    .set_image(
                        url="https://media.giphy.com/media/MaDJCDpvjw3zIWnYdc/giphy-downsized-large.gif"
                    )
                )
                cur_components = [Button(label="Go Back")]

            await interaction.respond(embed=cur_emb, components=cur_components, type=7)
            while True:
                (
                    done,
                    pending,
                ) = await asyncio.wait(  # waits for both attachment uploads and "go back" button click
                    [
                        self.client.wait_for("message", check=lambda m: m.attachments),
                        self.client.wait_for("button_click"),
                    ],
                    return_when=asyncio.FIRST_COMPLETED,  # returns first action
                    timeout=600,  # 10 mins
                )
                if not done:  # if timeout
                    for a in cur_components[0]:
                        a.set_disabled(True)  # disable all components in current embed
                    cur_emb.title = "Sign-up Canceled (Time-Out)"
                    await msg.edit(embed=cur_emb, components=cur_components)
                    return
                payload = done.pop().result()
                if isinstance(
                    payload, discord_components.interaction.Interaction
                ):  # if payload is "go back" then payload is an instance of interaction
                    await payload.respond(embed=emb, components=components, type=7)
                    break
                else:
                    attachment_data = await payload.attachments[0].read()
                    try:
                        html_parser = BeautifulSoup(
                            attachment_data.decode("UTF-8"), "html.parser"
                        )
                    except UnicodeDecodeError:
                        new_emb = emb.copy()
                        new_emb.title = "Oops! You have uploaded the Wrong HTML!"
                        new_emb.description = f"Try using the other method or contact {self.client.aro.mention} if the error persists.\n\n"
                        await payload.reply(embed=new_emb)
                        continue
                    
                    tables = html_parser.find_all("table")
                    n = html_parser.find_all("h3", attrs={"class": "box-title"})
                    if (not n) or not (
                        n[0].text
                        == "Time Table"  # contains <h3 class="box-title">Time Table</h3>
                        and tables
                    ):
                        new_emb = emb.copy()
                        new_emb.title = "Oops! You have uploaded the Wrong HTML!"
                        new_emb.description = f"Try using the other method or contact {self.client.aro.mention} if the error persists.\n\n"
                        await payload.reply(embed=new_emb)
                        continue

                    semester_list = html_parser.find(
                        "select", attrs={"class": "form-control"}
                    ).find_all("option")

                    registernumber = html_parser.find(
                        "a", attrs={"class":"dropdown-toggle small"}
                    ).find_all("span")[1].text.split("(")[0]
                    
                    # FULL_NAME 
                    # REG_NO
                    verified = False
                    csv_name = "None"
                    ratio = 0
                    if REG_NO == registernumber:
                        with open(data_file_location,"r",encoding="UTF-8") as f:
                            reader = csv.reader(f)
                            for row in reader:
                                if row:
                                    if row[1] == REG_NO:
                                        ratio = SM(None,row[0].lower(),FULL_NAME.lower()).ratio() * 100
                                        csv_name = row[0]
                                        if ratio > 50:
                                            verified = True                                            
                                        break
                    
                    if not verified:
                        if not await notify_devs(self.client,dm,REG_NO,registernumber,FULL_NAME,csv_name,ratio):
                            return
                    else:
                        await dm.send(f"verified {REG_NO,FULL_NAME,csv_name,ratio}")

                    rows = tables[0].find_all("tr")
                    filtered_rows = list(
                        filter(
                            None, [rows[b].find_all("td") for b in range(1, len(rows))]
                        )
                    )[:-1]
                    row_data = []
                    for row in filtered_rows:
                        row = [s.text for r in row for s in r.find_all("p")]
                        row = format_timetable_row(
                            row, ctx.author.id, semester_list=semester_list
                        )
                        row_data.append(row)
                    semester_id = row_data[0][9]
                    semester_name = row_data[0][10]
                    row_data = embedded_course_check(row_data)

                    tables = html_parser.find_all("table")
                    table = tables[1]
                    unfiltered_rows = table.find_all("tr")
                    filtered_rows = [row.find_all("td") for row in unfiltered_rows]
                    filtered_rows_with_txt = [[ element.text for element in row if element!="\n"] for row in unfiltered_rows]
                    l1 = filtered_rows_with_txt[4:]
                    i = len(l1)
                    l2 = [l1[a][1:] if a%2 else l1[a][2:] for a in range(i)]
                    l3 = [[ "" if len(element) < 5 else (element.split("-")+["LAB"] if c%2 else element.split("-")) for element in l2[c] if element.lower()!="lunch"] for c in range(len(l2))]
                    cells_count = len(l3[0])
                    final_table_data = [ [(l3[a][b] or l3[a+1][b]) for b in range(cells_count)] for a in range(0,len(l3),2)]

                    self.cursor.execute(
                        f"""INSERT INTO current_semester
                        values(
                            '{ctx.author.id}',
                            '{semester_id}',
                            '{semester_name}'
                        )
                        """
                    )
                    self.cursor.execute(
                        f"""INSERT INTO guild_client_info(client_id)
                        values('{ctx.author.id}')
                        """
                    )
                    guild_ids = self.cursor.execute(
                        f"""SELECT guild_id FROM guilds_info"""
                    ).fetchall()
                    mutual_guild_ids = [a.id for a in ctx.author.mutual_guilds]
                    guild_ids = [
                        f"`{id[0]}` = 'joined'"
                        for id in guild_ids
                        if int(id[0]) in mutual_guild_ids
                    ]
                    self.cursor.execute(
                        f"""UPDATE guild_client_info
                        SET {", ".join(guild_ids)}
                        WHERE client_id = "{ctx.author.id}"
                        """
                    )

                    faculty_list = set([a[7] for a in row_data if a[8] != "ACAD"])
                    data_for_rate = [
                        (a, ctx.author.id, semester_id, datetime.now())
                        for a in faculty_list
                    ]
                    self.cursor.executemany(
                        f"""INSERT INTO client_faculty_rate(
                            faculty_name,
                            client_id,
                            semester_id,
                            day_voted
                        )
                        VALUES(?,?,?,?)
                        """,
                        data_for_rate,
                    )
                    self.cursor.execute(
                        f"""INSERT INTO vote_notify(
                            client_id
                        ) values (
                            {ctx.author.id}
                        )
                        """
                    )
                    
                    self.cursor.execute(
                        f"""INSERT INTO client_info values(
                            "{ctx.author.id}",
                            "{data["campus"]}",
                            "test",
                            "{data["stream"]}",
                            "{data["CourseName"]}",
                            "{data["name"]}",
                            "{data["regno"]}"
                        )
                        """
                    )
                    
                    self.cursor.executemany(
                        f"""INSERT INTO schedule_data values(
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?,
                            ?
                        )
                        """,
                        row_data
                    )

                    schedule_details = [[row[a].strip() for a in (1,2,3,5,7)] for row in row_data if row[6] != "NIL"]

                    
                    self.cursor.commit()
                    await dm.send(
                        embed=discord.Embed(
                            title="Course list uploaded successfully!",
                            description=str(row_data),
                            colour=discord.Colour.from_rgb(207, 68, 119),
                        ).set_thumbnail(url=THUMBNAIL_URL)
                    )


                    # invoke rate
                    return


def setup(bot):
    bot.add_cog(SetupCommands(bot))
