#!/usr/bin/env python3

import json

FILE = 'ogre_city_raw_data_2023-01-20.json'

#bash to get more meaning format
# cat ogre_city_raw_data_2023-01-20.json \
#    | sed 's/[ |\n]//g' \  # remove space char or \n char - bug we do not remove only single space char- that will help with splits
#    | sed 's/",/",\n/g' \  # add new line after each ", occourance
#    | sed 's/],/],\n/g'    # the same here add new line after each \, occournace

# cat new_ogre_city_raw_data_2023-01-20.json | sed 's/:\[/:\[\n    {/g'| sed 's/\]/\]\n}/g'

# TODO
# all what left to do is replace LV chars with EN
# remove lines of no interest
# split lines of interest
# convert to valid json
# add view coint if possible


# Opening JSON file
with open(FILE) as json_file:
    data = json.load(json_file)
    print("Type:", type(data))


employees_string = '''
{
    "employees" : [
       {
           "first_name": "Michael",
           "last_name": "Rodgers",
           "department": "Marketing"

        },
       {
           "first_name": "Michelle",
           "last_name": "Williams",
           "department": "Engineering"
        }
    ]
}
'''

valid_data = json.loads(employees_string)

print(type(valid_data))
#output
#<class 'dict'>


# how to convert str to json
#https://www.freecodecamp.org/news/python-json-how-to-convert-a-string-to-json/#:~:text=you%20can%20turn%20it%20into,it%20to%20a%20Python%20dictionary.
