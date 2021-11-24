from PIL import Image
from create_image import generate_label


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


if __name__ == "__main__":
    fill_label(
        [(442, 407), (722, 535)],
        [(0, 255, 0), (0, 0, 50)],
        [(0, 0, 0), (255, 255, 255)],
        ["BCSE101T", "BCSE101L"],
    )
