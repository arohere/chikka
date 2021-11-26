import discord


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

notify_warning_1 = discord.Embed(
    colour=discord.Colour.from_rgb(207, 68, 119),
    title="Rate your faculties",
    description=(
        "It's been a month since you last rated your faculties. Click on the button below to take the 2 minute survey.\n\n"
        "These surveys help Kartus to assess faculties, and the consolidated ratings of each faculty is made available to all users."
        "This data enables the user to make an informed choice in selecting their faculties for the upcoming semester.\n\n"
        "Failing to take the survey will restrict you from viewing faculty ratings and using Kartus features."
    ),
)

notify_warning_2 = discord.Embed(
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


rating_embed_1 = discord.Embed(
    title="Rate Your Faculties",
    description="From the drop down list below select a faculty to rate.",
    footer="Note: The lesser the Mean Deviation more accurate the ratings are.",
    colour=discord.Colour.from_rgb(207, 68, 119),
)

enable_server_message_embed = discord.Embed(
    description="Enable messages from server members in settings to rate.",
    image_url="https://cdn.discordapp.com/attachments/885410368015446097/907901692836741120/unknown.png",
    colour=discord.Colour.from_rgb(207, 68, 119),
)

kwargs_of_embed_for_not_rated_before = [
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

def kwargs_of_embed_for_rated_faculty(faculty_data,faculty_name):
    return [
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