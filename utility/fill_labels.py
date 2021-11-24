from PIL import Image
from create_image import generate_label
from functools import cache


def fill_label(lst, bg_colors=None, font_colors=None, texts=None):
    if bg_colors is None:
        bg_colors = [(0, 255, 0)] * len(lst)
    if font_colors is None:
        font_colors = [(0, 0, 0)] * len(lst)
    if texts is None:
        texts = ["Hello"] * len(lst)

    if not len(lst) == len(bg_colors) == len(font_colors) == len(texts):
        raise ValueError("Inappropriate dimensions for background or font colors")
    im = Image.open("Pinkish_theme.png")
    for coords, bg, font, text in zip(lst, bg_colors, font_colors, texts):
        im.paste(generate_label(text, bg, font), coords)
    im.show()
    return im


@cache
def get_coords():
    rows, columns = 7, 12
    start = 442, 407
    lst = []
    for i in range(rows):
        lst.extend(
            (start[0] + 281 * j, start[1] + int(130.6 * i)) for j in range(columns)
        )
    return lst


if __name__ == "__main__":
    fill_label(get_coords())
