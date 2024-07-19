import datetime
import re
import time
import boto3
import requests
import os
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


def extract_data_from_url(nondup_urls: list) -> None:
    """Iterate over all first page msg urls 
    scrape advert data from each url and write 
    to file Ogre-raw-data-report.txt"""

    dest_file="Ogre-raw-data-report.txt"
    msg_url_count = len(nondup_urls)
    for i in range(msg_url_count): # Original line
        current_msg_url = nondup_urls[i] + "\n"
        table_opt_names = get_msg_table_info(nondup_urls[i], "ads_opt_name")
        table_opt_values = get_msg_table_info(nondup_urls[i], "ads_opt")
        table_price = get_msg_table_info(nondup_urls[i], "ads_price")

        print(f"Extracting data from message URL  {i + 1}")
        write_line(current_msg_url, dest_file)
        for idx in range(len(table_opt_names) - 1):
            text_line = table_opt_names[idx] + ">" + table_opt_values[idx] + "\n"
            write_line(text_line, dest_file)

        # Extract message price field
        price_line = "Price:>" + table_price[0] + "\n"
        write_line(price_line, dest_file)

        # Extract message publish date field
        table_date = get_msg_table_info(nondup_urls[i], "msg_footer")
        for date_idx in range(len(table_date)):
            if date_idx == 2:
                date_str = table_date[date_idx]
                date_and_time = date_str.replace("Datums:", "")
                date_clean = date_and_time.split()[0]
                date_field = "Date:>" + str(date_clean) + "\n"
        write_line(date_field, dest_file)
        time.sleep(2)


def write_line(text: str, file_name: str) -> None:
    """Append text to end of the file"""
    with open(file_name, 'a') as the_file:
        the_file.write(text)


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


def upload_text_file_to_s3(file_path, bucket_name, s3_key) -> None:
    """
    Uploads a text file to an S3 bucket.

    :param file_path: The local path to the text file.
    :param bucket_name: The name of the S3 bucket to upload the file to.
    :param s3_key: The S3 key to use for the uploaded file.
    """
    s3_client = boto3.client('s3')
    with open(file_path, 'rb') as file:
        s3_client.upload_fileobj(file, bucket_name, s3_key)


def add_datetime_to_filename(filename):
    """
    Adds the current date and time to a filename.

    :param filename: The original filename.
    :return: The new filename with the current date and time added.
    """

    # Get the current date and time in YYYY-MM-DDTHH-MM-SS format
    current_datetime = datetime.datetime.now().strftime('%Y-%m-%dT%H-%M-%S')

    # Add the current date and time to the filename
    new_filename = filename.replace('.txt', f'-{current_datetime}.txt')

    return new_filename


def handler(event, context):  # Original code line
    """lambda main entry point"""
    # page = requests.get("https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/")
    # bs_ogre_object = BeautifulSoup(page.content, "html.parser")
    # valid_msg_urls = find_single_page_urls(bs_ogre_object)
    
    # New static way of extracting data from first three pages
    # TODO: make this dynamic
    page_one = requests.get("https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/")
    page_two = requests.get("https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/page2.html")
    page_three = requests.get("https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/page3.html")
    
    # Error handling behavior by ss.lv
    # If non existing page requested for example https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/page4.html
    # it rederacts to first page https://www.ss.lv/lv/real-estate/flats/ogre-and-reg/ogre/sell/page.html

    page_one_bs_obj = BeautifulSoup(page_one.content, "html.parser")
    page_two_bs_obj = BeautifulSoup(page_two.content, "html.parser")
    page_three_bs_obj = BeautifulSoup(page_three.content, "html.parser")
    
    page_one_msg_urls = find_single_page_urls(page_one_bs_obj)
    page_two_msg_urls = find_single_page_urls(page_two_bs_obj)
    page_three_msg_urls = find_single_page_urls(page_three_bs_obj)
    combined_urls = page_one_msg_urls +  page_two_msg_urls + page_three_msg_urls
    # Since currently there is no dynamic page cound extraction avilable 
    # curent behavior of ss.lv if you request none existing page it redirects to
    # first page current quick fix is to remove duplicate entries because of scenario 
    # if page 3 is missing an you have requested it will gra  urls from first page and 
    # it will end up with duplicate entries
    valid_msg_urls = list(set(combined_urls))
    
    # Change directory to /tmp folder
    os.chdir('/tmp')    # lambda allows to write only in /tmp
    extract_data_from_url(valid_msg_urls)

    original_filename = "Ogre-raw-data-report.txt"
    new_filename = add_datetime_to_filename(original_filename)
    S3_bucket="lambda-ogre-scraped-data"
    upload_text_file_to_s3(original_filename, S3_bucket, new_filename )
    # Output: Ogre-raw-data-report-2023-02-18.txt (if today is February 18, 2023)
    print(f"File {new_filename} was uploaded to S3 bucket successfully" )

    return {'status': 'True',
            'statusCode': 200,
            'body': 'File with scraped data was uploaded to S3 bucket successfully'}




