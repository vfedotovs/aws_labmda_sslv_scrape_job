#!/usr/bin/env python3

import json
import re
from datetime import datetime
import time
# import boto3
import requests
from bs4 import BeautifulSoup


SCRAPED_DATA = {"for_sale_apartments": []}

AD_OPTIONS = {
    "street": "Iela:",            # implemented
    "room_cnt": "Istabas:",       # implemented
    "floor_area": "Platība:",     # implemented
    "apt_floor_loc": "Stāvs:",    # implemented
    "house_floor_cnt": "Stāvs:",  # implemented

    "house_series": "Sērija:",
    "house_type":  'Mājas tips:',
    "apt_feats": 'Ērtības:',
    "price ": "price",
    "sqm_price": "sqm_price",
    "listed_date": "listed_date",
    "listed_time": "listed_time",
    "view_cnt": "view_count"
}


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


def extract_data_from_url(nondup_urls: list) -> dict:
    """
    TODO: Refactor this function
    Iterates over url list and extracts ad_otion names,values,
    price and listed date value for each url and formats data
    and returns as dict"""
    all_ad_data = {}
    curr_ad_attributes = []
    ad_dict = []
    # print(f"Extracted {len(nondup_urls)} URL links with apartment ads for sale in ogre city")
#    for i in range(msg_url_count): # original iterates over all ad URLs
    for i in range(3):
        current_msg_url = nondup_urls[i] + "\n"
        print(current_msg_url)
        table_opt_names = get_msg_table_info(nondup_urls[i], "ads_opt_name")
        table_opt_values = get_msg_table_info(nondup_urls[i], "ads_opt")
        table_price = get_msg_table_info(nondup_urls[i], "ads_price")
        # print(f"Extracting data from message URL  {i + 1}")
        ad_url_hash = extract_url_hash(current_msg_url)
        ad_dict.append(ad_url_hash)
        for idx in range(len(table_opt_names) - 1):
            opt_name_value_line = table_opt_names[idx] + table_opt_values[idx]
            curr_ad_attributes.append(opt_name_value_line)
        # Extract message price field
        price_line = "apt_price:" + table_price[0]
        ad_dict.append(price_line)
        # print(price_line)
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
        # print(price_line)
        curr_ad_attributes.append(date_field)
        # print(date_field)
        all_ad_data[ad_url_hash] = curr_ad_attributes
        curr_ad_attributes = []
    print(type(all_ad_data))
    return all_ad_data


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
        no_front = tostr.split('">', 1)[1]
        name = no_front.split("</", 1)[0]
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


def extract_table_names_values(URL: str, td_class_name: str) -> dict:
    """Function extracts from 2 tables keys and values
    Example of returned data structure is dict from 2 lists
    If the lists have different lengths, zip will stop creating
    pairs when the shortest list is exhausted.
    If you need to handle lists of different lengths and ensure
    that all keys have corresponding values,
    you can use itertools.zip_longest.

    ['Iela:', 'Istabas:', 'Platība:', 'Stāvs:', 'Sērija:', 'Mājas tips:', 'Ērtības:']
    ['<b>Ausekļa prospekts 2a', '2', '51 m²', '2/9', '602.', 'Paneļu', 'Lodžija, Parkošanas vieta']

    td_class_name = "ads_opt_name"
    """
    table_opt_names = get_msg_table_info(URL, td_class_name)
    table_opt_values = get_msg_table_info(URL, "ads_opt")
    names_values = dict(zip(table_opt_names, table_opt_values))
    return names_values


def get_msg_table_info(msg_url: str, td_class: str) -> list:
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
        name = data.get_text(strip=True)
        table_fields.append(name)
    return table_fields


def extract_ad_value(ad_table: dict, option: str) -> str:
    """TODO"""
    lv_key_name = AD_OPTIONS.get(option)
    value = ad_table.get(lv_key_name, 'N/A')
    if option == "street":
        street_value = value.replace("[Karte]", "")
        print(f"The value for key '{option}' is {street_value}")
        return option, street_value
    if option == "room_cnt":
        room_cnt_value = value
        print(f"The value for key '{option}' is {room_cnt_value}")
        return option, room_cnt_value
    if option == "floor_area":
        floor_area_value = value.split(" ")[0]
        print(f"The value for key '{option}' is {floor_area_value}")
        return option, floor_area_value
    if option == "apt_floor_loc":
        apt_floor_loc_value = value.split("/")[0]
        print(f"The value for key '{option}' is {apt_floor_loc_value}")
        return option, apt_floor_loc_value
    if option == "house_floor_cnt":
        house_floor_cnt_value = value.split("/")[1]
        print(f"The value for key '{option}' is {house_floor_cnt_value}")
        return option, house_floor_cnt_value
    if option == "house_series":
        house_series_value = value
        print(f"The value for key '{option}' is {house_series_value}")
        return option, house_series_value
    if option == "house_type":
        house_type_value = value
        print(f"The value for key '{option}' is {house_type_value}")
        return option, house_type_value
    if option == "apt_feats":
        apt_feat_list = value
        print(f"The value for key '{option}' is {apt_feat_list}")
        return option, apt_feat_list
    print(type(curr_ad))
    print(curr_ad)

    print(f"The value for key '{option}' is {value}")
    # return value


