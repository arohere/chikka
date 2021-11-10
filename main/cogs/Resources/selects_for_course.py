from discord_components import Select, SelectOption



vellore_streams = {
    "UG"    : [
        Select(
            placeholder="Select A Stream",
            options=[
                SelectOption(label="Engineering", value="Engineering"),
                SelectOption(label="Industrial Design", value="Industrial Design"),     
                SelectOption(label="Architecture", value="Architecture"),
                SelectOption(label="Agriculture", value="Agriculture"),
                SelectOption(label="Sciences", value="Sciences"),
                SelectOption(label="Management Studies & Humanities", value="Management Studies & Humanities"),
                SelectOption(label="Computer Applications", value="Computer Applications"),

            ]
        )
    ],
    "PG"    : [
        Select(
            placeholder="Select A Stream",
            options=[
                SelectOption(label="Engineering", value="Engineering"),
                SelectOption(label="Industrial Design", value="Industrial Design"),     
                SelectOption(label="Computer Applications", value="Computer Applications"),
                SelectOption(label="Management Studies", value="Management Studies"),
                SelectOption(label="Science & Humanities", value="Science & Humanities"),
                SelectOption(label="Social Work", value="Social Work"),
            ]
        )
    ],
    "Integrated":[
        Select(
            placeholder="Select A Stream",
            options = [
                SelectOption(label="Engineering", value="Engineering"),
                SelectOption(label="Sciences", value="Sciences"),
            ]
        )
    ]
}

