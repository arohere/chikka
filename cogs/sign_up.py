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
from cogs.Resources import selects_for_course  # import w.r.t main.py

thumbnail_url = "https://cdn.discordapp.com/attachments/872059879379050527/889749015938334730/Copy_of_VITC25.png"


# def fetch_required_data(file_data : bytes):
#     html_parser = BeautifulSoup(file_data.decode("UTF-8"))


def format_timetable_row(lis: list, client_id: int, semester_list: int):
    for semester_id in semester_list:
        if (
            semester_id["value"]
            and semester_id["value"] == lis[6][: len(semester_id["value"])]
        ):
            break
    else:
        print(lis[6][: len(semester_id["value"])])
        print(semester_id)
        print("error")

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


class setup_commands(commands.Cog):

    # Initialization
    def __init__(self, client) -> None:
        self.client: commands.Bot = client
        self.cursor: sqlite3.Connection = client.cursor

    @commands.command(name="signup")
    async def signup_with_schedule(self, ctx: commands.Context):
        """
        check if user schedule already in table
        check if schedule exists for current semester
        """
        # cur_sem = self.cursor.execute("SELECT value FROM common_keys WHERE key = 'current_sem'").fetchone()[0]
        # data = self.cursor.execute(f"SELECT COUNT(*) FROM schedule_data WHERE client_id = '{ctx.author.id}'' AND semester_id = '{cur_sem}' ").fetchone()
        # if data:
        #     # already exists for current semester re_signup?
        #     return
        # dm = await ctx.author.create_dm()
        # dm : discord.TextChannel = self.client.get_channel(905886505770303488)
        dm = ctx.channel

        embed = discord.Embed(
            title="👋🏻 Hello from Team Kartus!",
            description="We would like to let you know data collected through Kartus will be stored safely and your privacy will not be compromised.",
            colour=discord.Colour.from_rgb(207, 68, 119),
        )

        embed.add_field(
            name="Data Collected By Kartus will include your",
            value="⭐ Full Name\n⭐ Registration Number\n⭐ Registered Courses",
            inline=False,
        )

        embed.add_field(
            name="Collected Data will be used to",
            value="⭐ Find Peers with similar Courses\n⭐ Conduct a short survey to rate faculties\n⭐ To View or Add Faculties to Blacklist/Whitelist \n⭐ Notify before a class starts (optional)",
            inline=False,
        )

        embed.set_thumbnail(url=thumbnail_url)

        try:
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
            # request them to enable server members text
            pass

        interaction = await self.client.wait_for(
            "button_click", check=lambda b: b.custom_id in ("agree", "disagree")
        )
        await interaction.disable_components()
        if interaction.custom_id == "disagree":
            await dm.send(
                embed=discord.Embed(
                    title="Signup Canceled.",
                    colour=discord.Colour.from_rgb(207, 68, 119),
                )
            )
            return

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
        await fullname_msg.edit(
            embed=discord.Embed(
                title=f"Name: {message.content.strip()}",
                colour=discord.Colour.from_rgb(207, 68, 119),
            )
        )
        data["name"] = message.content.strip()

        regno_msg: discord.Message = await dm.send(
            embed=discord.Embed(
                title="Enter your registration number below ",
                colour=discord.Colour.from_rgb(207, 68, 119),
            )
        )
        message = await self.client.wait_for(
            "message", check=lambda m: m.author == ctx.author and m.channel == dm
        )
        await regno_msg.edit(
            embed=discord.Embed(
                title=f"Registration number: {message.content.strip()}",
                colour=discord.Colour.from_rgb(207, 68, 119),
            )
        )
        data["regno"] = message.content.strip()

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
        branch = interaction.values[0]

        emb = discord.Embed(
            title="Select your degree", colour=discord.Colour.from_rgb(207, 68, 119)
        )
        emb.add_field(name=f"Branch", value=f"{branch}\n")
        await interaction.respond(
            embed=emb, components=selects_for_course.select_options["Degree"], type=7
        )
        interaction = await self.client.wait_for("select_option")
        degree = interaction.values[0]
        emb.add_field(name=f"Pursuing Degree", value=f"{degree}\n")

        if stream_components := selects_for_course.select_options[branch]["stream"][
            degree
        ]:
            emb.title = "Select your Stream"
            await interaction.respond(embed=emb, components=stream_components, type=7)
            interaction = await self.client.wait_for("select_option")
            stream = interaction.values[0]
            emb.add_field(name=f"Stream", value=f"{stream}\n")
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
        emb.add_field(name=f"Course Name", value=f"{course}\n")
        emb.title = "Course Details"
        await interaction.respond(embed=emb, components=[], type=7)
        data["CourseName"] = course

        emb = discord.Embed(
            title="Upload Courses List",
            description="Upload the list of courses you've undertaken at VIT. This list will be used for finding connections and collecting information about facuties at VIT. Uploading your schedule to kartus means that you agree to take a survey every once in two months, where you will be allowed to rate/blacklist/whitelist your faculties. Try using a browser to upload. If the browser method dosen't work then try using an browser extension. If you are a linux user, you are recommended to download the extension to save the HTML file. ",
            colour=discord.Colour.from_rgb(207, 68, 119),
        )
        emb.set_thumbnail(url=thumbnail_url)

        components = [
            [
                Button(label="Use Browser", custom_id="chrome", style=ButtonStyle.blue),
                Button(
                    label="Use extension", custom_id="linux", style=ButtonStyle.blue
                ),
            ]
        ]

        msg = await dm.send(embed=emb, components=components)
        while True:
            try:
                interaction: Interaction = await self.client.wait_for(
                    "button_click",
                    check=lambda inter: inter.custom_id in ("chrome", "linux"),
                    timeout=300,
                )
            except asyncio.TimeoutError:
                for a in components[0]:
                    a.set_disabled(True)
                emb.title = "Signup Canceled"
                await msg.edit(embed=emb, components=components)
                return

            if interaction.custom_id == "linux":
                cur_emb = discord.Embed(
                    title="Upload Courses List",
                    description="🎈 Click on the link above and install the extension.\n🎈 Sign-In into VTop and go to the time table page.\n🎈 Click on the Installed extension and save the HTML file.\n🎈 Drag and Drop the Saved HTML Below. ",
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
                        description="🎈 Open Vtop and go to the Time Table page.\n🎈 Right Click and select Save As.\n🎈 In the Drop Down, select 'Webpage, Complete' and save it.\n🎈 Drag and Drop the Saved HTML Below.\n🎈 [Watch the GIF in a better clarity](https://youtu.be/9ZQ3xF5JiFQ) for a clear walkthrough.",
                        colour=discord.Colour.from_rgb(207, 68, 119),
                    )
                    .set_thumbnail(url=thumbnail_url)
                    .set_image(
                        url="https://media.giphy.com/media/MaDJCDpvjw3zIWnYdc/giphy-downsized-large.gif"
                    )
                )
                cur_components = [Button(label="Go Back")]

            await interaction.respond(embed=cur_emb, components=cur_components, type=7)

            done, pending = await asyncio.wait(
                [
                    self.client.wait_for("message", check=lambda m: m.attachments),
                    self.client.wait_for("button_click"),
                ],
                return_when=asyncio.FIRST_COMPLETED,
                timeout=600,
            )
            if not done:
                for a in cur_components[0]:
                    a.set_disabled(True)
                await msg.edit(embed=cur_emb, components=cur_components)
                return
            payload = done.pop().result()
            if isinstance(payload, discord_components.interaction.Interaction):
                await payload.respond(embed=emb, components=components, type=7)
                continue
            else:
                attachment_data = await payload.attachments[0].read()
                html_parser = BeautifulSoup(
                    attachment_data.decode("UTF-8"), "html.parser"
                )
                tables = html_parser.find_all("table")
                if (
                    html_parser.find_all("h3", attrs={"class": "box-title"})[0]
                    == "Time Table"
                    and tables
                ):
                    return
                semester_list = html_parser.find(
                    "select", attrs={"class": "form-control"}
                ).find_all("option")
                rows = tables[0].find_all("tr")
                filtered_rows = list(
                    filter(None, [rows[b].find_all("td") for b in range(1, len(rows))])
                )[:-1]
                data_for_sql = []
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
                break


def setup(bot):
    bot.add_cog(setup_commands(bot))
