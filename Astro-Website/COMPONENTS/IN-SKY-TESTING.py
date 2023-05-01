import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json

from urllib.request import urlopen

urlopen("https://ipinfo.io/json")

data = json.load(urlopen("https://ipinfo.io/json"))

latitude = float(data['loc'].split(',')[0])
latitude =  float("{:.2f}".format(latitude))
latitude =  float("{:.2f}".format(latitude))
longitude = float(data['loc'].split(',')[1])
longitude = float("{:.2f}".format(longitude))

location = [latitude, longitude]
print(location)


from object_retrieve import get_object_icrs 
from object_retrieve import get_time

time = get_time(location)

#TEST OBJECT
object = "mars"



RADe_object,in_sky = get_object_icrs(time,location,object)
print(in_sky)

if in_sky == True:
    statement = "THIS OBJECT IS UP IN YOUR SKY!"
else:
    statement = "THIS OBJECT IS BELOW YOUR HORIZON"

title_string = "LAT: " + str(latitude) + " LONG: " + str(longitude) + " -- " + statement





with open("Astro-Website/PAGES/object-1-page.html",'r',encoding='utf-8') as object_1_page:
    content = object_1_page.read()

content = content.replace("[[[IN-SKY-1]]]",title_string)

with open("Astro-Website/PAGES/object-1-page.html",'w',encoding='utf-8') as object_1_page:
    object_1_page.write(content)

