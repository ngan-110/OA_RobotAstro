popular_topics = 'data/popular_topics.txt'
obj_1_template = 'Astro-Website/PAGES/template/object-1-page.html'
obj_2_template = 'Astro-Website/PAGES/template/object-2-page.html'
obj_3_template = 'Astro-Website/PAGES/template/object-3-page.html'
obj_1_page = 'Astro-Website/PAGES/object-1-page.html'
obj_2_page = 'Astro-Website/PAGES/object-2-page.html'
obj_3_page = 'Astro-Website/PAGES/object-3-page.html'
OBJ_1 = '[[[OBJECT-1]]]'
OBJ_2 = '[[[OBJECT-2]]]'
OBJ_3 = '[[[OBJECT-3]]]'

import os

# Remove the old object pages and replace them with the templates
if os.path.exists(obj_1_page):
    os.remove(obj_1_page)
    os.system('cp ' + obj_1_template + ' ' + obj_1_page)
if os.path.exists(obj_2_page):
    os.remove(obj_2_page) 
    os.system('cp ' + obj_2_template + ' ' + obj_2_page)  
if os.path.exists(obj_3_page):
    os.remove(obj_3_page)
    os.system('cp ' + obj_3_template + ' ' + obj_3_page)

def generate_obj_list(popular_topics):
    with open(popular_topics,'r',encoding='utf-8') as pop_topics_file:
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

object_list = generate_obj_list(popular_topics)


# TODO: Rewrite into functions
# MODIFYING OBJECT-1-PAGE...
with open(obj_1_page,'r',encoding='utf-8') as obj1_file:
    new_content = obj1_file.read()
modified_object_1_page = new_content.replace(OBJ_1,object_list[0].upper())
with open(obj_1_page,'w',encoding='utf-8') as file:
    file.write(modified_object_1_page)


# MODIFYING OBJECT-2-PAGE...
with open(obj_2_page,'r',encoding='utf-8') as obj2_file:
    new_content = obj2_file.read()
modified_object_2_page = new_content.replace(OBJ_1,object_list[0])
modified_object_2_page = modified_object_2_page.replace(OBJ_2,object_list[1].upper())
with open(obj_2_page,'w',encoding='utf-8') as file:
    file.write(modified_object_2_page)


# MODIFYING OBJECT-3-PAGE...
with open(obj_3_page,'r',encoding='utf-8') as obj3_file:
    new_content = obj3_file.read()
modified_object_3_page = new_content.replace(OBJ_1,object_list[0])
modified_object_3_page = modified_object_3_page.replace(OBJ_3,object_list[2].upper())
with open(obj_3_page,'w',encoding='utf-8') as file:
    file.write(modified_object_3_page)


#&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&
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

object_list = ['M3','M83','mars']


# TO UPDATE EACH OF THE OBJECT HTMLS WITH LOCATION INFORMATION #

from object_retrieve import run_analysis

for i in range(len(object_list)):
    # TODO: MAKE A COPY OF BELOW STUFF!!!
    file_name = 'Astro-Website/PAGES/object-' + str(i+1) + '-page.html'
    IN_SKY_ref = '[[[IN-SKY-' + str(i+1) + ']]]'
    RA_ref = '[[[RA-' + str(i+1) + ']]]'
    DEC_ref = '[[[DEC-' + str(i+1) + ']]]'
    IMAGE_ref = '[[[IMAGE-' + str(i+1) + ']]]'
    
    RA, DEC, IMAGE_path, in_sky = run_analysis(object_list[i],location)
    #DEC = str(DEC)

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






'''
def modify_obj_page(obj_page, OBJ, object_list):
    with open(obj_page,'r',encoding='utf-8') as obj_page:
        content = obj_page.read()
    modified_obj = content.replace(OBJ,object_list[0])
    if OBJ == OBJ_2:
        modified_obj = modified_obj.replace(OBJ, object_list[1])
    if OBJ == OBJ_3:
        modified_obj = modified_obj.replace(OBJ, object_list[2])
    file_content = modified_obj.read()
    file_str = str(file_content)
    with open(obj_page,'w',encoding='utf-8') as file:
        file.write(file_str)


modify_obj_page(obj_1_page, OBJ_1, object_list)
modify_obj_page(obj_2_page, OBJ_2, object_list)
modify_obj_page(obj_3_page, OBJ_3, object_list)'''