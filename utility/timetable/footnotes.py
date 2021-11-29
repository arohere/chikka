import fill_labels
from PIL import Image


def complete_footnotes(
    dct, image_timetable_upper=Image.open("./assets/Pinkish_theme.png")
):
    """Takes in the upper timetable and the dictionary scheme, generates the lower portion, sticks it and returns it"""
    coords = []  # placeholder
    texts = [i for i in coords]
    fonts = [j for i, j in coords.values()]
    bg_colors = [i for i, j in coords.values()]
    footnote = fill_labels.fill_lable(coords, bg_colors, fonts, texts)
    COORDINATE = 100, 100  # placeholder
    image_timetable_upper.paste(footnote, COORDINATE)
    return image_timetable_upper
