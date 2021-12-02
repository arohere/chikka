import fill_labels
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
from paste import paste


def complete_footnotes(
    dct,
    details,
    image_timetable_upper=Image.open("./assets/Pinkish_theme.png"),
    image_footer=Image.open("./assets/course_frames.png"),
):
    """Takes in the upper timetable and the dictionary scheme, generates the lower portion, sticks it and returns it"""
    label_coords = []  # placeholder
    details_coords = [
        ((0, 0), (0, 0), (0, 0))
    ]  # placeholder <course coords> <teacher coords> <type coords>
    teacher_size = (200, 200)  # placeholder
    course_size = (200, 200)  # placeholder
    process_teacher = lambda a: a
    process_course = lambda a: a
    process_course_type = lambda a: a
    teachers = [details[i]["Teacher"] for i in dct]
    full_course_names = [details[i]["Full name"] for i in dct]
    course_types = [details[i]["Course type"] for i in dct]
    teacher_images = []
    for teacher in teachers:
        teacher_images.append(generate_text(process_teacher(teacher), teacher_size))
    full_course_images = []
    for course in full_course_names:
        full_course_images.append(generate_text(process_course(course), course_size))
    full_type_images = []
    for type in course_types:
        full_type_images.append(generate_text(process_course_type(type), course_size))

    for (c, teach, typ), i, j, k in zip(
        details_coords, full_course_images, teacher_images, full_type_images
    ):
        image_footer = paste(image_footer, i, c)
        image_footer = paste(image_footer, j, teach)
        image_footer = paste(image_footer, k, typ)

    texts = [i for i in dct]
    fonts = [j for i, j in dct.values()]
    bg_colors = [i for i, j in dct.values()]
    footnote = fill_labels.fill_lable(label_coords, bg_colors, fonts, texts)
    COORDINATE = 100, 100  # placeholder
    image_timetable_upper.paste(footnote, COORDINATE)
    return image_timetable_upper


def generate_text(
    text,
    dimensions,
    font_type="./assets/BwModelica-Medium.ttf",
    text_color="white",
    font_size=45,
):
    im = Image.new("RGBA", dimensions)
    draw = ImageDraw.Draw(im)
    font = ImageFont.truetype(font_type, font_size)
    draw.text((0, 0), text, fill=text_color, font=font)
    return im


if __name__ == "__main__":
    x = generate_text("HMM\nHMMM", (200, 200))
    x.paste(
        generate_text("(Hi)", (50, 50), font_size=20),
        (0, 100),
    )
    x.show()
