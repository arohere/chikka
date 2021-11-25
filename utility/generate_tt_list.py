from fill_labels import get_coords
from itertools import cycle


def generate_tt(
    list_2d,
    pallette_dark=[()],
    pallette_light=[()],
    text_dark=[()],
    text_light=[()],
    function_chech_dark=lambda a: a.endswith("L"),
):
    coords = get_coords()
    flatten = []
    for i in list_2d:
        flatten.extend(i)
    if len(flatten) != coords:
        raise ValueError(
            "Dimension mismatch, make sure to pass an empty string for empty elements"
        )
    dct = {}
    light, dark = iter(cycle(pallette_light)), iter(cycle(pallette_dark))
    t_dark, t_light = iter(cycle(text_light)), iter(cycle(text_dark))
    txt_list = []
    font_lst = []
    color_lst = []
    coord_lst = []
    for txt, coord in zip(flatten, coords):
        if txt == "":
            continue
        if i in dct:
            color_lst.append(dct[i])
        else:
            txt_list.append(txt)
            coord_lst.append(coord)
            if function_chech_dark(txt):
                font_lst.append(next(t_dark))
                color_lst.append(next(dark))
            else:
                font_lst.append(next(t_light))
                color_lst.append(next(light))
    return coord_lst, font_lst, color_lst, txt_list
