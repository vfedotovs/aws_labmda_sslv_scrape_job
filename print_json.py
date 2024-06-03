import json

json_string = """{
    "fbgfm": [
        "Pils\\u0113ta, rajons:<b>Ogre un raj.",
        "Pils\\u0113ta/pagasts:<b>Ogre",
        "Iela:<b>Zilokalnu prospekts 16",
        "Istabas:2",
        "Plat\\u012bba:49 m\\u00b2",
        "St\\u0101vs:2/9",
        "S\\u0113rija:602.",
        "M\\u0101jas tips:Pane\\u013cu",
        "apt_price:38 000 \\u20ac (775.51 \\u20ac/m\\u00b2)",
        "listed_date:03.06.2024"
    ],
    "cijml": [
        "Pils\\u0113ta, rajons:<b>Ogre un raj.",
        "Pils\\u0113ta/pagasts:<b>Ogre",
        "Iela:<b>R\\u012bgas iela 6",
        "Istabas:2",
        "Plat\\u012bba:47 m\\u00b2",
        "St\\u0101vs:1/5",
        "S\\u0113rija:Specpr.",
        "M\\u0101jas tips:\\u0136ie\\u0123e\\u013cu-pane\\u013cu",
        "apt_price:47 000 \\u20ac (1 000 \\u20ac/m\\u00b2)",
        "listed_date:03.06.2024"
    ],
    "ceefl": [
        "Pils\\u0113ta, rajons:<b>Ogre un raj.",
        "Pils\\u0113ta/pagasts:<b>Ogre",
        "Iela:<b>Skolas iela 1a",
        "Istabas:2",
        "Plat\\u012bba:35 m\\u00b2",
        "St\\u0101vs:5/5",
        "S\\u0113rija:Hru\\u0161\\u010d.",
        "apt_price:30 000 \\u20ac (857.14 \\u20ac/m\\u00b2)",
        "listed_date:03.06.2024"
    ]
}"""

data = json.loads(json_string)

# Pretty-print the JSON data
print(json.dumps(data, indent=4, ensure_ascii=False))

