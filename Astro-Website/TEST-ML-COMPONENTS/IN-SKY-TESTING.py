import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json

from urllib.request import urlopen

urlopen("https://ipinfo.io/json")

data = json.load(urlopen("https://ipinfo.io/json"))

latitude = float(data['loc'].split(',')[0])
latitude =  float("{:.2f}".format(latitude))
longitude = float(data['loc'].split(',')[1])
longitude = float("{:.2f}".format(longitude))

location = [latitude, longitude]


from object_retrieve import get_object_icrs 
from object_retrieve import get_time

time = get_time(location)

#TEST OBJECT
object = "M3"

RADe_object,in_sky = get_object_icrs(time,location,object)

if in_sky == True:
    statement = "THIS OBJECT IS UP IN YOUR SKY!"
else:
    statement = "THIS OBJECT IS BELOW YOUR HORIZON"

title_string = "LAT: " + str(latitude) + " LONG: " + str(longitude) + " -- " + statement
print(title_string)


