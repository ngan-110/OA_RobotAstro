with open('/Users/alexandrasavino/Desktop/Astro-Website/TEST-ML-COMPONENTS/popular_topics.txt','r',encoding='utf-8') as pop_topics_file:
    object_list = []
    counter = 0
    for line in pop_topics_file:
        line = line[:-1]
        if counter < 3:
            object_list.append(line)
            counter += 1
        else:
            break
#print(object_list)


# MODIFYING OBJECT-1-PAGE...
with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/object-1-page.html','r',encoding='utf-8') as object_1_page:
    content = object_1_page.read()
modified_object_1_page = content.replace('[[[OBJECT-1]]]',object_list[0])
with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/object-1-page.html','w',encoding='utf-8') as file:
    file.write(modified_object_1_page)


# MODIFYING OBJECT-2-PAGE...
with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/object-2-page.html','r',encoding='utf-8') as object_2_page:
    content = object_2_page.read()
modified_object_2_page = content.replace('[[[OBJECT-1]]]',object_list[0])
modified_object_2_page = modified_object_2_page.replace('[[[OBJECT-2]]]',object_list[1])
with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/object-2-page.html','w',encoding='utf-8') as file:
    file.write(modified_object_2_page)


# MODIFYING OBJECT-3-PAGE...
with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/object-3-page.html','r',encoding='utf-8') as object_3_page:
    content = object_3_page.read()
modified_object_3_page = content.replace('[[[OBJECT-1]]]',object_list[0])
modified_object_3_page = modified_object_3_page.replace('[[[OBJECT-3]]]',object_list[2])
with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/object-3-page.html','w',encoding='utf-8') as file:
    file.write(modified_object_3_page)