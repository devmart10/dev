import win32api
from datetime import datetime, timedelta
import time
import csv
import googlemaps
import sys
import os

# variables
# --------------------------------------------------
n_filename = 'northbound.csv'
s_filename = 'southbound.csv'
home = '390 Maureen Ln, Pleasant Hill, CA'
work = '128 Baytech Dr, San Jose, CA'
trans = 'driving'
response_frequency = 120  # seconds

use_thresholds = False
duration_threshold = timedelta(hours=1, minutes=0)
delta_threshold = timedelta(minutes=2)
# --------------------------------------------------

def log_info(filename, duration, delta):
    # format output
    hour = str(datetime.now().ctime().split()[3])   # HH:MM:SS
    row = [hour, duration, delta]
     # write output to file
    # '''
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(row)
    # '''
    print('{:<15} {:>10},{:>3},{:>3}'.format(filename, row[0], row[1], row[2]))


def get_dur(gmaps, departing, arriving):
    # get the data from google
    now = datetime.now()
    seconds = 0
    try:
        response = gmaps.directions(departing, arriving, mode=trans, departure_time=now)
        seconds = response[0]['legs'][0]['duration_in_traffic']['value']
    except googlemaps.exceptions.Timeout as e:
        print('caught timeout exception:\n', e)
    except googlemaps.exceptions.ApiError as e:
        print('caught api exception:\n', e)
    except KeyError as e:
        print('caught error:\n', e)

    # find change
    duration = int(seconds / 60)
    return duration

def main():
    # API token
    gmaps = googlemaps.Client(key='AIzaSyA5ZelhjwojpiU1unrjECjpbOMdUAZhT64')

    # parse command line args
    flags = []
    if len(sys.argv) > 1:
        flags = sys.argv[1:]

    # group logs by day
    today = str(datetime.now().date())
    if not os.path.isdir(today):
        os.mkdir(today)
    os.chdir(today)

    # clear log files
    if '--clear' in flags:
        print('overwriting existing logs')
        # clear log file
        with open(n_filename, 'w', newline='') as file:
            csv.writer(file).writerow(['Time', 'Duration', 'Delta'])
        with open(s_filename, 'w', newline='') as file:
            csv.writer(file).writerow(['Time', 'Duration', 'Delta'])

    n_prev = 0
    s_prev = 0
    while True:
        n_dur = get_dur(gmaps, work, home)
        n_delta = n_dur - n_prev
        n_prev = n_dur

        s_dur = get_dur(gmaps, home, work)
        s_delta = s_dur - s_prev
        s_prev = s_dur

        log_info(n_filename, n_dur, n_delta)
        log_info(s_filename, s_dur, s_delta)
        print()

        # wait
        time.sleep(response_frequency)

if __name__ == '__main__':
    main()