vellore_programs = {
    "UG" : {
        "Engineering" : [
            Select(
                placeholder="Engineering Programs",
                options=[
                    SelectOption(label="B.Tech Biotechnology", value="B.Tech - Biotechnology"),
                    SelectOption(label="B.Tech Chemical Engineering", value="B.Tech - Chemical Engineering"),
                    SelectOption(label="B.Tech Civil Engineering", value="B.Tech - Civil Engineering"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in Bioinformatics",description = "specialisation in Bioinformatics"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in Information Security",description = "specialisation in Information Security"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in Internet of Things",description = "specialisation in Internet of Things"),
                    SelectOption(label="B.Tech CSE and Business Systems", value="B.Tech - Computer Science and Engineering and Business Systems(in collaboration with TCS)"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in Data Science",description = "specialisation in Data Science"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in Block Chain Technology",description = "specialisation in Block Chain Technology"),
                    SelectOption(label="B.Tech Electrical and Electronics Engineering", value="B.Tech - Electrical and Electronics Engineering"),
                    SelectOption(label="B.Tech Electronics and Communication Engineering", value="B.Tech - Electronics and Communication Engineering"),
                    SelectOption(label="B.Tech Electronics and Instrumentation Engineering", value="B.Tech - Electronics and Instrumentation Engineering"),
                    SelectOption(label="B.Tech Electronics and Communication", value="B.Tech - Electronics and Communication with spc. in Biomedical Engineering",description = "specialisation in Biomedical Engineering"),
                    SelectOption(label="B.Tech Information Technology", value="B.Tech - Information Technology"),
                    SelectOption(label="B.Tech Mechanical Engineering", value="B.Tech - Mechanical Engineering"),
                    SelectOption(label="B.Tech Mechanical", value="B.Tech - Mechanical with spc. in Automotive Engineering",description = "specialisation in Automotive Engineering"),
                    SelectOption(label="B.Tech Mechanical", value="B.Tech - Mechanical with spc. in Manufacturing Engineering",description = "specialisation in Manufacturing Engineering"),
                    SelectOption(label="B.Tech Civil Engineering", value="B.Tech - Civil Engineering with Minor in Computer Science Engineering",description = "Minor in Computer Science Engineering"),
                    SelectOption(label="B.Tech Civil Engineering", value="B.Tech - Civil Engineering with Minor in Artificial Intelligence",description = "Minor in Artificial Intelligence"),
                    SelectOption(label="B.Tech Civil Engineering", value="B.Tech - Civil Engineering with Minor in Data Science",description = "Minor in Data Science"),
                    SelectOption(label="B.Tech Mechanical Engineering", value="B.Tech - Mechanical Engineering with Minor in Computer Science and Engineering",description = "Minor in CSE"),
                    SelectOption(label="B.Tech Mechanical Engineering", value="B.Tech - Mechanical Engineering with Minor in AI ML",description = "Minor in AI ML"),
                    SelectOption(label="B.Tech Mechanical Engineering", value="B.Tech - Mechanical Engineering with Minor in Data Science",description = "Minor in Data Science"),

                ]
            )
        ],

        "Industrial Design" : [
            Select(
                placeholder="Industrial Design Programs",
                options=[
                    SelectOption(label="B.Des. Industrial Design", value="B.Des. Industrial Design")
                ]
            )
        ],

        "Architecture" : [
            Select(
                placeholder="Architecture Programs",
                options=[
                    SelectOption(label="B.Arch", value="B.Arch")
                ]
            )
        ],

        "Agriculture" : [
            Select(
                placeholder="Agriculture Programs",
                options=[
                    SelectOption(label="B.Sc. (Hons.) Agriculture", value="B.Sc. (Hons.) Agriculture"),
                ]
            )
        ],

        "Sciences" : [
            Select(
                placeholder="Science Programs",
                options=[
                    SelectOption(label="B.Sc Catering and Hotel Management", value="B.Sc Catering and Hotel Management"),
                    SelectOption(label="B.Sc Computer Science", value="B.Sc Computer Science"),
                    SelectOption(label="B.Sc (Multimedia & Animation)", value="B.Sc (Multimedia & Animation)"),
                    SelectOption(label="B.Sc. Visual Communication", value="B.Sc. Visual Communication"),
                ]
            )
        ],

        "Management Studies & Humanities" : [
            Select(
                placeholder="Management Studies & Humanities Programs",
                options=[
                    SelectOption(label="B.B.A (Bachelor of Business Administration)", value="B.B.A (Bachelor of Business Administration)"),
                    SelectOption(label="B.Com (Bachelor of Commerce)", value="B.Com (Bachelor of Commerce)"),
                ]
            )
        ],

        "Computer Applications" : [
            Select(
                placeholder="Computer Applications Programs",
                options=[
                    SelectOption(label="B.C.A (Bachelor of Computer Applications)", value="B.C.A (Bachelor of Computer Applications)"),
                ]
            )
        ]
    },
    "Integrated" : {
        "Engineering" : [
            Select(
                placeholder="Engineering Programs",
                options=[
                    SelectOption(label="Integrated M.Tech Software Engineering ", value="Integrated M.Tech Software Engineering "),
                    SelectOption(label="Integrated M.Tech CSE", value="Integrated M.Tech CSE in collaboration with Virtusa ",description = "in collaboration with Virtusa "),
                    SelectOption(label="Integrated M.Tech CSE with spc. In Data Science ", value="Integrated M.Tech Computer Science and Engineering with spc. In Data Science ",description = "specialisation In Data Science "),
                ]
            )
        ],

        "Sciences" : [
            Select(
                placeholder="Science Programs",
                options=[
                    SelectOption(label="Integrated Master of Science in Biotechnology ", value="Integrated Master of Science in Biotechnology "),
                    SelectOption(label="Integrated M.Sc. Food Science and Technology (5 Year)", value="Integrated M.Sc. Food Science and Technology (5 Year)"),
                    SelectOption(label="Integrated M.Sc Computational Statistics and Data Analytics (5 Year)", value="Integrated M.Sc Computational Statistics and Data Analytics (5 Year)"),
                    SelectOption(label="Integrated M.Sc. Physics (5 Year)", value="Integrated M.Sc. Physics (5 Year)",description = "exit option B.Sc. Physics (3 Year) or B.Sc. Physics (Hon) (4 Year)"),
                    SelectOption(label="Integrated M.Sc. Chemistry (5 Year)", value="Integrated M.Sc. Chemistry (5 Year)",description = "exit option B.Sc. Chemistry (3 Year) or B.Sc. Chemistry (Hon) (4 Year)"),
                    SelectOption(label="Integrated M.Sc. Mathematics (5 Year)", value="Integrated M.Sc. Mathematics (5 Year)",description = "exit option B.Sc. Mathematics (3 Year) or B.Sc. Mathematics (Hon) (4 Year)"),
                ]
            )
        ],
    },
    "PG":{
        "Engineering" : [
            Select(
                placeholder="Engineering Programs",
                options=[
                    SelectOption(label="M.Tech Automotive Electronics", value="M.Tech Automotive Electronics in collaboration with TIFAC-CORE industry partners",description = "in collaboration with TIFAC-CORE industry partners"),
                    SelectOption(label="M.Tech Automotive Engineering", value="M.Tech - Automotive Engineering"),
                    SelectOption(label="M.Tech Biomedical Engineering ", value="M.Tech Biomedical Engineering "),
                    SelectOption(label="M.Tech Biotechnology", value="M.Tech Biotechnology"),
                    SelectOption(label="M.Tech CAD / CAM", value="M.Tech CAD / CAM"),
                    SelectOption(label="M.Tech Communication Engineering", value="M.Tech Communication Engineering"),
                    SelectOption(label="M.Tech CSE", value="M.Tech Computer Science and Engineering"),
                    SelectOption(label="M.TechConstruction Technology and Management", value="M.TechConstruction Technology and Management"),
                    SelectOption(label="M.Tech Control and Automation", value="M.Tech Control and Automation"),
                    SelectOption(label="M. Tech CSE", value="M. Tech Computer Science and Engineering with spc. in Big Data Analytics",description = "specialisation in Big Data Analytics"),
                    SelectOption(label="M. Tech CSE", value="M. Tech Computer Science and Engineering with spc. in Information Security",description = "specialisation in Information Security"),
                    SelectOption(label="M. Tech CSE", value="M. Tech Computer Science and Engineering with spc. in AI ML",description = "specialisation in AI ML"),
                    SelectOption(label="M.Tech Embedded Systems", value="M.Tech Embedded Systems"),
                    SelectOption(label="M.Tech IoT and Sensor Systems", value="M.Tech IoT and Sensor Systems"),
                    SelectOption(label="M.Tech Manufacturing Engineering", value="M.Tech Manufacturing Engineering"),
                    SelectOption(label="M.Tech Mechanical", value="M.Tech Mechanical with spc. in Cyber Physical Systems",description = "specialisation in Cyber Physical Systems"),
                    SelectOption(label="M.Tech Mechatronics", value="M.Tech Mechatronics"),
                    SelectOption(label="M.Tech Nanotechnology", value="M.Tech Nanotechnology"),
                    SelectOption(label="M.Tech Power Electronics and Drives", value="M.Tech Power Electronics and Drives"),
                    SelectOption(label="M.Tech Structural Engineering", value="M.Tech Structural Engineering"),
                    SelectOption(label="M.Tech VLSI Design", value="M.Tech VLSI Design"),
                ]
            )
        ],

        "Industrial Design" : [
            Select(
                placeholder="Industrial Design Programs",
                options=[
                    SelectOption(label="M.Des. (Industrial Design)", value="M.Des. (Industrial Design)"),
                ]
            )
        ],

        "Computer Applications" : [
            Select(
                placeholder="Computer Applications Programs",
                options=[
                    SelectOption(label="M.C.A. (Master of Computer Applications)", value="M.C.A. (Master of Computer Applications)"),
                ]
            )
        ],

        "Management Studies" : [
            Select(
                placeholder="Management Studies Programs",
                options=[
                    SelectOption(label="MBA (Master of Business Administration)", value="MBA (Master of Business Administration)"),
                ]
            )
        ],

        "Science & Humanities" : [
            Select(
                placeholder="Science & Humanities Programes",
                options=[
                    SelectOption(label="M.Sc Applied MicroBiology", value="M.Sc Applied MicroBiology"),
                    SelectOption(label="M.Sc Biomedical Genetics", value="M.Sc Biomedical Genetics"),
                    SelectOption(label="M.Sc Biotechnology", value="M.Sc Biotechnology"),
                    SelectOption(label="M.Sc Business Statistics", value="M.Sc Business Statistics"),
                    SelectOption(label="M.Sc Chemistry", value="M.Sc Chemistry"),
                    SelectOption(label="M.Sc Data Science", value="M.Sc Data Science"),
                    SelectOption(label="M.Sc Physics", value="M.Sc Physics"),
                ]
            )
        ],

        "Social Work" : [
            Select(
                placeholder="Social Work",
                options=[
                    SelectOption(label="Master of Social Work", value="Master of Social Work"),
                ]
            )
        ],
    }
}

chennai_streams = {
    "UG"    : [
        Select(
            placeholder="Select A Stream",
            options=[
                SelectOption(label="Engineering", value="Engineering"),
                SelectOption(label="Integrated Law", value="Integrated Law"),     
                SelectOption(label="Sciences", value="Science"),
                SelectOption(label="Management Studies & Humanities", value="Management Studies & Humanities"),
            ]
        )
    ],
    "PG"    : [
        Select(
            placeholder="Select A Stream",
            options=[
                SelectOption(label="M.Tech", value="M.Tech"),
                SelectOption(label="Industrial Courses", value="Industrial Courses"),     
                SelectOption(label="Computer Applications", value="Computer Applications"),
                SelectOption(label="Business Management", value="Business Management"),
                SelectOption(label="Science & Humanities", value="Science & Humanities"),
            ]
        )
    ],
    "Integrated":[
    ]
}


chennai_programs = {
    "UG" : {
        "Engineering" : [
            Select(
                placeholder="Engineering Programss",
                options=[
                    SelectOption(label="B.Tech Civil Engineering", value="B.Tech - Civil Engineering"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in AI ML",description = "specialisation in AI ML"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in Artificial Intelligence and Robotics",description = "specialisation in Artificial Intelligence and Robotics"),
                    SelectOption(label="B.Tech CSE", value="B.Tech - Computer Science and Engineering with spc. in Cyber Physical Systems",description = "specialisation in Cyber Physical Systems"),
                    SelectOption(label="B.Tech Electrical and Electronics Engineering", value="B.Tech - Electrical and Electronics Engineering"),
                    SelectOption(label="B.Tech Electronics and Communication Engineering", value="B.Tech - Electronics and Communication Engineering"),
                    SelectOption(label="B.Tech Electronics and Computer Engineering", value="B.Tech - Electronics and Computer Engineering"),
                    SelectOption(label="B.Tech Fashion Technology ", value="B.Tech - Fashion Technology "),
                    SelectOption(label="B.Tech Mechanical Engineering", value="B.Tech - Mechanical Engineering"),
                    SelectOption(label="B.Tech Mechatronics and Automation", value="B.Tech - Mechatronics and Automation"),
                    SelectOption(label="B.Tech Mechanical Engineering with Specialization in Electric Vehicles", value="B.Tech Mechanical Engineering with Specialization in Electric Vehicles",description = "Specialization in Electric Vehicles"),
                    ]
                )
            ],

        "Integrated Law" : [
            Select(
                placeholder="Integrated Law Programs",
                options=[
                    SelectOption(label="B.A., LL.B (Hons.)", value="B.A., LL.B (Hons.)"),
                    SelectOption(label="BBA., LL.B (Hons.)", value="BBA., LL.B (Hons.)"),
                    ]
                )
            ],

        "Science" : [
            Select(
                placeholder="Science Programs",
                options=[
                    SelectOption(label="B.Sc. Fashion Design", value="B.Sc. Fashion Design"),
                    SelectOption(label="B.Sc. Mathematics and Computing", value="B.Sc. Mathematics and Computing"),
                    SelectOption(label="Bachelor of Science PCM", value="Bachelor of Science PCM"),
                    ]
                )
            ],

        "Management Studies & Humanities" : [
            Select(
                placeholder="Management Studies & Humanities Programs",
                options=[
					SelectOption(label="BBA Honours (2+2) programme", value="BBA Honours (2+2) programme in collaboration with RIT ",description = "in collaboration with RIT"),
					SelectOption(label="B.Com (Honours) ", value="B.Com (Honours) "),
                    ]
                )
            ]
    },
    "PG" : {
        "M.Tech" : [
            Select(
                placeholder="M.Tech Programs",
                options=[
                    
					SelectOption(label="M.Tech CSE", value="M.Tech Computer Science and Engineering"),
					SelectOption(label="M.Tech CSE", value="M.Tech Computer Science and Engineering with spc. in Big Data Analytics",description = "specialisation in Big Data Analytics"),
					SelectOption(label="M.Tech CSE", value="M.Tech Computer Science and Engineering with spc. in AI ML",description = "specialisation in AI ML"),
					SelectOption(label="M.Tech CSE", value="M.Tech Computer Science and Engineering with spc. in Cyber Physical Systems",description = "specialisation in Cyber Physical Systems"),
					SelectOption(label="M.Tech VLSI Design", value="M.Tech VLSI Design"),
					SelectOption(label="M.Tech Embedded Sysytems", value="M.Tech Embedded Sysytems"),
					SelectOption(label="M.Tech Structural Engineering", value="M.Tech Structural Engineering"),
					SelectOption(label="M.Tech Mechatronics", value="M.Tech Mechatronics"),
					SelectOption(label="M.Tech CAD/CAM", value="M.Tech CAD/CAM"),
                ]
            )
        ],

        "Industrial Courses" : [
            Select(
                placeholder="Industrial Courses",
                options=[
					SelectOption(label="M.Tech Automation and Mechatronics (valeo)", value="M.Tech Automation and Mechatronics (valeo)"),
					SelectOption(label="M.Tech Power Electronics and Drives (valeo)", value="M.Tech Power Electronics and Drives (valeo)"),
                ]
            )
        ],

        "Computer Applications" : [
            Select(
                placeholder="Computer Applications Programs",
                options=[
					SelectOption(label="M.C.A.(Master of Computer Applications)", value="M.C.A.(Master of Computer Applications)"),
                ]
            )
        ],

        "Business Management" : [
            Select(
                placeholder="Business Mangement Programs",
                options=[
					SelectOption(label="M.B.A. Master of Business Administration", value="M.B.A. Master of Business Administration"),
                ]
            )
        ],

        "Science & Humanities" : [
            Select(
                placeholder="Science  & Humanities Programs",
                options=[
					SelectOption(label="M.Sc Chemistry", value="M.Sc Chemistry"),
					SelectOption(label="M.Sc Data Science", value="M.Sc Data Science"),
					SelectOption(label="M.Sc Physics", value="M.Sc Physics"),
                ]
            )
        ],
    },
    "Integrated" : {
        "Integrated" : [
            Select(
                placeholder="Science  & Humanities Programs",
                options=[
					SelectOption(label="Integrated M.Tech. Software Engineering", value="Integrated M.Tech. Software Engineering"),
					SelectOption(label="Integrated M.Tech. Computer Science and Engineering", value="Integrated M.Tech. Computer Science and Engineering with spc. in Business Analytics", description = "specialisation in Business Analytics"),
					SelectOption(label="Integrated M.Tech. Construction Technology and Management", value="Integrated M.Tech. Construction Technology and Management"),
                ]
            )

        ]
    }
}


select_options = {
    "Degree"  : [
        Select(
            placeholder="Select your pursuing degree",
            options=[
                SelectOption(label = "Undergraduate",value = "UG"),
                SelectOption(label = "Postgraduate",value = "PG"),
                SelectOption(label = "Integrated Masters",value = "Integrated")
            ]
        )
    ],
    "Vellore" : {
        "stream"   : vellore_streams,
        "program" : vellore_programs
    },
    "Chennai" :  {
        "stream"   : chennai_streams,
        "program" : chennai_programs
    }
}