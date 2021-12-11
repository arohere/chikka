from xml.dom import minidom
from typing import List
import random
from PIL import Image, ImageDraw, ImageFont
import re 
r = lambda: random.randint(0,255)
x = lambda: '#%02X%02X%02X' % (r(),r(),r())

schemes = {"Royal Purple":"7b4b94","Quick Silver":"a9a19c","Cadet Blue Crayola":"9aa5b9","Magic Mint":"b7e3cc","Antique Brass":"da946e","Middle Blue Purple":"7d82b8","Yellow Green Crayola":"d6f7a3","Ash Gray":"aabdae","Russian Green":"77875c","Bistre":"3a2618"}


class Group():

    def __init__(self,group:minidom.Element,doc:minidom.Document) -> None:
        self.doc = doc
        nodes = group.childNodes
        nodes : List[minidom.Element]
        self.InnerLabel = nodes[0]
        self.BorderPaths = nodes[1:6]
        self.CourseTitle = nodes[6]
        self.CourseSubtitle = nodes[7]
        self.CourseCode = nodes[8]
        self.FacultyName = nodes[9]
        self.Width = int(float(nodes[2].getAttribute("width")))
        self.MaxWidth = (self.Width*1.5)
        self.CenterCodePos = int(float(nodes[2].getAttribute("x"))) + 5

    def _format_text(self, string: str):
        max_width = self.MaxWidth
        font_size = 38
        font = ImageFont.truetype("./assets/Fonts/Bw Modelica/BwModelica-Bold.otf",font_size)
        string = string.split()
        final_out = ""
        lines = 0
        while lines < 3 and string:
            for a in range(len(string),0,-1):
                current_string = " ".join(string[:a])
                (width, baseline), (offset_x, offset_y) = font.font.getsize(current_string)
                # print((width, baseline), (offset_x, offset_y),(current_string))
                if width < max_width:
                    final_out += current_string + "\n"
                    string = string[a:]
                    lines += 1
                    break
            else:
                raise ValueError(f"a word is too big: {current_string}")
        return final_out.strip()

    def set_inner_label_colour(self,hex:str):
        self.InnerLabel.setAttribute("fill",hex)

    def set_border_path_colour(self,hex:str):
        for path in self.BorderPaths:
            path.setAttribute("fill",hex)

    def set_course_title(self,title:str,height=41):
        lines = self._format_text(title).split("\n")
        for a in range(len(lines)):
            new_line : minidom.Element = self.doc.createElement("tspan")
            new_line.setAttribute("x","0")
            new_line.setAttribute("y",str(height*a))
            new_line.appendChild(self.doc.createTextNode(lines[a]))
            self.CourseTitle.appendChild(new_line)

    def set_subtitle(self,sub_title:str):
        self.CourseSubtitle.appendChild(self.doc.createTextNode(sub_title))
    
    def set_course_code(self,course:str):
        x,y = re.split("[(]| |[)]",self.CourseCode.getAttribute("transform"))[1:3]
        self.CourseCode.setAttribute("text-anchor","middle")
        self.CourseCode.setAttribute("transform",f"translate({self.CenterCodePos} {y})")
        self.CourseCode.appendChild(self.doc.createTextNode(course.upper()))

    def set_faculty_name(self,faculty_name:str):
        x,y = re.split("[(]| |[)]",self.FacultyName.getAttribute("transform"))[1:3]
        self.FacultyName.setAttribute("text-anchor","middle")
        self.FacultyName.setAttribute("transform",f"translate({(self.Width//2) + float(x)} {y})")
        self.FacultyName.appendChild(self.doc.createTextNode(faculty_name))
        

class FootnotesCreator():

    def __init__(self,svg):
        self.doc : minidom.Document = minidom.parse(svg)
        self.groups : List[Group] = []
        for d in self.doc.getElementsByTagName("g")[1:]:
            self.groups.append(Group(d,self.doc))

    def change_colours(self):
        for group_element in self.groups:
            group_element.set_inner_label_colour(x())
            group_element.set_border_path_colour(x())
            group_element.set_course_code("ARO HERE")
            group_element.set_course_title("Cognitive Thinking and psychological depression")
            group_element.set_subtitle("(Theory Only)")
            group_element.set_faculty_name("PUNITHAVELAN N")

    def return_svg(self):
        return self.doc.toprettyxml()


if __name__ == "__main__":
    obj = FootnotesCreator(open(r"assets\Footer Templates\9 classes.svg"))
    # obj = FootnotesCreator(open(r".\assets\testing_templates\template for 13 footers.svg"))
    obj.change_colours()
    with open(r".\assets\testing_templates\template for 13 footers output.svg","w") as f:
        f.write(obj.return_svg())
    
