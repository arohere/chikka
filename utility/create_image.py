from PIL import Image, ImageDraw, ImageFont
import numpy as np


def generate_label(string, bg_color, text_color):
    im = Image.open("template (1).png")
    im = im.convert("RGBA")
    data = np.array(im)
    red, green, blue, _alpha = data.T
    to_be_replaced = [209, 26, 26]
    r, g, b = to_be_replaced
    areas = (red == r) & (blue == b) & (green == g)
    data[..., :-1][areas.T] = bg_color
    font_size = 45
    im = Image.fromarray(data)
    W, H = im.size
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype("CascadiaCode.ttf", font_size)
    w, h = draw.textsize(string, font=font)
    draw.text(
        ((W - w) // 2 + font_size / 10, (H - h) // 2 - font_size / 10),
        string,
        fill=text_color,
        font=font,
    )
    return im


if __name__ == "__main__":
    generate_label("Hello", (0, 255, 0), (0, 0, 0)).show()
