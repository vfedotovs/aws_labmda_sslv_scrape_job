#!/usr/bin/env python3

import json
import re
from datetime import datetime
import time
# import boto3
import requests
from bs4 import BeautifulSoup


def find_single_page_urls(bs_object) -> list:
    """Function iterates over all a sections and gets all href lines
    object: bs4 object
    returns: list of strings with all message URLs"""
    urls = []
    for hyperlink in bs_object.find_all('a', href=True):
        one_link = "https://ss.lv" + hyperlink['href']
        re_match = re.search("msg", one_link)
        if re_match:
            urls.append(one_link)
    valid_urls = []
    for url in urls:
        if url not in valid_urls:
            valid_urls.append(url)
    return valid_urls


def extract_ad_value() -> str:
    # def extract_street(URL: str) -> str:
    """TODO extract street information value from ads_opt from opt_name 'Iela:'
    returns string

    7 values  +  insert time + price + sqm_price + view count 
    ['Iela:', 'Istabas:', 'Platība:', 'Stāvs:', 'Sērija:', 'Mājas tips:', 'Ērtības:']
    ['<b>Ausekļa prospekts 2a', '2', '51 m²', '2/9', '602.', 'Paneļu', 'Lodžija, Parkošanas vieta']

    """
    URL = "https://ss.lv/msg/lv/real-estate/flats/ogre-and-reg/ogre/idlmb.html"
    STREET_KEY = 'Iela:'
    table_opt_names = v2_get_msg_table_info(URL, "ads_opt_name")
    table_opt_values = v2_get_msg_table_info(URL, "ads_opt")
    names_values = dict(zip(table_opt_names, table_opt_values))
    print(" ------ ")
    value = names_values.get(STREET_KEY, 'Key not found')
    clean_value = value.replace("[Karte]", "")
    print(f"The value for key '{STREET_KEY}' is {clean_value}")



"""
Extracted 30 URL links with apartment ads for sale in ogre city
https://ss.lv/msg/lv/real-estate/flats/ogre-and-reg/ogre/idlmb.html

['Pilsēta, rajons:', 'Pilsēta/pagasts:', 'Iela:', 'Istabas:', 'Platība:', 'Stāvs:', 'Sērija:', 'Mājas tips:', 'Ērtības:']
['<b>Ogre un raj.', '<b>Ogre', '<b>Ausekļa prospekts 2a', '2', '51 m²', '2/9', '602.', 'Paneļu', 'Lodžija, Parkošanas vieta']
apt_price:47 000 € (921.57 €/m²)




def extract_floor_area(URL) -> hash:int
    #'Platība:', floor_area
	ruturn dict

def extract_room_count(URL) -> hash:int
    # 'Istabas:',room_count
	return dict


def extract_apt_loc_floor(URL) -> hash:int
     #'Stāvs:',  >> 2 > apt_loc_floor,


def extract_house_floor_count(URL) -> hash:int
    #  'Stāvs:' house_floor_count
    return dict

def extract_house_series(URL) -> hash:str
    #  'Sērija:', house_series
    return dict


def extract_house_type(URL) -> hash:str
    #  'Mājas tips:', house_type
    return dict

 
def extract_apt_feat(URL) -> hash:list 
    # 'Ērtības:'] apt_feat
    return dict

def extart_apt_price(URL) -> hash:int 
    # price valuse code
    return dict
 

def extart_sqm_price(URL) -> hash:float
    # sqm price code
    return dict


def extract_pub_date(ULR) ->hash: str
   # Datums  pub_date


def extarct_view_count(URL) ->hash:int
    # Unicalo ameklejumu skaits: view_count


def combine_single_ad_data(URL) dict:
    # call function from above
    extrat_1
    extact_2
    exctract_... 
    return dict  URL:hash + data

list of dict

for URL in URLS:
	combine_single_ad_data(URL) 
	add to list of dict 


def create_json_file()
	using list of all adds data 

"""


def extract_data_from_url(nondup_urls: list) -> dict:
    """
    TODO: Refactor this function


    Iterates over url list and extracts ad_otion names,values,
    price and listed date value for each url and formats data
    and returns as dict"""
    all_ad_data = {}
    curr_ad_attributes = []
    ad_dict = []
    print(f"Extracted {len(nondup_urls)} URL links with apartment ads for sale in ogre city")
