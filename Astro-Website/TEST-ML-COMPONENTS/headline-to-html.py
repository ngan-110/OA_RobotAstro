# THIS CODE ASSUMES THAT EACH HEADLINE IS ONE LINE!!!
#    MIGHT HAVE TO CHANGE TO INCLUDE LINKS?


with open('/Users/alexandrasavino/Desktop/Astro-Website/TEST-ML-COMPONENTS/links.txt','r',encoding='utf-8') as link_file:
    link_list = []
    for line in link_file:
        link_list.append(line)
    #print(link_list)

with open('/Users/alexandrasavino/Desktop/Astro-Website/TEST-ML-COMPONENTS/headlines.txt','r',encoding='utf-8') as headline_file:
    headline_list = []
    for line in headline_file:
        line = ' '.join(word.capitalize() for word in line.split())
        headline_list.append(line)

#print(len(link_list))
#print(len(headline_list))

list_html = ""
for bullet_index in range(len(link_list)):
    ####  <a href="https://www.example.com">This is a link</a>  ####
    list_item = '<li><i>"' +  headline_list[bullet_index].strip() \
        + '"</i>-<a href="' + link_list[bullet_index] + '" style="color: #02ff02;">' \
        + link_list[bullet_index] + '</a></li>'
    ''' #with original underline - guess underlines are inherent to links?
    list_item = '<li><i>"' +  headline_list[bullet_index].strip() \
        + '"</i>-<u><a href="' + link_list[bullet_index] + '" style="color: #02ff02;">' \
        + link_list[bullet_index] + '</a></u></li>'
    '''
    list_html += list_item
with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/ref-site-page.html','w',encoding='utf-8') as ref_page:
#with open('/Users/alexandrasavino/Desktop/Astro Website/PAGES/UR-MOM-TESTING.html','r',encoding='utf-8') as ref_page:
    html_content = ref_page.read()

modified_html_content = html_content.replace("[[[LIST]]]", list_html)
# THIS HAS TO BE RESET EVERYDAY TO [[[LIST]]] SO THAT THE FILE CAN BE UPDATED!!! 

with open('/Users/alexandrasavino/Desktop/Astro-Website/PAGES/ref-site-page.html','w',encoding='utf-8') as file:
#with open('/Users/alexandrasavino/Desktop/Astro Website/PAGES/UR-MOM-TESTING.html','w',encoding='utf-8') as file:
    file.write(modified_html_content)