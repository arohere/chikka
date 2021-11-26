import asyncio
from discord.ext import commands, tasks
import discord
from datetime import datetime, timedelta
import sqlite3

from discord_components.component import Button, ButtonStyle, Select, SelectOption
from discord_components.interaction import Interaction


def return_hearts(n):
    n = int(n)
    f_h = "<:full_heart:911538231911276604>"
    h_h = "<:half_heart:911538231860953108>"
    n_h = "<:no_heart:911538231928057906>"
    if n % 2:
        n = (n - 1) // 2
        return f_h * (n) + h_h + n_h * (4 - n)
    else:
        n = n // 2
        return f_h * (n) + n_h * (5 - n)


class ReportBug(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.cursor: sqlite3.Connection = bot.cursor
        self.check_ratings.start()

    # add to vote_notify, last_voted
    # check for DM errors, try except

    # @tasks.loop(hours=168)
    @tasks.loop(seconds=20)
    async def check_ratings(self):
        # print("running loop")
        data = self.cursor.execute(
            """SELECT client_id FROM vote_notify
            WHERE (last_voted is not NULL and last_voted < ?) and (last_notified is NULL or last_notified < last_voted)
            """,
            # (datetime.now() - timedelta(days=31),),
            (datetime.now() - timedelta(minutes=1),),
        ).fetchall()
        client_ids = [int(a[0]) for a in data]
        embed = discord.Embed(
            colour=discord.Colour.from_rgb(207, 68, 119),
            title="Rate your faculties",
            description=(
                "It's been a month since you last rated your faculties. Click on the button below to take the 2 minute survey.\n\n"
                "These surveys help Kartus to assess faculties, and the consolidated ratings of each faculty is made available to all users."
                "This data enables the user to make an informed choice in selecting their faculties for the upcoming semester.\n\n"
                "Failing to take the survey will restrict you from viewing faculty ratings and using Kartus features."
            ),
        )
        components = [
            [
                Button(
                    label="Click Here to Rate",
                    custom_id="DM_rate_request_button",
                    style=ButtonStyle.green,
                )
            ]
        ]
        total_request_messages = []
        # end_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now() + timedelta(minutes=2)
        # print(end_time)
        # asyncio.create_task(self.reply_to_interactions(timedelta(hours=1)))
        asyncio.create_task(self.reply_to_interactions(timedelta(minutes=1)))
        for a in client_ids:
            user: discord.User = self.client.get_user(a)
            dm = await user.create_dm()
            request_message = await dm.send(embed=embed, components=components)
            total_request_messages.append(request_message)
            self.cursor.execute(
                f"""UPDATE vote_notify
                SET notified = "no", last_notified = ?
                WHERE client_id = '{a}'
                """,
                (datetime.now(),),
            )
        self.cursor.commit()

        embed = discord.Embed(
            colour=discord.Colour.from_rgb(207, 68, 119),
            title="Rate your faculties",
            description=(
                "This is the final notification to remind you to rate your faculties. Click on the button below to take the 2-minute survey. "
                "**Failing to take the survey will restrict you from viewing faculty ratings and using Kartus features.**\n\n"
                "These surveys help us to assess faculties, and the consolidated ratings of each faculty is made available to all the users. "
                "This data enables the user to make an informed choice in selecting their faculties for the upcoming semester.\n\n"
                "In case you have been restricted, use ka!rate to take the survey and regain access to Kartus."
            ),
        )

        data = self.cursor.execute(  # add already notified bool
            """SELECT client_id, last_voted, last_notified FROM vote_notify
            WHERE (last_notified is not NULL and last_notified < ?) and notified == "no"
            """,
            # (datetime.now() - timedelta(days=14),),
            (datetime.now() - timedelta(minutes=1),),
        ).fetchall()
        client_ids = [int(a[0]) for a in data]
        for a in client_ids:
            user: discord.User = self.client.get_user(a)
            dm = await user.create_dm()
            request_message = await dm.send(embed=embed, components=components)
            total_request_messages.append(request_message)
            self.cursor.execute(
                f"""UPDATE vote_notify
                SET notified = "yes", last_notified = ?
                WHERE client_id = '{a}'
                """,
                (datetime.now(),),
            )
        self.cursor.commit()
        if total_request_messages:
            total_seconds = (end_time - datetime.now()).total_seconds()
            # print(total_seconds)
            await asyncio.sleep(total_seconds)
            for msg in total_request_messages:
                await msg.disable_components()

    @check_ratings.before_loop
    async def before_rating(self):
        await self.client.wait_until_ready()

    # @check_ratings.before_loop
    # async def before_rating(self):
    #     now = datetime.now()
    #     day = now.weekday()
    #     day = 0 if day == 0 and now.hour < 13 else 8 - day
    #     hours = 13 - now.hour
    #     total_seconds = timedelta(days=day, hours=hours).total_seconds()
    #     await asyncio.sleep(total_seconds)

    async def reply_to_interactions(self, timeout_delta: timedelta):
        endtime = datetime.now() + timeout_delta
        try:
            ongoing_ratings = []
            while True:
                interaction: Interaction = await self.client.wait_for(
                    "button_click",
                    timeout=(endtime - datetime.now()).total_seconds(),
                    check=lambda i: i.custom_id == "DM_rate_request_button",
                )
                await interaction.disable_components()
                dm = await interaction.author.create_dm()
                task1 = asyncio.create_task(
                    self.rate_it(
                        author=interaction.author, channel=interaction.channel, dm=dm
                    )
                )
                ongoing_ratings.append(task1)
        except asyncio.TimeoutError:
            return

    @commands.command()
    async def rate(self, ctx: commands.Context):  # remove and pass through ctx
        author = ctx.author
        channel = ctx.channel
        dm = await ctx.author.create_dm()
        command_msg = ctx.message
        await self.rate_it(author, channel, dm, command_msg)

    async def rate_it(
        self,
        author: discord.Member,
        channel: discord.TextChannel,
        dm: discord.DMChannel,
        command_msg: discord.Message = False,
    ):
        current_semester = self.cursor.execute(
            f"""SELECT semester_id FROM current_semester
            WHERE client_id = '{author.id}'
            """
        ).fetchone()[0]
        rated_data = self.cursor.execute(
            f"""SELECT * FROM client_faculty_rate
            WHERE client_id = '{author.id}' AND semester_id = '{current_semester}'
            """
        ).fetchall()
        faculty_data = {}
        for a in rated_data:
            data_for_faculty = self.cursor.execute(
                f"""SELECT MAX(day_voted),rating FROM client_faculty_rate
                WHERE faculty_name = '{a[0]}' and blacklisted is NULL and rating is not NULL
                GROUP BY client_id
                """
            ).fetchall()
            blacklisted_count = self.cursor.execute(
                f"""SELECT count(*) FROM client_faculty_rate
                WHERE faculty_name = '{a[0]}' and blacklisted = "yes"
                """
            ).fetchone()[0]
            n = len(data_for_faculty) + blacklisted_count
            if n == 0:
                faculty_data[a[0]] = {"not_rated_before": True}
                continue

            total_student_count = self.cursor.execute(
                f"""SELECT count(DISTINCT client_id) FROM client_faculty_rate
                WHERE faculty_name = '{a[0]}' and rating is not NULL
                """
            ).fetchone()[0]
            ratings_for_faculty = [int(b[1]) for b in data_for_faculty]
            mean_rating = sum(ratings_for_faculty) / n
            standard_deviation = (
                sum([(c - mean_rating) ** 2 for c in ratings_for_faculty]) / n
            ) ** 0.5
            faculty_data[a[0]] = {
                "not_rated_before": False,
                "standard_deviation": standard_deviation,
                "mean": mean_rating,
                "total_students": total_student_count,
                "blacklisted_count": blacklisted_count,
                "previous_rate": int(a[3]) if a[3] else 0,
            }
        rating_data = {}
        selection_options = [SelectOption(label=a[0], value=a[0]) for a in rated_data]

        emb = discord.Embed(
            title="Rate Your Faculties",
            description="From the drop down list below select a faculty to rate.",
            footer="Note: The lesser the Mean Deviation more accurate the ratings are.",
            colour=discord.Colour.from_rgb(207, 68, 119),
        )
        embeds = [emb]

        try:
            msg = await dm.send(
                embeds=embeds,
                components=[
                    Select(placeholder="Select a faculty", options=selection_options)
                ],
            )
            if command_msg:
                await command_msg.reply("Check your DMs.")
        except discord.errors.Forbidden:
            """
            ask users to enable messages from server members option in settings
            """
            if command_msg:
                await command_msg.reply(
                    embed=discord.Embed(
                        description="Enable messages from server members in settings to rate.",
                        image_url="https://cdn.discordapp.com/attachments/885410368015446097/907901692836741120/unknown.png",
                        colour=discord.Colour.from_rgb(207, 68, 119),
                    )
                )
            return
        # check try or except send embed and go into while loop
        options_for_rating = [
            [
                Select(
                    placeholder="Select your rating!",
                    options=[
                        SelectOption(
                            label=str(a / 2 if a % 2 else a // 2),
                            value=a,
                            emoji=self.client.emotes["full_heart"],
                        )
                        for a in range(10, 0, -1)
                    ],
                )
            ],
            [Button(label="Blacklist", custom_id="blacklist", style=ButtonStyle.red)],
        ]
        while selection_options:
            interaction: Interaction = await self.client.wait_for(
                "select_option",
                check=lambda i: i.author == author and i.channel == dm,
            )
            faculty_name = interaction.values[0]
            before_rating_embed = discord.Embed(
                title=faculty_name.title(), colour=discord.Colour.from_rgb(207, 68, 119)
            )
            after_rating_embed = discord.Embed(
                title=faculty_name.title(), colour=discord.Colour.from_rgb(207, 68, 119)
            )
            if faculty_data[faculty_name]["not_rated_before"]:
                before_rating_embed.description = (
                    "This faculty has not been rated before"
                )
                kwargs_for_embeds = [
                    {
                        "name": "Average Rating",
                        "value": return_hearts(0),
                        "inline": True,
                    },
                    {
                        "name": "Your Previous Rating",
                        "value": return_hearts(0),
                        "inline": True,
                    },
                    {"name": "‎", "value": "‎", "inline": True},
                ]
            else:
                kwargs_for_embeds = [
                    {
                        "name": "Average Rating",
                        "value": return_hearts(faculty_data[faculty_name]["mean"]),
                        "inline": True,
                    },
                    {
                        "name": "Your Previous Rating",
                        "value": return_hearts(
                            faculty_data[faculty_name]["previous_rate"]
                        ),
                        "inline": True,
                    },
                    {"name": "‎", "value": "‎", "inline": True},
                    {
                        "name": "Standard Deviation",
                        "value": faculty_data[faculty_name]["standard_deviation"],
                        "inline": True,
                    },
                    {
                        "name": "Blacklisted By",
                        "value": f'{faculty_data[faculty_name]["blacklisted_count"]} out of {faculty_data[faculty_name]["total_students"]}',
                        "inline": True,
                    },
                ]
                for kwargs in kwargs_for_embeds:
                    before_rating_embed.add_field(**kwargs)
            msg = await interaction.respond(
                embeds=embeds + [before_rating_embed],
                components=options_for_rating,
                type=7,
            )

            done, pending = await asyncio.wait(
                [
                    self.client.wait_for(
                        "select_option",
                        check=lambda i: i.author == author and i.channel == dm,
                    ),
                    self.client.wait_for(
                        "button_click",
                        check=lambda i: i.author == author and i.channel == dm,
                    ),
                ],
                return_when=asyncio.FIRST_COMPLETED,
            )
            interaction = done.pop().result()
            if isinstance(interaction.component, Select):
                selected = interaction.values[0]
            else:
                selected = "blacklist"
            # print(faculty_name, " - ", selected)
            rating_data[faculty_name] = selected
            # blacklist check and add l8r or now

            for a in selection_options:
                if a.value == faculty_name:
                    selection_options.remove(a)
                    break
                after_rating_embed.description = selected
            after_rating_embed.description = ()
            kwargs_for_embeds[2] = {
                "name": "Your Current Rating",
                "value": "Blacklisted"
                if selected == "blacklist"
                else return_hearts(selected),
                "inline": True,
            }
            for kwargs in kwargs_for_embeds:
                after_rating_embed.add_field(**kwargs)
            embeds.append(after_rating_embed)
            if selection_options:
                await interaction.respond(
                    embeds=embeds,
                    components=[
                        Select(
                            placeholder="Select a faculty", options=selection_options
                        )
                    ],
                    type=7,
                )
        # print(rating_data)
        for a in rating_data:
            if rating_data[a] == "blacklist":
                self.cursor.execute(
                    f"""UPDATE client_faculty_rate
                SET rating = 0, blacklisted = 'yes'
                WHERE client_id = '{author.id}' AND semester_id = '{current_semester}' AND faculty_name = '{a}'
                """
                )
            else:
                self.cursor.execute(
                    f"""UPDATE client_faculty_rate
                SET rating = {rating_data[a]}, blacklisted = NULL
                WHERE client_id = '{author.id}' AND semester_id = '{current_semester}' AND faculty_name = '{a}'
                """
                )
        self.cursor.execute(
            f"""UPDATE vote_notify
            SET last_voted = ?, last_notified = NULL, notified = "no"
            WHERE client_id == '{author.id}'
            """,
            (datetime.now(),),
        )
        self.cursor.commit()
        await interaction.respond(
            content="review done!", embeds=embeds, components=[], type=7
        )


def setup(bot):
    bot.add_cog(ReportBug(bot))
