import asyncio
from discord.ext import commands, tasks
import discord
from datetime import datetime, timedelta
import sqlite3

from discord_components.component import Button, ButtonStyle, Select, SelectOption
from discord_components.interaction import Interaction
from cogs.utility.rate import sql_queries
from cogs.utility.rate import calculations
from cogs.Resources.rate import embeds_for_rate 

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


class Rate(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.cursor: sqlite3.Connection = bot.cursor
        self.check_ratings.start()

    # add to vote_notify, last_voted
    # check for DM errors, try except

    # @tasks.loop(hours=168) # runs every week
    @tasks.loop(seconds=20)
    async def check_ratings(self):
        # fetch client_ids who have voted x days ago and not yet notified
        data = await sql_queries.fetch_yet_to_notify(self.cursor) 
        client_ids = [int(a[0]) for a in data]
        embed = embeds_for_rate.notify_warning_1
        components = [[
                Button(label="Click Here to Rate",custom_id="DM_rate_request_button",
                    style=ButtonStyle.green)
            ]]
        total_request_messages = [] # append messages to list to disable components after x hours

        # end_time = datetime.now() - timedelta(hours=1)
        end_time = datetime.now() + timedelta(minutes=2)
        # asyncio.create_task(self.reply_to_interactions(timedelta(hours=1)))
        asyncio.create_task(self.reply_to_interactions(timedelta(minutes=1)))

        for a in client_ids:
            user: discord.User = self.client.get_user(a)
            dm = await user.create_dm()
            try: # try to send else ignore
                request_message = await dm.send(embed=embed, components=components)
            except discord.errors.Forbidden:
                continue
            total_request_messages.append(request_message)
            await sql_queries.update_last_notify(self.cursor,a) # update notified date to sql database
        self.cursor.commit()

        #fetch client_ids who have been notified x days ago. notify them for the last time
        embed = embeds_for_rate.notify_warning_2
        data = await sql_queries.fetch_yet_to_notify_again(self.cursor)
        client_ids = [int(a[0]) for a in data]
        for a in client_ids:
            user: discord.User = self.client.get_user(a)
            dm = await user.create_dm()
            try:
                request_message = await dm.send(embed=embed, components=components)
            except discord.errors.Forbidden:
                continue
            total_request_messages.append(request_message)
            await sql_queries.update_last_notify_again(self.cursor,a)
        self.cursor.commit()

        if total_request_messages:
            total_seconds = (end_time - datetime.now()).total_seconds()
            await asyncio.sleep(total_seconds) # sleep for x hours and disable components
            for msg in total_request_messages:
                await msg.disable_components()

    @check_ratings.before_loop
    async def before_rating(self):
        await self.client.wait_until_ready()

    # starts the loop upcomming Monday, 12:00 - 13:00

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
            while True: # listen to interactions until timeout (alter timedelta to change timeout)
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
                ongoing_ratings.append(task1) # for future management
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
        author: discord.User,
        channel: discord.TextChannel,
        dm: discord.DMChannel,
        command_msg: discord.Message = False,
    ):
        current_semester = await sql_queries.fetch_current_semester(self.cursor,author.id)

        rated_data = await sql_queries.previous_rated_data(self.cursor,author.id,current_semester)

        faculty_data = {}
        
        for a in rated_data:     # a = ('PUNITHAVELAN N', '608276451074113539', 'CH20212217', None, None, '2021-11-27 10:03:07.741726')
            ratings_for_faculty = await sql_queries.ratings_for_faculty(self.cursor,a[0])

            blacklisted_count = await sql_queries.blacklisted_count_for_faculty(self.cursor,a[0])

            total_records = len(ratings_for_faculty) + blacklisted_count
            
            if total_records == 0:
                faculty_data[a[0]] = {"not_rated_before": True}
                continue

            total_student_count = await sql_queries.total_students_for_faculty(self.cursor,a[0])


            faculty_data[a[0]] = await calculations.get_faculty_summary(ratings_for_faculty,total_records,total_student_count,blacklisted_count,a[3])

        selection_options = [SelectOption(label=a[0], value=a[0]) for a in rated_data]

        embeds = [embeds_for_rate.rating_embed_1]

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
                    embed=embeds_for_rate.enable_server_message_embed
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

        rating_data = {}

        while selection_options:
            interaction: Interaction = await self.client.wait_for(
                "select_option",
                check=lambda i: i.author == author and i.channel == dm,
            )
            faculty_name = interaction.values[0]
            before_rating_embed = discord.Embed(
                title=faculty_name.title(), colour=discord.Colour.from_rgb(207, 68, 119)
            )
            after_rating_embed = before_rating_embed.copy()

            if faculty_data[faculty_name]["not_rated_before"]:
                before_rating_embed.description = (
                    "This faculty has not been rated before"
                )
                kwargs_for_embeds = embeds_for_rate.kwargs_of_embed_for_not_rated_before
            else:
                kwargs_for_embeds = embeds_for_rate.kwargs_of_embed_for_rated_faculty(faculty_data,faculty_name)
                for kwargs in kwargs_for_embeds:
                    before_rating_embed.add_field(**kwargs)
                    
            msg = await interaction.respond(
                embeds=[embeds[0]] + [before_rating_embed],
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
                
            rating_data[faculty_name] = selected

            for a in selection_options:
                if a.value == faculty_name:
                    selection_options.remove(a)
                    break
                
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
                    embeds=[embeds[0]]+[embeds[-1]],
                    components=[
                        Select(
                            placeholder="Select a faculty", options=selection_options
                        )
                    ],
                    type=7,
                )

        print(rating_data)
        for a in rating_data:
            if rating_data[a] == "blacklist":
                await sql_queries.update_blacklist_rating(self.cursor,author.id,current_semester,a)
            else:
                await sql_queries.update_rating(self.cursor,author.id,current_semester,faculty_name,rating_data)
        await sql_queries.update_voted_date(self.cursor,author.id)
        self.cursor.commit()
        await interaction.respond(
            content="review done!", embeds=embeds, components=[], type=7
        )


def setup(bot):
    bot.add_cog(Rate(bot))
