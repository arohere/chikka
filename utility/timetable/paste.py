def paste(im1, im2, coords):
    front = im1.convert("RGBA")
    back = im2.convert("RGBA")
    back.paste(front, coords, front)
    return back
