
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json
from urllib.request import urlopen
import os
import requests
import shutil
import astropy
from astropy.time import Time
from astropy.coordinates import solar_system_ephemeris, SkyCoord, EarthLocation, AltAz
from astropy.coordinates import get_body, name_resolve
from datetime import datetime
from timezonefinder import TimezoneFinder
import pytz
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys


# Define constants
LIST_OBJECTS = 'Astro-Website\DATA\list_objects.txt'
obj_1_template = 'Astro-Website\PAGES\TEMPLATES\object-1-page.html'
obj_2_template = 'Astro-Website\PAGES\TEMPLATES\object-2-page.html'
obj_3_template = 'Astro-Website\PAGES\TEMPLATES\object-3-page.html'
obj_1_page = 'Astro-Website\PAGES\object-1-page.html'
obj_2_page = 'Astro-Website\PAGES\object-2-page.html'
obj_3_page = 'Astro-Website\PAGES\object-3-page.html'
OBJ_1 = "[[[OBJECT-1]]]"
OBJ_2 = "[[[OBJECT-2]]]"
OBJ_3 = "[[[OBJECT-3]]]"
data_source = "https://archive.stsci.edu/cgi-bin/dss_form"
SolarSystemBodies = ['sun', 'mercury', 'venus', 'earth', 'moon', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune', 'pluto']


def get_object_icrs(time, observer_location, object):
    '''
    Get the RA and Dec of an object in ICRS coordinates
    input:
        time: Astropy time object, ex: 2023-05-04 01:01:15.124348
        location: Tuple of latitude and longitude of observer, ex: [40.73, -74.01]
        object: Name of object, string
    return:
        RADe_object: Astropy SkyCoord object of object in ICRS coordinates
            ex: <SkyCoord (ICRS): (ra, dec) in deg
                    (57.2905941, 24.05341674)>
        in_sky: Boolean, True if object is above horizon, False if below
    '''
    # Convert to lower case
    object = object.lower()
    location = EarthLocation (lat=observer_location[0],lon=observer_location[1])
    altaz = AltAz(obstime=time, location=location)
    if object in SolarSystemBodies:
        # Get the RA and Dec of the object if in solar system
        with solar_system_ephemeris.set('builtin'): # Use for solar system bodies
            RADe_object = get_body(object, time, location) 
            # Get ICRS coordinates
            RADe_object = RADe_object.icrs
    else:
        # A celestial object in ICRS outside the solar system
        # Check if astropy rasies an error
        try:
            SkyCoord.from_name(object)
        except astropy.coordinates.name_resolve.NameResolveError:
            # If there is an error, return None
            return None, None
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

def get_time(observer_location):
    '''
    Get the time at the observatory
    input:
        observer_location: Tuple of latitude and longitude of observer, ex: [40.73, -74.01]
    return:
        time: Astropy time object, ex: 2023-05-04 01:01:15.124348
    '''
    tz_name = TimezoneFinder().timezone_at(lng=observer_location[1],lat=observer_location[0])
    tz = pytz.timezone(tz_name)
    # Get time at observatory
    now = datetime.now(tz)
    time = Time(now)
    return time

def run_analysis(object, observer_location):
    '''
    Get object RA, DE, get image of object, if object is in sky
    input:
        object: Name of object, string
        observer_location: Tuple of latitude and longitude of observer
    return:
        RA: Right ascension of object, string, ex: 3.0h 49.0m 9.74s
        DE: Declination of object, string, ex: +24.0d 3.0m 12.30s
        dest_path: Path to image of object, string, ex: ../IMAGES\Atlas.gif
        in_sky: Boolean, True if object is in sky, False if not    
    '''
    time = get_time(observer_location)
     # Observation time. Convert to Astropy format
    download_type = 'gif' # Or 'fits'
    # Get RA and Dec of object and check if it's viewable at observer's location
    RADe_object, in_sky = get_object_icrs(time, observer_location, object) # Or 'sun' if looking in solar system but sky survey cant retrieve solar system image
    # If object is not in CDS database, return None
    if RADe_object is None:
        RA = 'None'
        DE = 'None'
        dest_path = os.path.join('../IMAGES', 'not_found.jpg')
        return RA, DE, dest_path, in_sky
    RA_deg = RADe_object.ra.deg
    DE_deg = RADe_object.dec.deg

    RA = RADe_object.ra.hms
    DE = RADe_object.dec.dms
    ra_hours, ra_minutes, ra_seconds = RA
    de_degrees, de_minutes, de_seconds = DE
    RA = "{}h {}m {:.2f}s".format(ra_hours, ra_minutes, ra_seconds)
    DE = "+{}d {}m {:.2f}s".format(de_degrees, de_minutes, de_seconds)

    # If object is in Solar system, use predownloaded images of solar system bodies
    if object in SolarSystemBodies:
        dest_path = os.path.join('Astro-Website/IMAGES', object + '.jpg')
    # If object is not in Solar system, download image from sky survey
    else:  
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
        response = requests.get(image_url)
        image_file_name = str(object) + '.gif'
        with open(image_file_name, 'wb') as f:
            f.write(response.content)
        # Define the source and destination paths
        src_path = image_file_name
        dest_path = os.path.join('../IMAGES', image_file_name)
        sys_dest_path = os.path.join('Astro-Website/IMAGES', image_file_name)

        # Move the file to the destination directory
        shutil.move(src_path, sys_dest_path)
    return RA, DE, dest_path, in_sky

def generate_obj_list(filename):
    '''
    Generates a list of the most popular objects from file
    input: file name, string
    output: list of objects, list
    '''
    with open(filename,'r') as pop_topics_file:
        object_list = []
        counter = 0
        for line in pop_topics_file:
            line = line[:-1]
            if counter < 3:
                object_list.append(line)
                counter += 1
            else:
                break
    return object_list

def modify_object_page (object, object_page, current_object, top_object):
    '''
    Modify object page with object info
    input: object, string
           object_page, string
           current_object, string
           top_object, string
    output: None
    '''
    with open(object_page,'r', encoding='utf-8') as obj_file:
        new_content = obj_file.read()
    modified_object_page = new_content.replace(OBJ_1,top_object.upper())
    if (object_page != obj_1_page):
        modified_object_page = modified_object_page.replace(current_object,object.upper())
    with open(object_page,'w', encoding='utf-8') as file:
        file.write(modified_object_page)

def update_obj_html():  
    # Remove the old object pages 
    if os.path.exists(obj_1_page):
        os.remove(obj_1_page)
    if os.path.exists(obj_2_page):
        os.remove(obj_2_page) 
    if os.path.exists(obj_3_page):
        os.remove(obj_3_page)
    # Copy the template to the object page
    os.system('copy ' + obj_1_template + ' ' + obj_1_page)
    os.system('copy ' + obj_2_template + ' ' + obj_2_page)  
    os.system('copy ' + obj_3_template + ' ' + obj_3_page)
    # Generate the object list
    object_list = generate_obj_list(LIST_OBJECTS)
    # TODO: Rewrite into functions
    # MODIFYING OBJECT-1-PAGE...
    modify_object_page(object_list[0], obj_1_page, OBJ_1, object_list[0])
    # MODIFYING OBJECT-2-PAGE...
    modify_object_page(object_list[1], obj_2_page, OBJ_2, object_list[0])
    # MODIFYING OBJECT-3-PAGE...
    modify_object_page(object_list[2], obj_3_page, OBJ_3, object_list[0])
        
    # Print complete messages
    print('UPDATED OBJECT HTMLS')
    print('Object list:', object_list)    

    #&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
    urlopen("https://ipinfo.io/json")
    data = json.load(urlopen("https://ipinfo.io/json"))
    latitude = float(data['loc'].split(',')[0])
    latitude =  float("{:.2f}".format(latitude))
    longitude = float(data['loc'].split(',')[1])
    longitude = float("{:.2f}".format(longitude))
    
    observer_location = [latitude, longitude]

    # TO UPDATE EACH OF THE OBJECT HTMLS WITH LOCATION INFORMATION #
    for i in range(len(object_list)):
        # TODO: MAKE A COPY OF BELOW STUFF!!!
        file_name = 'Astro-Website/PAGES/object-' + str(i+1) + '-page.html'
        IN_SKY_ref = '[[[IN-SKY-' + str(i+1) + ']]]'
        RA_ref = '[[[RA-' + str(i+1) + ']]]'
        DEC_ref = '[[[DEC-' + str(i+1) + ']]]'
        IMAGE_ref = '[[[IMAGE-' + str(i+1) + ']]]'
        
        RA, DEC, IMAGE_path, in_sky = run_analysis(object_list[i],observer_location)

        if in_sky == True:
            statement = "THIS OBJECT IS UP IN YOUR SKY!"
        else:
            statement = "THIS OBJECT IS BELOW YOUR HORIZON"
        in_sky_statement = "YOUR LAT: " + str(latitude) + " YOUR LONG: " + str(longitude) + " ... <b>" + statement + "</b>"

        # Updating object htmls with location information + images #
        with open(file_name,'r',encoding='utf-8') as file:
            content = file.read()
        modified_file = content.replace(RA_ref,RA)
        modified_file = modified_file.replace(DEC_ref,DEC)
        modified_file = modified_file.replace(IN_SKY_ref,in_sky_statement)

        modified_file = modified_file.replace(IMAGE_ref,IMAGE_path)

        with open(file_name,'w',encoding='utf-8') as file:
            file.write(modified_file)
        print('UPDATED OBJECT-' + str(i+1) + '-PAGE.HTML')
        print('Object:', object_list[i])