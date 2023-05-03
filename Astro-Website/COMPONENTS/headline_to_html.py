# THIS READS FROM HEADLINES.TXT TO SUB IN [[[OBJECT-1,2,3]]] IN EACH HTML FILE #
link_txt = 'Astro-Website/DATA/links.txt'
headline_txt = 'Astro-Website/DATA//headlines.txt'
ref_site_page = 'Astro-Website/PAGES/ref-site-page.html'

def update_headline_html():
    with open(link_txt,'r',encoding='utf-8') as link_file:
        link_list = []
        for line in link_file:
            link_list.append(line)


    with open(headline_txt,'r',encoding='utf-8') as headline_file:
        headline_list = []
        for line in headline_file:
            line = ' '.join(word.capitalize() for word in line.split())
            headline_list.append(line)


    list_html = ""
    for bullet_index in range(len(link_list)):
        list_item = '<li><i>"' +  headline_list[bullet_index].strip() \
            + '"</i>-<a href="' + link_list[bullet_index] + '" style="color: #02ff02;">' \
            + link_list[bullet_index] + '</a></li>'

        list_html += list_item
    with open(ref_site_page,'r',encoding='utf-8') as ref_page:
        html_content = ref_page.read()

    modified_html_content = html_content.replace("[[[LIST]]]", list_html)
    # THIS HAS TO BE RESET EVERYDAY TO [[[LIST]]] SO THAT THE FILE CAN BE UPDATED!!! 

    with open(ref_site_page,'w',encoding='utf-8') as file:
        file.write(modified_html_content)
    print('Headlines updated.')

    