import pyowm

owm = pyowm.OWM('c3ceda868af1a1f24425481f140bd2c7')

city = 'Pleasant Hill,US'

observation = owm.weather_at_place(city)
w = observation.get_weather()

temps = w.get_temperature('fahrenheit')
temp = temps['temp']
rains = w.get_rain()
rain = 0
if rains:
	rain = rains['3h']

print('Current temp in', city, 'is:', temp)
print('There is', rain, 'cm of rain')
print()

if temp > 70 and rain < .5:
	print('Good weather for Gamera!')
else:
	print('Too cold or rainy for turtles!')