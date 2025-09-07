import json
from datetime import datetime

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
    ]
}"""

# Parse the JSON string into a Python dictionary
data = json.loads(json_string)

# Add the created_date_time, city_id, and data_type keys
data["created_date_time"] = datetime.utcnow().isoformat() + "Z"
data["city_id"] = "001"
data["data_type"] = "apts_for_sale"

# Convert the dictionary back to a JSON string
updated_json_string = json.dumps(data, indent=4, ensure_ascii=False)

# Print the updated JSON string
print(updated_json_string)

"""
Consiser to add following metadata

    "created_date_time": "2024-06-03T12:00:00Z",
    "version": "1.0",
    "source": "www.ss.lv",
    "description": "Apartment listings for sale in Ogre",
    "data_type": "apts_for_sale",
    "city_id": "001",
    "record_count": 3,
    "encoding": "UTF-8",
    "tags": ["real estate", "sales", "apartments"],
"""
