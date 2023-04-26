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
    #print('Azimuth: ', az)
    #print('Altitude: ', alt)
    # Check if viewable from location
    if alt > 0:
        print('Object is viewable from location of viewer')
    return RADe_object

def run_analysis(object):
    # Get location at specific observation site
    obs_location = EarthLocation.of_address('New York, NY')
    tz_name = TimezoneFinder().timezone_at(lng=obs_location.lon.degree, lat=obs_location.lat.degree)
    tz = pytz.timezone(tz_name)
    # Get time at observatory
    now = datetime.now(tz)
    time = Time(now) # Observation time. Convert to Astropy format
    download_type = 'gif' # Or 'fits'
    data_source = "https://archive.stsci.edu/cgi-bin/dss_form"
    RADe_object = get_object_icrs(time, obs_location, object) # Or 'sun' if looking in solar system but sky survey cant retrieve solar system image
    RA = RADe_object.ra.deg
    DE = RADe_object.dec.deg

    # Automating locate elements for data retrieving
    browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    browser.get(data_source)
    ra = browser.find_element(By.NAME, 'r')
    de = browser.find_element(By.NAME, 'd')
    file = browser.find_element(By.XPATH, value="//select[@name='f']")
    terms = browser.find_element(By.XPATH, value="//input[@value='      RETRIEVE IMAGE      ']")

    # Feed RA-DE to the website
    ra.send_keys(RA)
    de.send_keys(DE)
    file.send_keys(download_type) 
    terms.click()

    return RA, DE

run_analysis('M3')