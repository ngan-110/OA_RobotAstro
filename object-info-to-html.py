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


from object_retrieve import run_analysis

#run_analysis(object_list[0])

RA, DE = run_analysis(object_list[0])
print("RA: ",RA)
print("DEC: ",DE)
