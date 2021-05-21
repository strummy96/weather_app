print("Importing modules...")
import datetime
import calendar
import os
import io
import time
from subprocess import call
import PySimpleGUI as sg
from PIL import Image, ImageTk
import json

print("Done importing!")

# ------------------------------variables-----------------------------
current_date = datetime.date.today().strftime('%m.%d.%Y')
location = "D:\\seths_msi\\Documents\\ArcGIS\\Data\\weather\\"
dlocation = location + "data\\"
plocation = location + "products\\"
fc_file = location + 'NWS_fc.txt'
lastupdate_file = location + "data\\" + 'NWS_lastupdate.txt'
precip814_png = "D:\\seths_msi\\Documents\\ArcGIS\\Data\\weather\\products\\precip_outlook" + \
                str(current_date) + ".png"
NWS_logo = location + "images\\NWS_logo_250x250.png"
filelist = os.listdir(plocation)
for file in filelist:
    if 'temp_fc' in file:
        temp_fc_png = plocation + file
get_NWS_data = 'C:\\Users\\seths\\Documents\\ArcGIS\\python scripts\\get_NWS_data.py'

# extract forecast disc
fc_reader = open(fc_file, 'r')
fc_text = fc_reader.read()
fc_reader.close()

# get hilo temps as list 'temps'
hilo_temps = dlocation + "config\\hilo_config.json"
with open(hilo_temps) as f:
    hilo_dict = json.load(f)
temps_ = hilo_dict['temps'].strip('][').split(', ')
temps = []
for x in range(len(temps_)):
    temps.append(temps_[x][1:3])

# get hilo variable from hilo_dict
hilo = hilo_dict['hilo']
if hilo == 'low':
    temps.insert(0, '  ')
if hilo == 'high':
    temps.append('  ')

# check on last update file
if os.path.exists(lastupdate_file):
    print("lastupdate_file exists")
    lastupdate_reader = open(lastupdate_file, 'r')
    last_update = lastupdate_reader.read()
    lastupdate_reader.close()
else:
    lastupdate_reader = open(lastupdate_file, 'w+')
    lastupdate_reader.close()

print("Last Update: " + last_update)

# ------------------------------------functions--------------------------------------------
def get_image_data(f, maxsize=(800, 800), first=False):
    img = Image.open(f)
    img.thumbnail(maxsize)
    if first:
        bio = io.BytesIO()
        img.save(bio, format="PNG")
        del img
        return bio.getvalue()
    return ImageTk.PhotoImage(img)

# --------------------------elements----------------------------------------------------------------------------
# launch window elements
info_text_element = sg.Text('This is an app for displaying NWS Forecasts.', font=30)
NWS_logo_elem = sg.Image(data=get_image_data(NWS_logo, first=True), size=(250,250), pad=(5,5))
update_data_element = sg.Button('Get new products from NWS', size=(40,2), font=20, button_color='black on gold')
close_button_element = sg.Button('Close', size=(40,2), font=20, button_color='firebrick3')
last_update_elem = sg.Text('Last Update: ' + str(last_update), size=(30, None), key='-UPDATETIME-', justification='center')
line_text = sg.Text('_______________________')
fc_button = sg.Button('Forecast Discussion', size=(40,2), font=20)
precip_button = sg.Button('8-14 Day Precipitation Outlook', size=(40,2), font=20)
max_temp_button = sg.Button('Tomorrow\'s Max Temperature Forecast', size=(40,2), font=20)
attribution_text = sg.Text('Created by: Seth Strumwasser', text_color='grey60')

# ---------------------------temp display---------------------------------------
# Day dictionary - each key is an integer 0-6 representing today (0) and each subsequent day.
# The values are the name of the weekday for each correspending date.
day_dict = {}
for j in range(0,10):
    date_ = datetime.date.today() + datetime.timedelta(days=j)
    date_y = date_.year
    date_m = date_.month
    date_d = date_.day
    day_dict[str(j)] = (str(calendar.day_name[datetime.date(date_y, date_m, date_d).weekday()]))

# Day elements dictionary - each key is an integer 0-6 representing today(0) and each subsequent day.
# Each value is a text element displaying the value from day_dict (the day of the week).
day_elem_dict = {}
for i in range(0,10):
    day_elem_dict[str(i)] = sg.Text(day_dict[str(i)], font=10)
col_hilo = sg.Col([[sg.Text('')],
                   [sg.Text('High:' + ' (\xb0' + 'F)', text_color='red', font=10)],
                   [sg.Text('Low:' + ' (\xb0' + 'F)', text_color='blue', font=10)]])

