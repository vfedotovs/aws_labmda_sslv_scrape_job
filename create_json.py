#!/usr/bin/env python3

import re
import json

FILE = 'ogre_city_raw_data_2024-06-03T21-02-24.json'

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
    raw_data = json.load(json_file)
    print("Type of raw_data:", type(raw_data))


def clean_string(str_data: str) -> str:
    """ Removes only 2 space chars in row occournaces"""
    removed_two_spaces = re.sub(' +', ' ', str_data)
    removed_nl_char = re.sub('\n', '', removed_two_spaces)
    print(removed_nl_char)
    return removed_nl_char

clean_string(raw_data)


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

valid_json_data = json.loads(employees_string)

print("Type of employees_string:",type(valid_json_data))
print(valid_json_data)
#output
#<class 'dict'>




    # Create pandas data frame
    # mydict = {'URL': urls,
    #         'Room_count': room_counts,
    #         'Size_sq_m' : room_sizes,
    #         'Floor': room_floors,
    #         "Street": room_streets,
    #         'Price': room_prices,
    #         'Pub_date': publish_dates }
    # pandas_df = pd.DataFrame(mydict)
    # return pandas_df


# def create_file_copy() -> None:
    # """Creates copy of pandas_df.csv in as data/pandas_df.csv_2022-12-03.csv"""
    # todays_date = datetime.today().strftime('%Y-%m-%d')
    # dest_file = 'pandas_df_' + todays_date + '.csv'
    # copy_cmd = 'cp pandas_df.csv data/' + dest_file
    # if not os.path.exists('data'):
    #     os.makedirs('data')
    # os.system(copy_cmd)



# how to convert str to json
#https://www.freecodecamp.org/news/python-json-how-to-convert-a-string-to-json/#:~:text=you%20can%20turn%20it%20into,it%20to%20a%20Python%20dictionary.
