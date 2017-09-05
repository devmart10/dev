import googlemaps
from datetime import datetime, timedelta

gmaps = googlemaps.Client(key='AIzaSyA5ZelhjwojpiU1unrjECjpbOMdUAZhT64')

start = '128 Baytech Dr, San Jose, CA'
end = '390 Maureen Ln, Pleasant Hill, CA'
trans = 'driving'

log_file = str('log_' + str(datetime.now().date()) + '.txt')

log = open(log_file, 'w+')

print('Beginning loop')
for i in range(20):
    now = datetime.now()
    response = gmaps.directions(start, end, mode=trans, departure_time=now)

    seconds = response[0]['legs'][0]['duration_in_traffic']['value']

    # duration = timedelta(seconds=seconds)

    info = 'time {},duration {}\n'.format(now.strftime('%H:%M:%S'), seconds)
    print(info)
    log.writelines(info)

log.close()