def extract_ad_table_values(URL: str, apt_data: dict) -> dict:
    """ TODO
    """
    print("DATA for curr URL: ", URL)
    ad_opt_table = extract_table_names_values(
        URL, "ads_opt_name")    # returns dict
    # Refactor replace with for loop
    ad_url_hash = extract_url_hash(URL)
    apt_data['url_hash'] = ad_url_hash
    street_key, street_value = extract_ad_value(ad_opt_table, "street")
    apt_data[street_key] = street_value
    rc_key, rc_value = extract_ad_value(ad_opt_table, "room_cnt")
    apt_data[rc_key] = rc_value
    fa_key, floor_area_value = extract_ad_value(ad_opt_table, "floor_area")
    apt_data[fa_key] = floor_area_value
    apt_loc_key, apt_fl_loc_value = extract_ad_value(
        ad_opt_table, "apt_floor_loc")
    apt_data[apt_loc_key] = apt_fl_loc_value

    house_floor_cnt_key, house_floor_cnt_value = extract_ad_value(
        ad_opt_table, "house_floor_cnt")
    apt_data[house_floor_cnt_key] = house_floor_cnt_value
    house_series_key, house_series_value = extract_ad_value(
        ad_opt_table, "house_series")
    apt_data[house_series_key] = house_series_value
    house_type_key, house_type_value = extract_ad_value(
        ad_opt_table, "house_type")
    apt_data[house_type_key] = house_type_value
    apt_feat_list_key, apt_feat_list_value = extract_ad_value(
        ad_opt_table, "apt_feats")
    apt_data[apt_feat_list_key] = apt_feat_list_value
    print(apt_data)
    return apt_data


def extract_footer_table_values(URL: str, td_class_name: str) -> dict:
    """ TODO
    # to extract date and time ads price table must be used )
    # table_date = get_msg_table_info(nondup_urls[i], "msg_footer")
    """
    footer_table = extract_table_names_values(
        URL, td_class_name)    # returns dict
    listed_date_key, listed_date_value = extract_ad_value(
        footer_table, "listed_date")
    listed_time_key, listed_time_value = extract_ad_value(
        footer_table, "listed_time")
    print("Ad Listed Date: ", listed_date_value)
    print("Ad Listed Time: ", listed_time_value)
    pass


def main():
    """main entry point for debugging"""
#    s3 = boto3.resource('s3')
    page = requests.get("https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/")
    bs_ogre_object = BeautifulSoup(page.content, "html.parser")
    valid_msg_urls = find_single_page_urls(bs_ogre_object)
    print("Todays Ogre city apartment ad for sale count is : ", len(valid_msg_urls))
    scraped_data = {"apartments": []}

    if len(valid_msg_urls) > 0:
        for idx in range(3):
            curr_apt_elements = {}
            curr_apt_data = extract_ad_table_values(valid_msg_urls[idx], curr_apt_elements)
            price_and_sqm_price = get_msg_table_info(
                valid_msg_urls[idx], "ads_price")[0]
            apt_price = price_and_sqm_price.split('€')[0]
            sqm_price = price_and_sqm_price.split('€')[1]
            clean_sqm_price = sqm_price.split("(")[1]
            curr_apt_data["price"] = apt_price
            curr_apt_data["sqm_price"] = clean_sqm_price
            print("Apartment price: ", apt_price)
            print("Apartment sqm price: ", clean_sqm_price)
            footer_table = get_msg_table_info(valid_msg_urls[idx], "msg_footer")
            for date_idx in range(len(footer_table)):
                if date_idx == 2:
                    date_str = footer_table[date_idx]
                    date_and_time = date_str.replace("Datums:", "")
                    clean_date = date_and_time.split()[0]
                    clean_time = date_and_time.split()[1]
                    print("Ad listed date: ", clean_date)
                    print("Ad listed time: ", clean_time)
                    curr_apt_data["listed_date"] = clean_date
                    curr_apt_data["listed_time"] = clean_time
            scraped_data["apartments"].append(curr_apt_data)
    print(scraped_data)


#
    # refactor this function:
    # continue work here after 2024-06-23
    # advert_data = extract_data_from_url(valid_msg_urls)
    # ads_data_json = json.dumps(advert_data, indent=4)
    

    lambda_out_v2 = json.dumps(scraped_data, indent=4)

#
    full_time = str(datetime.now())
    date_str = full_time.split(" ")[0]
    time_str = full_time.split(" ")[1].split(".")[0]
    new_ts = time_str.replace(":", "_")
    uniq_ts = date_str + "T" + new_ts

#    bucket_name = "my-s3-bucket-name"
    # output_file_name = f"city_id_5001_apt_sale_data_{uniq_ts}.json"
    output_file_name_v2 = f"city_id_5001_apt_sale_data_v2_{uniq_ts}.json"
    # json_object = json.dumps(ads_data_json)
    json_object_v2 = json.dumps(lambda_out_v2)
    # Writing to sample.json
    # with open(output_file_name, "w") as outfile:
    #     outfile.write(json_object)
    with open(output_file_name_v2, "w",encoding='utf8') as outfile_v2:
        outfile_v2.write(json_object_v2)
#    s3.Bucket(bucket_name).put_object(Key=output_file_name, Body=json_body)
    # with open(output_file_name_v2, 'w', encoding='utf-8') as f:
    #     json.dump(lambda_out_v2, f, ensure_ascii=False, indent=4)



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
