import sqlite3
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

# Relative Import
from cogs.Resources import selects_for_course  # import w.r.t CWD

"""
location for selects_course is kartus/main/cogs/Resources/selects_for_course.py
contains Select Options for Course selection during signup
"""


thumbnail_url = "https://cdn.discordapp.com/attachments/872059879379050527/889749015938334730/Copy_of_VITC25.png"


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
        lis[6],
        ",".join(lis[7].replace(" - ", "").split("+")),
        lis[8],
        lis[9].replace(" - ", ""),
        lis[10],
        semester_id["value"],
        semester_id.text,
    ]


class SetupCommands(commands.Cog):

    # Initialization
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cursor: sqlite3.Connection = client.cursor

    @commands.command(name="signup")
    async def signup_with_schedule(self, ctx: commands.Context):
        cur_sem = self.cursor.execute(  # Not fully built, ignore for now
            "SELECT value FROM common_keys\
            WHERE key = 'current_sem'"
        ).fetchone()
        if cur_sem:
            cur_sem = cur_sem[0]

        data = self.cursor.execute(  # checks if user has already signed up
            f"SELECT COUNT(*) FROM client_info \
            WHERE client_id = '{ctx.author.id}'"
        ).fetchone()

        if data != (0,):
            # already exists for current semester ask for re_signup?
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

        embed.set_thumbnail(url=thumbnail_url)

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
        emb.set_thumbnail(url=thumbnail_url)

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
            # try:
            #     interaction: Interaction = await self.client.wait_for(
            #         "button_click",
            #         check=lambda inter: inter.custom_id in ("chrome", "linux"),
            #         timeout=300,
            #     )
            # except asyncio.TimeoutError:
            #     for a in components[0]:
            #         a.set_disabled(True)
            #     emb.title = "Signup Canceled"
            #     await msg.edit(embed=emb, components=components)
            #     return

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
                ).set_thumbnail(url=thumbnail_url)
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
                    .set_thumbnail(url=thumbnail_url)
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
                    html_parser = BeautifulSoup(
                        attachment_data.decode("UTF-8"), "html.parser"
                    )
                    tables = html_parser.find_all("table")
                    n = html_parser.find_all("h3", attrs={"class": "box-title"})
                    if (not n) or not (
                        n[0]
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

                    await dm.send(
                        embed=discord.Embed(
                            title="Course list uploaded successfully!",
                            description=str(row_data),
                            colour=discord.Colour.from_rgb(207, 68, 119),
                        )
                    )
                    return


def setup(bot):
    bot.add_cog(SetupCommands(bot))
