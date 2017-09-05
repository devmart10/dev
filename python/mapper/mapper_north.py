import win32api
from datetime import datetime, timedelta
import time
import csv
import googlemaps

# API token
gmaps = googlemaps.Client(key='AIzaSyA5ZelhjwojpiU1unrjECjpbOMdUAZhT64')

# variables
# --------------------------------------------------
filename = 'northbound.csv'
start = '128 Baytech Dr, San Jose, CA'
end = '390 Maureen Ln, Pleasant Hill, CA'
trans = 'driving'
response_frequency = 120 # seconds

use_thresholds = False
duration_threshold = timedelta(hours=1, minutes=0)
delta_threshold = timedelta(minutes=2)
# --------------------------------------------------

# clear log file
with open(filename, 'w', newline='') as file:
    csv.writer(file).writerow(['Time', 'Duration', 'Delta'])

prev = 0
while True:
    # get the data from google
    now = datetime.now()
    try:
        response = gmaps.directions(start, end, mode=trans, departure_time=now)
        seconds = response[0]['legs'][0]['duration_in_traffic']['value']
    except googlemaps.exceptions.Timeout as e:
        print('caught timeout exception:\n', e)
        continue
    except googlemaps.exceptions.ApiError as e:
        print('caught api exception:\n', e)
        continue
    except KeyError as e:
        print('caught key error:\n', e)
        continue

    # find change
    duration = int(seconds / 60)
    delta = duration - prev
    prev = duration

    # format output
    hour = now.ctime().split()[3]   # grabs HH:MM:SS
    row = [hour, duration, delta]
    
    # write output to file
    # ''' 
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
    # '''
    print('time:', row[0], 'minutes:', row[1], 'delta:', row[2])

    # display warning prompt if over thresholds
    if use_thresholds:
        if duration > duration_threshold or delta > delta_threshold:
            message = 'Leave now!\n' + info
            win32api.MessageBox(0, message, 'Time Checker', 0x00001000)

    # wait
    time.sleep(response_frequency)
