print("Importing modules...")
import requests
from bs4 import BeautifulSoup
import os.path
from os import path, remove
import time
import json

print("Done.")

# get text from website
print("Fetching data...")
response = requests.get(
    'https://forecast.weather.gov/MapClick.php?lat=38.5794&lon=-121.4909&unit=0&lg=english&FcstType=text&TextType=1'
)
soup = BeautifulSoup(response.text, 'html.parser')
fc_text = soup.getText()
# print("Entire text:")
# print("...")
# print(fc_text)
location = "D:\\seths_msi\\Documents\\ArcGIS\\Data\\weather\\data\\config\\"
fc_file = location + 'hilo_config.json'

# remove \n from fc_text
fc_text_no_breaks = fc_text.replace('\n', ' ')

# create list of words in the text
fc_text_words = fc_text_no_breaks.split(' ')


# create list of temperatures by finding the word before them
indices = []
temps = []
temps_ = []

for x, y in enumerate(fc_text_words):
    if y == 'near' or y == 'around':
        indices.append(x)
        temps.append(fc_text_words[x+1])
for x in temps:
    temps_.append((x)[0:2])
# print("Indices: ", indices)
# print("Temps: ", temps_)

# set hilo variable by finding which index comes first.
# near is high temp, around is low temp.
# so, near<around means high comes first.
near_loc = fc_text_words.index('near')
around_loc = fc_text_words.index('around')

hilo = ''
if near_loc < around_loc:
    hilo = 'high'
if near_loc > around_loc:
    hilo = 'low'

print("Data acquired.")
print("Checking for old data...")
if os.path.exists(fc_file) == True:
    os.remove(fc_file)

json_dict = {'temps' : str(temps_), 'hilo' : hilo}
with open(fc_file, 'w') as outfile:
    json.dump(json_dict, outfile)

print("Done!")