import json
import re
import boto3
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import time


def find_single_page_urls(bs_object) -> list:
    """Function iterates over all a sections and gets all href lines
    object: bs4 object
    returns: list of strings with all message URLs"""
    urls = []
    for a in bs_object.find_all('a', href=True):
        one_link = "https://ss.lv" + a['href']
        re_match = re.search("msg", one_link)
        if re_match:
            urls.append(one_link)
    valid_urls = []
    for url in urls:
        if url not in valid_urls:
            valid_urls.append(url)
    return valid_urls


def extract_data_from_url(nondup_urls: list) -> dict:
    """TODO: split this function it does too many tasks:
    1. Iterate over url list
    2. extract ad_otion names,values, price and listed date value for each url
    3. format in to dict and return dict """
    msg_url_count = len(nondup_urls)
    all_ad_data = {}
    curr_ad_attributes = []
    ad_dict = []
    print(len(nondup_urls))
    for i in range(msg_url_count):
        current_msg_url = nondup_urls[i] + "\n"
        table_opt_names = get_msg_table_info(nondup_urls[i], "ads_opt_name")
        table_opt_values = get_msg_table_info(nondup_urls[i], "ads_opt")
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
        # Extract message publish date field
        table_date = get_msg_table_info(nondup_urls[i], "msg_footer")
        for date_idx in range(len(table_date)):
            if date_idx == 2:
                date_str = table_date[date_idx]
                date_and_time = date_str.replace("Datums:", "")
                date_clean = date_and_time.split()[0]
                date_field = "listed_date:" + str(date_clean)
        ad_dict.append(date_field)
        time.sleep(3)
        curr_ad_attributes.append(price_line)
        curr_ad_attributes.append(date_field)
        all_ad_data[ad_url_hash] = curr_ad_attributes
        curr_ad_attributes = []
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


def handler(event, context):
    s3 = boto3.resource('s3')
    page = requests.get("https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/")
    bs_ogre_object = BeautifulSoup(page.content, "html.parser")
    valid_msg_urls = find_single_page_urls(bs_ogre_object)

    advert_data = extract_data_from_url(valid_msg_urls)
    ads_data_json = json.dumps(advert_data, indent = 4)

    full_time = str(datetime.now())
    time_str = full_time.split(" ")[0]

    BUCKET_NAME = "dailycovid19lambda"
    output_file_name = f"ogre_city_raw_data_{time_str}.json"
    OUTPUT_BODY = json.dumps(ads_data_json)
    s3.Bucket(BUCKET_NAME).put_object(Key=output_file_name, Body=OUTPUT_BODY)
