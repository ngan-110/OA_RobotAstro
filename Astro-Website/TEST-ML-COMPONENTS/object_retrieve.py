import ssl
ssl._create_default_https_context = ssl._create_unverified_context

import os
import operator
import numpy as np
import astropy
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, SkyCoord, EarthLocation, AltAz
from astropy.coordinates import get_body
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

def get_nouns(filename):
    nouns = []
    with open(filename, 'r') as f:
        for line in f:
            nouns.append(line.strip())
    return nouns

def get_object_icrs(time, location, object):
    SolarSystemBodies = ['sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']
    # Convert to lower case
    object = object.lower()
    location = EarthLocation (lat=location[0],lon=location[1])
    altaz = AltAz(obstime=time, location=location)
    if object in SolarSystemBodies:
        # Get the RA and Dec of the object if in solar system
        with solar_system_ephemeris.set('builtin'): # Use for solar system bodies
            RADe_object = get_body(object, time, location) 
            # Get ICRS coordinates
            RADe_object = RADe_object.icrs
    else:
        # A celestial object in ICRS outside the solar system
        RADe_object = SkyCoord.from_name(object)
        no_interp = RADe_object.transform_to(altaz)  
        az = no_interp.az.deg
        alt = no_interp.alt.deg
        
        # IS THIS IMPORTANT TO THE USER?
        if alt > 0:
            in_sky = True
        else:
            in_sky = False
    return RADe_object, in_sky

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image
from io import BytesIO

def get_time(location):
    tz_name = TimezoneFinder().timezone_at(lng=location[1], lat=location[0])
    tz = pytz.timezone(tz_name)
    # Get time at observatory
    now = datetime.now(tz)
    time = Time(now)
    return time

def run_analysis(object,location):
    time = get_time(location)
     # Observation time. Convert to Astropy format
    download_type = 'gif' # Or 'fits'
    data_source = "https://archive.stsci.edu/cgi-bin/dss_form"
    RADe_object, in_sky = get_object_icrs(time, location, object) # Or 'sun' if looking in solar system but sky survey cant retrieve solar system image
    RA_deg = RADe_object.ra.deg
    DE_deg = RADe_object.dec.deg

    RA = RADe_object.ra.hms
    hours, minutes, seconds = RA
    RA = "{}h {}m {:.2f}s".format(hours, minutes, seconds)
    DE = RADe_object.dec.dms
    degrees, minutes, seconds = DE
    # DO I NEED TO HAVE A '+' IN FRONT OF DE?
    if degrees >= 0:
        DE = "+{}d {}m {:.2f}s".format(degrees, minutes, seconds)
    else:
        E = "-{}d {}m {:.2f}s".format(degrees, minutes, seconds)

    # Automating locate elements for data retrieving
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get(data_source)
    ra = browser.find_element(By.NAME, 'r')
    de = browser.find_element(By.NAME, 'd')
    file = browser.find_element(By.XPATH, value="//select[@name='f']")
    terms = browser.find_element(By.XPATH, value="//input[@value='      RETRIEVE IMAGE      ']")

    # Feed RA-DE to the website
    ra.send_keys(RA_deg)
    de.send_keys(DE_deg)
    file.send_keys(download_type) 
    terms.click()

    # Assuming that `browser` is the `WebDriver` object
    image = browser.find_element(By.XPATH, '//img[@style="display: block;-webkit-user-select: none;margin: auto;cursor: zoom-in;background-color: hsl(0, 0%, 90%);"]')
    image_url = image.get_attribute('src')

    # Downloading an image itself
    import requests
    response = requests.get(image_url)
    image_file_name = str(object) + '.gif'

    with open(image_file_name, 'wb') as f:
        f.write(response.content)
    import shutil

    # Define the source and destination paths
    src_path = image_file_name
    dest_path = '../IMAGES/' + image_file_name
    sys_dest_path = 'Astro-Website/IMAGES/' + image_file_name


    # Move the file to the destination directory
    shutil.move(src_path, sys_dest_path)

    return RA, DE, dest_path