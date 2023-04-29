import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json

from urllib.request import urlopen

urlopen("https://ipinfo.io/json")

data = json.load(urlopen("https://ipinfo.io/json"))

latitude = float(data['loc'].split(',')[0])
latitude =  "{:.2f}".format(latitude)
longitude = float(data['loc'].split(',')[1])
longitude = "{:.2f}".format(longitude)

