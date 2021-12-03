from fill_labels import get_coords
from itertools import cycle


def generate_tt(
    list_2d,
    pallette_dark=[(0, 0, 0)],
    pallette_light=[(255, 255, 255)],
    text_dark=[(255, 255, 255)],
    text_light=[(0, 0, 0)],
    function_check_dark=lambda a: a.endswith("L"),
    process_text=lambda a: a,
):
    coords = get_coords()
    flatten = []
    for i in list_2d:
        flatten.extend(i)
    if len(flatten) != len(coords):
        raise ValueError(
            "Dimension mismatch, make sure to pass an empty string for empty elements"
        )
    dct = {}
    light, dark = iter(cycle(pallette_light)), iter(cycle(pallette_dark))
    t_light, t_dark = iter(cycle(text_light)), iter(cycle(text_dark))
    txt_list = []
    font_lst = []
    color_lst = []
    coord_lst = []
    for txt, coord in zip(flatten, coords):
        if txt == "":
            continue
        if txt in dct:
            color, font = dct[txt]
            color_lst.append(color)
            font_lst.append(font)
            txt_list.append(process_text(txt))
            coord_lst.append(coord)
        else:
            color = next(dark if function_check_dark(txt) else light)
            font = next(t_dark if function_check_dark(txt) else t_light)
            dct[txt] = (color, font)
            txt_list.append(process_text(txt))
            coord_lst.append(coord)
            font_lst.append(font)
            color_lst.append(color)
    return coord_lst, color_lst, font_lst, txt_list, dct


if __name__ == "__main__":
    from fill_labels import fill_label
    from footnotes import complete_footnotes

    lst = [
        ["Hi", "", "Hello", "Hmm", "Bye", "", "", "", "", "", "CSEL", "BLAH"]
        for _ in range(7)
    ]
    *params, dct = generate_tt(lst)
    upper = fill_label(*params)
    complete = complete_footnotes(dct, upper)
    complete.show()