#    for i in range(msg_url_count): # original iterates over all ad URLs
    for i in range(3):
        current_msg_url = nondup_urls[i] + "\n"
        print(current_msg_url)
        table_opt_names = get_msg_table_info(nondup_urls[i], "ads_opt_name")

        # print(table_opt_names)
        table_opt_values = get_msg_table_info(nondup_urls[i], "ads_opt")
        # print(table_opt_values)
        table_price = get_msg_table_info(nondup_urls[i], "ads_price")
        print(f"Extracting data from message URL  {i + 1}")
        ad_url_hash = extract_url_hash(current_msg_url)
        ad_dict.append(ad_url_hash)
        for idx in range(len(table_opt_names) - 1):
            opt_name_value_line = table_opt_names[idx] + table_opt_values[idx]
            curr_ad_attributes.append(opt_name_value_line)
        # Extract message price field
        price_line = "apt_price:" + table_price[0]
        ad_dict.append(price_line)
        print(price_line)
        # Extract message publish date field
        table_date = get_msg_table_info(nondup_urls[i], "msg_footer")
        for date_idx in range(len(table_date)):
            if date_idx == 2:
                date_str = table_date[date_idx]
                date_and_time = date_str.replace("Datums:", "")
                date_clean = date_and_time.split()[0]
                date_field = "listed_date:" + str(date_clean)
        ad_dict.append(date_field)
        time.sleep(2)
        curr_ad_attributes.append(price_line)
        curr_ad_attributes.append(date_field)
        all_ad_data[ad_url_hash] = curr_ad_attributes
        curr_ad_attributes = []
    return all_ad_data


def v2_get_msg_table_info(msg_url: str, td_class: str) -> list:
    """Function parses message page and extracts td_class table fields.
    Parameters:
    msg_url: message web page link
    td_class: table field name
    Returns:
    List of strings with table field data
    """
    try:
        page = requests.get(msg_url)
        page.raise_for_status()  # Check if the request was successful
    except requests.RequestException as e:
        print(f"Request failed: {e}")
        return []

    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find('table', id="page_main")
    if not table:
        print("Table with id 'page_main' not found.")
        return []

    table_fields = []
    table_data = table.find_all('td', class_=td_class)
    for data in table_data:
        # Get the text content and strip whitespace
        name = data.get_text(strip=True)
        table_fields.append(name)
    return table_fields


def get_msg_table_info(msg_url: str, td_class: str) -> list:
    """ Function parses message page and extracts td_class table fields
    Paramters:
    msg_url: message web page link
    td_class: table field name
    returns: str list with table field data"""
    page = requests.get(msg_url)
    soup = BeautifulSoup(page.content, "html.parser")
    table = soup.find('table', id="page_main")
    table_fields = []
    table_data = table.findAll('td', {"class": td_class})
    for data in table_data:
        tostr = str(data)
        # print("print - data here ")
        no_front = tostr.split('">', 1)[1]
        # print(no_front)
        name = no_front.split("</", 1)[0]
        # print(name)
        table_fields.append(name)
    return table_fields


def get_msg_field_info(msg_url: str, span_id: str):
    """Function finds span id in soup object extracted from url
    and returns text format span"""
    response = requests.get(msg_url)
    data = response.text
    soup = BeautifulSoup(data, "html.parser")
    span = soup.find("span", id=span_id)
    return span.text


def extract_url_hash(full_url: str) -> str:
    """ Extracts hash: dlonf from example url below:
    https://ss.lv/msg/lv/real-estate/flats/ogre-and-reg/ogre/dlonf.html\n'"""
    url_hash = full_url.split("/")[9].split(".")[0]
    return url_hash


def main():
    """main entry point for debugging"""
#    s3 = boto3.resource('s3')
    page = requests.get(
        "https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/")
    bs_ogre_object = BeautifulSoup(page.content, "html.parser")
    valid_msg_urls = find_single_page_urls(bs_ogre_object)
    extract_ad_value()
#
    advert_data = extract_data_from_url(valid_msg_urls)
    ads_data_json = json.dumps(advert_data, indent=4)
#
    full_time = str(datetime.now())
    date_str = full_time.split(" ")[0]
    time_str = full_time.split(" ")[1].split(".")[0]
    new_ts = time_str.replace(":", "-")
    uniq_ts = date_str + "T" + new_ts

#    bucket_name = "my-s3-bucket-name"
    output_file_name = f"ogre_city_raw_data_{uniq_ts}.json"
    json_object = json.dumps(ads_data_json)
    # Writing to sample.json
    with open(output_file_name, "w") as outfile:
        outfile.write(json_object)
#    s3.Bucket(bucket_name).put_object(Key=output_file_name, Body=json_body)


main()


# def handler(event, context):
#    """lambda main entry point"""
#    s3 = boto3.resource('s3')
#    page = requests.get("https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/")
#    bs_ogre_object = BeautifulSoup(page.content, "html.parser")
#    valid_msg_urls = find_single_page_urls(bs_ogre_object)
#
#    advert_data = extract_data_from_url(valid_msg_urls)
#    ads_data_json = json.dumps(advert_data, indent = 4)
#
#    full_time = str(datetime.now())
#    time_str = full_time.split(" ")[0]

#    bucket_name = "my-s3-bucket-name"
#    output_file_name = f"ogre_city_raw_data_{time_str}.json"
#    json_body = json.dumps(ads_data_json)
#    s3.Bucket(bucket_name).put_object(Key=output_file_name, Body=json_body)
