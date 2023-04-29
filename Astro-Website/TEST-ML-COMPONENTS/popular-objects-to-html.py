popular_topics = 'data/popular_topics.txt'
obj_1_page = 'Astro-Website/PAGES/object-1-page.html'
obj_2_page = 'Astro-Website/PAGES/object-2-page.html'
obj_3_page = 'Astro-Website/PAGES/object-3-page.html'
OBJ_1 = '[[[OBJECT-1]]]'
OBJ_2 = '[[[OBJECT-2]]]'
OBJ_3 = '[[[OBJECT-3]]]'

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
with open(obj_1_page,'r',encoding='utf-8') as object_1_page:
    content = object_1_page.read()
modified_object_1_page = content.replace(OBJ_1,object_list[0])
with open(obj_1_page,'w',encoding='utf-8') as file:
    file.write(modified_object_1_page)


# MODIFYING OBJECT-2-PAGE...
with open(obj_2_page,'r',encoding='utf-8') as object_2_page:
    content = object_2_page.read()
modified_object_2_page = content.replace(OBJ_1,object_list[0])
modified_object_2_page = modified_object_2_page.replace(OBJ_2,object_list[1])
with open(obj_2_page,'w',encoding='utf-8') as file:
    file.write(modified_object_2_page)


# MODIFYING OBJECT-3-PAGE...
with open(obj_3_page,'r',encoding='utf-8') as object_3_page:
    content = object_3_page.read()
modified_object_3_page = content.replace(OBJ_1,object_list[0])
modified_object_3_page = modified_object_3_page.replace(OBJ_3,object_list[2])
with open(obj_3_page,'w',encoding='utf-8') as file:
    file.write(modified_object_3_page)



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