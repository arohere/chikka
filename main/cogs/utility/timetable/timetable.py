
from xml.dom import minidom
import re
import os
import json
import random
from cogs.utility.timetable.footers import Group
from typing import List
from cairosvg import svg2png
from PIL import Image
import io

class TimeTable():
    def __init__(self,sql_data):
        x_done = r"./assets/Time Table Template/Time Table.svg"
        doc = minidom.parse(open(x_done))
        tt = doc.getElementsByTagName("g")
        for g in tt :
            if g.getAttribute("id") == "Time_table-2":
                tt = g
                break

        self.doc : minidom.Document = doc
        self.tt = tt
        self.course_data = json.loads(sql_data[1])
        self.schedule_data = json.loads(sql_data[2])
        self.sem_name = sql_data[4]
        self.user_name = sql_data[5]
        self.start_end_colour_font = "ff15d4"
        self.start_end_colour = "30304f"
        self.week_colour_font = "b02bed"
        self.week_colour = "434360"
        self.timings_colour_font = "1f84ff"
        self.timings_colour = "a8a8ed"
        self.semitransparent_bg = "2f3e63"
        self.sem_name_user_name = "6aa4ff"
        self.rectange_stroke = "8f8fbf"
        self._set_username_semname()
        self._init_footers()

    def _init_footers(self):
        l = len(self.course_data)
        if not 7<l<15:
            raise ValueError(f"{l} classes not supported")
        svg = open(f"./assets/Footer Templates/{l} classes.svg")
        self.footers_doc : minidom.Document = minidom.parse(svg)
        self.groups : List[Group] = []
        for d in self.footers_doc.getElementsByTagName("g")[1:]:
            self.groups.append(Group(d,self.footers_doc))

    def _find_darker_colour(self,hex_color,brightness_offset=-20):
        hex_color = "#" + hex_color
        if len(hex_color) != 7:
            raise Exception("Passed %s into color_variant(), needs to be in #87c95f format." % hex_color)
        rgb_hex = [hex_color[x:x+2] for x in [1, 3, 5]]
        new_rgb_int = [int(hex_value, 16) + brightness_offset for hex_value in rgb_hex]
        new_rgb_int = [min([255, max([0, i])]) for i in new_rgb_int] # make sure new values are between 0 and 255
        # hex() produces "0x88", we want just "88"
        return "#" + "".join([hex(i)[2:] for i in new_rgb_int])


    def _set_username_semname(self):
        user_name = self.doc.childNodes[0].childNodes[-1]
        timetable_name = self.doc.childNodes[0].childNodes[-2]
        user_name.appendChild(self.doc.createTextNode(self.user_name))
        timetable_name.appendChild(self.doc.createTextNode(self.sem_name))

    def set_theme(self,location=r"assets/Themes/theme - 1.json",file=None):
        theme_data = json.load(open(location))
        colours = list(theme_data["colours"].values())
        random.shuffle(colours)
        for a in self.course_data:
            a.append(colours.pop())
        script = self.doc.getElementsByTagName("style")[0]
        text = script.childNodes[0].nodeValue
        text = text.replace(self.start_end_colour_font,theme_data["start_end_colour_font"])
        text = text.replace(self.start_end_colour,theme_data["start_end_colour"])
        text = text.replace(self.week_colour_font,theme_data["week_colour_font"])
        text = text.replace(self.week_colour,theme_data["week_colour"])
        text = text.replace(self.timings_colour_font,theme_data["timings_colour_font"])    
        text = text.replace(self.timings_colour,theme_data["timings_colour"])
        text = text.replace(self.semitransparent_bg,theme_data["semitransparent_bg"])      
        text = text.replace(self.sem_name_user_name,theme_data["sem_name_user_name"])      
        text = text.replace(self.rectange_stroke,theme_data["rectange_stroke"])
        script.removeChild(script.childNodes[0])
        script.appendChild(self.doc.createTextNode(text))


    def _set_timetable(self):
        for row in range(len(self.schedule_data)):
            for cell in range(len(self.schedule_data[row])):
                data = self.schedule_data[row][cell] or ""
                if data:
                    g = self.tt.childNodes[-1-row].childNodes[-1-cell]
                    g.removeAttribute("opacity")
                    if "LAB" in data:
                        for course in self.course_data:
                            if course[0] == data[0] and "lab" in course[2].lower():
                                colour = course[-1]
                                break
                    else:
                        for course in self.course_data:
                            if course[0] == data[0] and "lab" not in course[2].lower():
                                colour = course[-1]
                                break

                    rect = g.childNodes[0].childNodes[1]
                    rect.setAttribute("fill",f"#{colour}")
                    rect.removeAttribute("class")
                    text = g.childNodes[1]
                    text.appendChild(self.doc.createTextNode(str(data[0])))

    def _set_footers(self):
        footer_cells = iter(self.groups)
        for group in self.course_data:
            cell = next(footer_cells)
            cell.set_course_code(group[0])
            cell.set_course_title(group[1])
            cell.set_subtitle(group[2])
            cell.set_faculty_name(group[4])
            cell.set_inner_label_colour(f"#{group[5]}")
            cell.set_border_path_colour(self._find_darker_colour(group[5]))
            cell.set_font_colour()

    def _return_svg(self):
        return [self.footers_doc.toxml(), self.doc.toxml()]

    def export_png(self):
        out = self._return_svg()
        footers = svg2png(bytestring=out[0])
        table = svg2png(bytestring=out[1])
        footer_foreground = Image.open(io.BytesIO(footers))
        table_background = Image.open(io.BytesIO(table))
        table_background , footer_foreground = table_background.convert("RGBA") , footer_foreground.convert("RGBA")
        x, y = (67,1435)
        table_background.paste(footer_foreground,(x,y),footer_foreground)
        img_byte_arr = io.BytesIO()
        table_background.save(img_byte_arr, format="png")
        img_byte_arr.seek(0)
        return img_byte_arr