# list of column elements
col_list = [col_hilo]
for i, j in [(0,1), (2,3), (4,5), (6,7), (8,9), (10,11), (12,13)]:
        col_list.append(sg.Column([[day_elem_dict[str(int(j-(i/2)-1))]],
                        [sg.Text(temps[i], font=20, key='-TEMPCOL' + str(i) + '-')],
                        [sg.Text(temps[j], font=20, key='-TEMPCOL' + str(j) + '-')]], element_justification='center'))

print(col_list)
# -----------------------columns setup-----------------------------------------------------------------
# launch_window columns
col1layout = [
            [info_text_element],
            [NWS_logo_elem],
            [update_data_element],
            [last_update_elem],
            [line_text],
            col_list,
            [fc_button],
            [precip_button],
            [max_temp_button],
            [close_button_element],
            [attribution_text]
        ]
col1 = sg.Column(col1layout, element_justification='center')

#layout
layout_launch = [[col1]]

# launch_window
launch_window = sg.Window('NWS Weather App', layout_launch, finalize=True, element_justification='center')

img_win_active = False
fc_win_active = False
temp_win_active = False

# launch window loop
while True:
    ev_launch, val_launch = launch_window.read(timeout=100)
    if ev_launch == sg.WIN_CLOSED or ev_launch == 'Close':
        break

    # forecast discussion
    if ev_launch == 'Forecast Discussion':
        fc_win_active=True
        launch_window.Hide()
        fc_reader = open(fc_file, 'r')
        fc_text = fc_reader.read()
        fc_reader.close()
        layout_fc = [[sg.Column([[sg.Text(fc_text, font=15, key='-DISC-')]], scrollable=True, vertical_scroll_only=True,
                                size=(800, 600),
                                element_justification='center')],
                     [sg.Column([[sg.Button('Back to products', font=10)]], justification='center', element_justification='center')]]
        fc_window = sg.Window('NWS Weather App', layout_fc, size=(675,700))
        while True:
            ev_fc, val_fc = fc_window.read()
            if ev_fc == sg.WIN_CLOSED:
                break
            if ev_fc == 'Back to products':
                fc_window.close()
                fc_win_active=False
                del layout_fc
                launch_window.UnHide()

    # precip outlook
    if ev_launch == '8-14 Day Precipitation Outlook':
        img_win_active=True
        launch_window.Hide()
        layout_img = [[sg.Column([[sg.Image(data=get_image_data(precip814_png, first=True), size=(800, 800), key='-IMAGE-')],
                                  [sg.Button('Back to products')]], element_justification='center')]]
        img_window = sg.Window('NWS Weather App', layout_img, )
        while True:
            ev_img, val_img = img_window.read()
            if ev_img == sg.WIN_CLOSED:
                break
            if ev_img == 'Back to products':
                img_window.close()
                img_win_active=False
                del layout_img
                launch_window.UnHide()

    # get new products
    if ev_launch == 'Get new products from NWS':
        confirm = sg.popup_ok_cancel('This may take a few minutes - proceed?')
        if confirm == 'OK':
            sg.popup_no_buttons('Getting new products...', non_blocking=True, auto_close=True, keep_on_top=True)
            call(['python', get_NWS_data])
            sg.popup_ok('Done!')

            # update element
            t = time.localtime()
            current_time = time.strftime('%H:%M:%S', t)
            launch_window['-UPDATETIME-'].update('Last Update: ' + current_date + ' ' + current_time)
            for i, j in [(0,1), (2,3), (4,5), (6,7), (8,9), (10,11), (12,13)]:
                launch_window['-TEMPCOL' + str(i) + '-'].update()
                launch_window['-TEMPCOL' + str(j) + '-'].update()

    # Tomorrows temp forecast
    if ev_launch == 'Tomorrow\'s Max Temperature Forecast':
        temp_win_active=True
        launch_window.Hide()
        layout_temp = [[sg.Column([[sg.Image(data=get_image_data(temp_fc_png, first=True), key='-TEMP-')],
                                   [sg.Button('Back to products')]], element_justification='center')]]
        temp_window = sg.Window('Max Temperature Forecast', layout_temp, no_titlebar=True)
        while True:
            ev_temp, val_temp = temp_window.read()
            if ev_temp == sg.WIN_CLOSED:
                break
            if ev_temp == 'Back to products':
                temp_window.close()
                temp_win_active=False
                del layout_temp
                launch_window.UnHide()


launch_window.close()
