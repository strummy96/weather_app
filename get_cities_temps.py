from bs4 import BeautifulSoup
import requests
import re

page_1 = 'https://forecast.weather.gov/product.php?site=CRH&product=SCS&issuedby=01'
page_2 = 'https://forecast.weather.gov/product.php?site=CRH&product=SCS&issuedby=02'
page_3 = 'https://forecast.weather.gov/product.php?site=CRH&product=SCS&issuedby=03'
page_4 = 'https://forecast.weather.gov/product.php?site=CRH&product=SCS&issuedby=04'

csv_dict = {}

states_abbr = ["AK","AL","AR","AZ","CA","CO","CT","DC","DE","FL","GA","GU",
                                                           "HI","IA","ID", "IL","IN","KS","KY","LA","MA","MD","ME",
                                                           "MH","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM",
                                                           "NV","NY", "OH","OK","OR","PA","PR","PW","RI","SC","SD",
                                                           "TN","TX","UT","VA","VI","VT","WA","WI","WV","WY"]

def getCitiesTemps(url, page_num):
    # text from webpage
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    fc_string = soup.pre.getText()

    # make list of lines in fc_string
    fc_lines_list = fc_string.splitlines()

    # make a list of lists of words in each line
    fc_list_of_line_wordlists = []
    for x in fc_lines_list:
        fc_list_of_line_wordlists.append(x.split())

    # make a list of strings - each consists of the words of each line separated by commas
    fc_csv_line_str = []
    for x in range(len(fc_list_of_line_wordlists)):
        fc_csv_line_str.append('')
        for y in range(len(fc_list_of_line_wordlists[x])):
            try:
                if fc_list_of_line_wordlists[x][y].isalpha() is True and \
                        fc_list_of_line_wordlists[x][y+1].isalpha() is True and \
                        fc_list_of_line_wordlists[x][y+1] not in states_abbr:
                    fc_csv_line_str[x] += fc_list_of_line_wordlists[x][y] + ' '
                elif fc_list_of_line_wordlists[x][y] in states_abbr:
                    continue
                elif fc_list_of_line_wordlists[x][y+1] in states_abbr:
                    fc_csv_line_str[x] += fc_list_of_line_wordlists[x][y] + ','
                else:
                    fc_csv_line_str[x] += fc_list_of_line_wordlists[x][y] + ','
            except IndexError:
                fc_csv_line_str[x] += fc_list_of_line_wordlists[x][y] + ','

    # check for precip value - if none, add blank space
    listoflists_precip = []
    for x in fc_csv_line_str:
        listoflists_precip.append(x.split(','))
    for x in listoflists_precip:
        try:
            if x[3][0].isalpha() is True:
                x.insert(3, '0')
        except IndexError:
            continue

    # make city names title case
    capital_list = []
    for x in listoflists_precip:
        # print(x)
        if len(x) > 0:
            capital_list.append(x[0].title())
    for x in range(len(listoflists_precip)):
        try:
            listoflists_precip[x][0] = capital_list[x]
            print(listoflists_precip[x])
        except IndexError:
            pass

    # return to list of strings
    fc_csv_line_str_precip = []
    for x in range(len(listoflists_precip)):
        fc_csv_line_str_precip.append('')
        for y in range(len(listoflists_precip[x])):
            fc_csv_line_str_precip[x] += listoflists_precip[x][y] + ','

    # remove slashes
    fc_csv_line_str_noslash = []
    for x in fc_csv_line_str_precip:
        fc_csv_line_str_noslash.append(x.replace('/', ','))

    # combine into one large csv string with line breaks
    fc_csv = ''
    for x in range(len(fc_csv_line_str_noslash)):
        if page_num == '1':
            if x in range(0,14) or x == 15 or x in range(len(fc_csv_line_str_noslash)-5,len(fc_csv_line_str_noslash)):
                pass
                print(fc_csv_line_str_noslash[x])
            elif x == 14:
                fc_csv_line_str_noslash[14] = 'CITY,HI,LO,PCPN,WEA+11,HI+1,LO+1,WEA+2,HI+2,LO+2,,'
                fc_csv += fc_csv_line_str_noslash[x] + '\n'
            else:
                fc_csv += fc_csv_line_str_noslash[x] + '\n'
        else:
            if x in range(0,16) \
                    or x in range(len(fc_csv_line_str_noslash)-5,len(fc_csv_line_str_noslash))\
                    or x == 0:
                pass
            elif x == 14:
                fc_csv_line_str_noslash[14] = 'CITY,HI,LO,PCPN,WEA+1,HI+1,LO+1,WEA+2,HI+2,LO+2,,'
                fc_csv += fc_csv_line_str_noslash[x] + '\n'
            else:
                fc_csv += fc_csv_line_str_noslash[x] + '\n'
    # print('fc_csv = ' + fc_csv)

    # write text to dictionary for use in concatenation
    csv_dict[page_num] = fc_csv

    # write to csv
    file = 'D:\\seths_msi\\Documents\\GIS Data\\cities_temps_pg' + page_num + '.csv'
    file_reader = open(file, 'w+')
    file_reader.write(fc_csv)
    file_reader.close()

# get data for each page and make csv
getCitiesTemps(page_1, '1')
getCitiesTemps(page_2, '2')
getCitiesTemps(page_3, '3')
getCitiesTemps(page_4, '4')

# combine 4 csvs into one
master_csv = ''

for key in csv_dict:
    master_csv += csv_dict[key]
    # print(str(key))
    # print(csv_dict[key])
    # print("break")
file = 'D:\\seths_msi\\Documents\\GIS Data\\cities_temps_master.csv'
file_reader = open(file, 'w+')
file_reader.write(master_csv)
file_reader.close()