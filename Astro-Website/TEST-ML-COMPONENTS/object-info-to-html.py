# TO MAKE THE OBJECT_LIST #
'''
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
#object_name = object_list[0]
'''

object_list = ['M3','M87','M91']


# TO UPDATE EACH OF THE OBJECT HTMLS WITH LOCATION INFORMATION #
from object_retrieve import run_analysis

for i in range(len(object_list)):
    # TODO: MAKE A COPY OF BELOW STUFF!!!
    file_name = 'Astro-Website/PAGES/object-' + str(i+1) + '-page.html'
    RA_ref = '[[[RA-' + str(i+1) + ']]]'
    DEC_ref = '[[[DEC-' + str(i+1) + ']]]'
    IMAGE_ref = '[[[IMAGE-' + str(i+1) + ']]]'
    
    RA, DEC, IMAGE_path = run_analysis(object_list[i])

    # Updating object htmls with location information + images #
    with open(file_name,'r',encoding='utf-8') as file:
        content = file.read()
    modified_file = content.replace(RA_ref,RA)
    modified_file = modified_file.replace(DEC_ref,DEC)

    modified_file = modified_file.replace(IMAGE_ref,IMAGE_path)

    with open(file_name,'w',encoding='utf-8') as file:
        file.write(modified_file)


    