if __name__ == "__main__":
    sql_data = ['608276451074113539', '[["BCSE101E", "Computer Programming Python", "( Embedded Theory )", "TE1", "VIJAYAKUMAR K P"], ["BCSE101E", "Computer Programming Python", "( Embedded Lab )", "L45,L46,L57,L58", "VIJAYAKUMAR K P"], ["BECE101L", "Basic Electronics", "( Theory Only )", "D1", "S SELVENDRAN"], ["BECE101P", "Basic Electronics Lab", "( Lab Only )", "L49,L50", "S SELVENDRAN"], ["BMAT101L", "Calculus", "( Theory Only )", "B1,TB1", "ANURADHA .J"], ["BMAT101P", "Calculus Lab", "( Lab Only )", "L23,L24", "ANURADHA .J"], ["BPHY101L", "Engineering Physics", "( Theory Only )", "C1,TC1", "PUNITHAVELAN N"], ["BPHY101P", "Engineering Physics Lab", "( Lab Only )", "L37,L38", "PUNITHAVELAN N"], ["BSTS101P", "Quantitative Skills Practice I", "( Lab Only )", "L1,L14,L27", "SMART (APT)"]]', '[[["BSTS101P", "LAB"], "", ["BECE101L"], ["BMAT101L"], "", "", "", "", "", "", "", ""], [["BMAT101L"], "", "", ["BPHY101L"], "", "", ["BPHY101P", "LAB"], ["BPHY101P", "LAB"], "", "", "", ""], [["BPHY101L"], ["BSTS101P", "LAB"], "", "", "", "", "", "", ["BCSE101E", "LAB"], ["BCSE101E", "LAB"], "", ""], [["BECE101L"], ["BMAT101L"], "", ["BCSE101E"], ["BMAT101P", "LAB"], ["BMAT101P", "LAB"], ["BECE101P", "LAB"], ["BECE101P", "LAB"], "", "", "", ""], ["", ["BPHY101L"], ["BSTS101P", "LAB"], "", "", "", "", "", ["BCSE101E", "LAB"], ["BCSE101E", "LAB"], "", ""], ["", "", "", "", "", "", "", "", "", "", "", ""], ["", "", "", "", "", "", "", "", "", "", "", ""]]', 'CH20212217', 'Fall Semester I YEAR 2021-22', 'Abbas Roshan']
    obj = TimeTable(sql_data)
    obj.set_theme()
    obj._set_footers()
    obj._set_timetable()
    obj.export_png()



        
