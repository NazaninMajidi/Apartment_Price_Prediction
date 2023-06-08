import re
import requests
import mysql.connector
from bs4 import BeautifulSoup

# Define constants
DIVAR_URL = 'https://divar.ir/s/tehran/buy-apartment'
DB_USER = 'user'
DB_PASSWORD = 'password'
DB_HOST = 'host'
DB_NAME = 'DB_APT_Info'

# Create a session object for making requests
session = requests.Session()

# Define a function to extract apartment data from a given ad link
def extract_apartment_data(ad_link):
    res = session.get(ad_link)
    soup = BeautifulSoup(res.text, 'html.parser')
    area_elements = soup.find_all('span', attrs={'class': 'kt-group-row-item__value'})
    price_element = soup.find('p', attrs={'class': 'kt-unexpandable-row__value'})
    address_element = soup.find('div', attrs={'class': 'kt-page-title__subtitle kt-page-title__subtitle--responsive-sized'})

    if len(area_elements) == 6 and len(price_element) == 1 and len(address_element) == 1:
        area = int(area_elements[0].text)
        build_date_text = area_elements[1].text
        room_text = area_elements[2].text
        elevator = area_elements[3].text
        parking = area_elements[4].text
        warehouse = area_elements[5].text
        
        # Process apartment data
        if room_text == 'بدون اتاق':
            room = 0
        elif room_text == '+۴':
            room = 5
        else:
            room = int(room_text)
        
        build_date_regex = re.search(r'(\d+)', build_date_text)
        build_date = int(build_date_regex.group()) if build_date_regex else None
        
        elevator = 1 if elevator == 'آسانسور' else 0
        parking = 1 if parking == 'پارکینگ' else 0
        warehouse = 1 if warehouse == 'انباری' else 0
        
        if price_element.text != 'توافقی':
            price_regex = re.search(r'(.+)\s', price_element.text)
            price = int(price_regex.group().replace('٬', '').strip()) if price_regex else None
        else:
            price = None
            
        address_regex = re.search(r'\،(.+)', address_element.text)
        address = address_regex.group().replace('، ', '') if address_regex else None
        
        return (area, build_date, room, parking, warehouse, elevator, price, address)
    else:
        return None

# Connect to the database
cnx = mysql.connector.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, database=DB_NAME)

# Create a cursor object
cursor = cnx.cursor()

# Get the HTML content of the divar.ir website
res = session.get(DIVAR_URL)
soup = BeautifulSoup(res.text, 'html.parser')

# Extract the links of each apartment ad
ad_links = [item.a['href'] for item in soup.find_all('div', attrs={'class': 'post-card-item-af972 kt-col-6-bee95 kt-col-xxl-4-e9d46'})]

# Loop through each ad link and extract apartment data
for ad_link in ad_links:
    apartment_data = extract_apartment_data('https://divar.ir' + ad_link)
    
    if apartment_data:
        # Insert apartment data into the database
        sql = 'INSERT INTO aptprice (area, build_date, room, parking, warehouse, elevator, price, address) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        cursor.execute(sql, apartment_data)
        cnx.commit()

# Close the database connection
cnx.close()