print("Importing modules...")
import requests
from bs4 import BeautifulSoup
import os.path
from os import path, remove
import time

print("Done.")

print("Fetching data...")
response = requests.get(
    'https://forecast.weather.gov/product.php?site=STO&issuedby=STO&product=AFD&format=CI&version=1&glossary=1'
)
soup = BeautifulSoup(response.text, 'html.parser')
fc_text = soup.pre.getText()
location = "D:\\seths_msi\\Documents\\ArcGIS\\Data\\weather\\"
fc_file = location + 'NWS_fc.txt'

print("Data acquired.")
print("Checking for old data...")
if os.path.exists(fc_file) == True:
    os.remove(fc_file)

print("Creating txt file...")
file = open(fc_file, 'w+')
file.write(fc_text)
file.close()

file = open(fc_file, 'r')
file.close()
print("Done!")

date_modified_epoch = path.getmtime(fc_file)
date_modified = str(time.ctime(date_modified_epoch))