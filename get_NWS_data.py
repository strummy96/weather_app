import subprocess
import datetime
import time

# paths
precip_outlook = 'C:\\Users\\seths\\Documents\\ArcGIS\\python scripts\\precip_outlook.py'
get_forecast_discussion = 'C:\\Users\\seths\\Documents\\ArcGIS\\python scripts\\get_NWS_fc.py'
get_temp_fc = 'C:\\Users\\seths\\Documents\\ArcGIS\\python scripts\\get_temp_fc.py'
hilo_temps = 'C:\\Users\\seths\\Documents\\ArcGIS\\python scripts\\hilo_temps.py'
cities_temps = 'C:\\Users\\seths\\Documents\\ArcGIS\\python scripts\\get_cities_temps.py'

# calls
print("Running script: " + precip_outlook)
subprocess.call(['python', precip_outlook])
print("Running script: " + get_forecast_discussion)
subprocess.call(['python', get_forecast_discussion])
print("Running script: " + hilo_temps)
subprocess.call(['python', hilo_temps])
print("Running script: " + cities_temps)
subprocess.call(['python', cities_temps])

# update 'last update' time and date
print("Updating last update time and date...")
t = time.localtime()
current_time = time.strftime('%H:%M:%S', t)
current_date = datetime.date.today().strftime('%m.%d.%Y')
location = "D:\\seths_msi\\Documents\\ArcGIS\\Data\\weather\\"
lastupdate_file = location + "data\\" + 'NWS_lastupdate.txt'

lastupdate_reader = open(lastupdate_file, 'w+')
lastupdate_reader.write(current_date + ' ' + current_time)
last_update = lastupdate_reader.read()
lastupdate_reader.close()
print("Done!")