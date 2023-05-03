#pip install timezonefinder
import ssl
ssl._create_default_https_context = ssl._create_unverified_context
import json
from urllib.request import urlopen
import os
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
final_objects = 'Astro-Website\DATA\list_objects.txt'
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


def get_object_icrs(time, location, object):
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
        # Check if astropy rasies an error
        if (name_resolve(object)._parse_response() == None):
            return None, False
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
def get_time(location):
    tz_name = TimezoneFinder().timezone_at(lng=location[1],lat=location[0])
    tz = pytz.timezone(tz_name)
    # Get time at observatory
    now = datetime.now(tz)
    time = Time(now)
    return time

def run_analysis(object,location):
    time = get_time(location)
     # Observation time. Convert to Astropy format
    download_type = 'gif' # Or 'fits'
    RADe_object, in_sky = get_object_icrs(time, location, object) # Or 'sun' if looking in solar system but sky survey cant retrieve solar system image
    if RADe_object is None:
        RA = None
        DE = None
        dest_path = os.path.join('Astro-Website/IMAGES', 'not_found.jpg')
        return RA, DE, dest_path, in_sky
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
        DE = "-{}d {}m {:.2f}s".format(degrees, minutes, seconds)

    if object in SolarSystemBodies:
        dest_path = os.path.join('Astro-Website/IMAGES', object + '.jpg')
        #dest_path = '../IMAGES/' + object + '.jpg'
      
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
        import requests
        response = requests.get(image_url)
        image_file_name = str(object) + '.gif'

        with open(image_file_name, 'wb') as f:
            f.write(response.content)
        import shutil

        # Define the source and destination paths
        src_path = image_file_name
        dest_path = os.path.join('../IMAGES', image_file_name)
        sys_dest_path = os.path.join('Astro-Website/IMAGES', image_file_name)

        # Move the file to the destination directory
        shutil.move(src_path, sys_dest_path)

    return RA, DE, dest_path, in_sky

def generate_obj_list(objects):
    with open(objects,'r') as pop_topics_file:
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

def update_obj_html():  
    # Remove the old object pages and replace them with the templates
    if os.path.exists(obj_1_page):
        os.remove(obj_1_page)
    # Copy the template to the object page
    os.system('copy ' + obj_1_template + ' ' + obj_1_page)
    if os.path.exists(obj_2_page):
        os.remove(obj_2_page) 
    os.system('copy ' + obj_2_template + ' ' + obj_2_page)  
    if os.path.exists(obj_3_page):
        os.remove(obj_3_page)
    os.system('copy ' + obj_3_template + ' ' + obj_3_page)
    # Generate the object list
    object_list = generate_obj_list(final_objects)
    # TODO: Rewrite into functions
    # MODIFYING OBJECT-1-PAGE...
    with open(obj_1_page,'r') as obj1_file:
        new_content = obj1_file.read()
    modified_object_1_page = new_content.replace(OBJ_1,object_list[0].upper())
    with open(obj_1_page,'w') as file:
        file.write(modified_object_1_page)

    # MODIFYING OBJECT-2-PAGE...
    with open(obj_2_page,'r',encoding='utf-8') as obj2_file:
        new_content = obj2_file.read()
    modified_object_2_page = new_content.replace(OBJ_1,object_list[0].upper())
    modified_object_2_page = modified_object_2_page.replace(OBJ_2,object_list[1].upper())
    with open(obj_2_page,'w',encoding='utf-8') as file:
        file.write(modified_object_2_page)

    # MODIFYING OBJECT-3-PAGE...
    with open(obj_3_page,'r',encoding='utf-8') as obj3_file:
        new_content = obj3_file.read()
    modified_object_3_page = new_content.replace(OBJ_1,object_list[0].upper())
    modified_object_3_page = modified_object_3_page.replace(OBJ_3,object_list[2].upper())
    with open(obj_3_page,'w',encoding='utf-8') as file:
        file.write(modified_object_3_page)
        
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
    location = [latitude, longitude]

    # TO UPDATE EACH OF THE OBJECT HTMLS WITH LOCATION INFORMATION #
    for i in range(len(object_list)):
        # TODO: MAKE A COPY OF BELOW STUFF!!!
        file_name = 'Astro-Website/PAGES/object-' + str(i+1) + '-page.html'
        IN_SKY_ref = '[[[IN-SKY-' + str(i+1) + ']]]'
        RA_ref = '[[[RA-' + str(i+1) + ']]]'
        DEC_ref = '[[[DEC-' + str(i+1) + ']]]'
        IMAGE_ref = '[[[IMAGE-' + str(i+1) + ']]]'
        
        RA, DEC, IMAGE_path, in_sky = run_analysis(object_list[i],location)

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