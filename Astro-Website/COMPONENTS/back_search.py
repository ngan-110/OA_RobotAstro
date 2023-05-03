import nltk
#nltk.download('punkt')
#nltk.download('averaged_perceptron_tagger')
#%pip install xlrd
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from collections.abc import Mapping
from gensim import summarization



# Reads headlines.txt file into list 
def read_file(filename):
    with open(filename, 'r') as f:
        each_line = f.readlines()
        headlines = []
        for word in each_line:
            if word.isalpha():
                each_line = each_line.replace(word, word.lower())       
        for line in each_line:
            line = line.strip()
            if line:
                headlines.append(line)
        return headlines
    
# Reads populat_topics.txt file and returns list
def read_file_word(filename):
    with open(filename, 'r') as f:
        each_line = f.read().split()
        return each_line

# Read links file into list    
def read_links(filename):
    with open(filename, 'r') as l:
        links = [line.strip() for line in l]
        return links

words = read_file_word('data/popular_topics.txt')
headlines = read_file('data/headlines.txt')
links = read_links('data/links.txt')

# Returns nouns from string
def return_noun(line):
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(line)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    return nouns

# Gets the headlines that have the top words
def get_headlines(words, headlines):
    popular_headlines = []
    for word in words:
        for headline in headlines:
            if word in headline.split():
                popular_headlines.append(headline)
            else:
                continue
    return popular_headlines

# Find link for given headline and add it to list_links with headline
def get_links(popular_headlines, headlines, links):
    list_links = []
    for x in popular_headlines:
        if x in headlines:
            index = headlines.index(x)
            link = links[index]
            list_links.append(link)
        else:
            print("Headline not found.")
    return list_links


def make_word_lists():
    # Read the NGC Excel file into a dataframe
    df1 = pd.read_excel('data/NGC.xlsx', sheet_name='NGC')

    # Read the Messier Excel file into a dataframe
    df2 = pd.read_excel('data/mesr-mas.xls', sheet_name='Messier Objects', skiprows = 8, nrows=110, usecols=range(2))

    # Create lists for each Messier and NGC objects
    messier1 = df2.iloc[:,0].tolist()
    NGC2 = df2.iloc[:,1].dropna().tolist()
    NGC1 = df1.iloc[:,24].dropna().tolist()

    # Combine two NGC to find missing elements
    NGC_str = list(set(NGC1).union(set(NGC2)))

    # Convert to string plus catalog identifier
    messier = ['M' + str(element) for element in messier1]
    NGC = ['NGC ' + str(element).rstrip('.0') for element in NGC_str]
    d_planets = ['Pluto', 'Ceres', 'Makemake', 'Haumea', 'Eris']
    mars_moons = ['Deimos', 'Phobos']
    named_jupiter_moons = ['Adrastea', 'Aitne', 'Amalthea', 'Ananke', 'Aoede', 'Arche', 'Autonoe', 'Callirrhoe', 'Callisto', 'Carme', 
                    'Carpo', 'Chaldene', 'Cyllene', 'Dia', 'Eirene', 'Elara', 'Erinome', 'Ersa', 'Euanthe', 'Eukelade', 'Eupheme', 
                    'Euporie', 'Europa', 'Eurydome', 'Ganymede', 'Harpalyke', 'Hegemone', 'Helike', 'Hermippe', 'Herse', 'Himalia', 
                    'Io', 'Iocaste', 'Isonoe', 'Jupiter LI', 'Jupiter LII', 'Kale', 'Kallichore', 'Kalyke', 'Kore', 'Leda', 'Lysithea', 
                    'Megaclite', 'Metis', 'Mneme', 'Orthosie', 'Pasiphae', 'Pasithee', 'Praxidike', 'Valetudo', 'Sinope', 'Sponde', 
                    'Taygete', 'Thebe', 'Thelxinoe', 'Themisto', 'Thyone']
    named_saturn_moons = ['Aegaeon', 'Aegir', 'Albiorix', 'Anthe', 'Atlas', 'Bebhionn', 'Bergelmir', 'Bestla', 'Calypso', 'Daphnis', 
                    'Dione', 'Enceladus', 'Epimetheus', 'Erriapus', 'Farbauti', 'Fenrir', 'Fornjot', 'Greip', 'Hati', 'Helene', 
                    'Hyperion', 'Hyrrokkin', 'Iapetus', 'Ijiraq', 'Janus', 'Jarnsaxa', 'Kari', 'Kiviuq', 'Loge', 'Methone', 
                    'Mimas', 'Mundilfari', 'Narvi', 'Paaliaq', 'Pallene', 'Pan', 'Pandora', 'Phoebe', 'Polydeuces', 'Prometheus', 
                    'Rhea', 'Siarnaq', 'Skathi', 'Skoll', 'Surtur', 'Suttungr', 'Tarqeq', 'Tarvos', 'Telesto', 'Tethys', 'Thrymyr', 
                    'Titan', 'Ymir']
    named_uranus_names = ['Ariel', 'Belinda', 'Bianca', 'Caliban', 'Cordelia', 'Cressida', 'Cupid', 'Desdemona', 'Ferdinand', 'Francisco', 
                'Juliet', 'Mab', 'Margaret', 'Miranda', 'Oberon', 'Ophelia', 'Perdita', 'Portia', 'Prospero', 'Puck', 'Rosalind', 
                'Setebos', 'Stephano', 'Sycorax', 'Titania', 'Trinculo', 'Umbriel']
    named_neptune_moons = ['Despina', 'Galatea', 'Halimede', 'Hippocamp', 'Laomedeia', 'Larissa', 'Naiad', 'Nereid', 'Neso', 'Proteus', 
                'Psamathe', 'Sao', 'Thalassa', 'Triton']
    named_pluto_moons = ['Charon', 'Hydra', 'Kerberos', 'Nix', 'Styx']
    exoplanet_names = ['Proxima Centauri b', 'TRAPPIST-1d', 'LHS 1140 b', 'Kepler-438b', 'Kepler-442b', 'Kepler-452b', 'Kepler-1229b', 
                    'Kepler-62f', 'Kepler-186f', 'Kepler-452b', 'Kepler-1652b', 'Kepler-442b', 'Kepler-1638b', 'Kepler-438b', 'Kepler-1229b', 
                    'Kepler-1649c', 'Kepler-62f', 'Kepler-186f', 'Kepler-69c', 'Kepler-1649c', 'Kepler-1652b', 'Kepler-1638b', 'Kepler-62e', 
                    'Kepler-438b', 'Kepler-442b', 'Kepler-452b', 'Kepler-1229b', 'Kepler-442b', 'Kepler-1649c', 'Kepler-1638b', 'Kepler-438b', 
                    'Kepler-1652b', 'Kepler-62f', 'Kepler-62e', 'Kepler-186f', 'Kepler-438b', 'Kepler-452b', 'Kepler-442b', 'Kepler-1649c', 
                    'Kepler-62f', 'Kepler-1652b', 'Kepler-1638b', 'Kepler-438b', 'Kepler-62e', 'Kepler-1229b', 'Kepler-186f', 'Kepler-69c', 
                    'Kepler-1649c', 'Kepler-438b', 'Kepler-442b', 'Kepler-1638b', 'Kepler-1652b', 'Kepler-62f', 'Kepler-62e', 'Kepler-186f', 
                    'Kepler-1649c', 'Kepler-1229b', 'Kepler-438b', 'Kepler-69c', 'Kepler-442b', 'Kepler-1638b', 'Kepler-452b', 'Kepler-1652b', 
                    'Kepler-62f', 'Kepler-62e', 'Kepler-186f', 'Kepler-1649c', 'Kepler-438b', 'Kepler-1229b', 'Kepler-1638b', 'Kepler-442b', 
                    'Kepler-1652b', 'Kepler-452b', 'Kepler-1649c', 'Kepler-62f', 'Kepler-186f', 'Kepler-438b', 'Kepler-62e', 'Kepler-69c', 
                    'Kepler-442b', 'Kepler-1229b', 'Kepler-1638b', 'Kepler-1652b', 'Kepler-62f', 'Kepler-1649c', 'Kepler-452b', 'Kepler-438b', 
                    'Kepler-186f', 'Kepler-62e', 'Kepler-442b', 'Kepler-1638b', 'Kepler-1652b', 'Kepler-69c', 'Kepler-1649c', 'Kepler-62f', 
                    'Kepler-438b', 'Kepler-1229b', 'Kepler-186f', 'Kepler-62e', 'Kepler-452b']
    more_exoplanets =  [ 'Proxima Centauri b','TRAPPIST-1b','TRAPPIST-1c','TRAPPIST-1e','TRAPPIST-1f','TRAPPIST-1g','TRAPPIST-1h','Tau Cetie',
                        'Tau Cetif','Ross 128b','LHS 1140b', 'Wolf 1061c','Wolf 1061d','Kepler-1649c','Gliese 667Cc','Gliese 667Cf','Gliese 667Ce',
                        'HD-40307g','Gliese 163c','Gliese 832c','Gliese 667Cb']

    # Create one total list
    total_list = messier+NGC+d_planets+mars_moons+named_uranus_names+named_jupiter_moons+named_neptune_moons+named_pluto_moons+named_saturn_moons+exoplanet_names+more_exoplanets
    return total_list


#Summarizes content from links (1m 10s)
def summarize_artciles(list_links):
    summary_list = []
    # Loop through each link
    for link in list_links:
        
        # Download HTML content of link
        headers ={'User-Agent': 'Chrome/58.0.3029.110 Safari/537.3'}
        response = requests.get(link, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Extract article content
        paragraphs = soup.find_all('p')
        article_text = '\n'.join([p.text for p in paragraphs])

        # Summarize article content
        if (len(summarization.summarize(article_text, ratio=0.4, split=True)))==0:
            summary = summarization.summarize(article_text, ratio=0.4, split=True)
            # Append summary
            summary_list.append(summary)
        else:
            summary = summarization.summarize(article_text, ratio=0.4, split=True)
            # Append summary
            summary_list.append(summary)
    return summary_list


# Compare each summary to the list of Messier objects
def object_list(total_list, summary_list):
    object_ls = []
    for object_name in total_list:
        for summary1 in summary_list:
            for summary in summary1:
                if re.search(r'\b' + object_name + r'\b', summary):
                    if object_name in object_ls:
                        continue
                    else:
                        object_ls.append(object_name)
    return object_ls


# Final function, runs full file
def run_back_search():
    popular_headlines = get_headlines(words, headlines)
    list_links = get_links(popular_headlines, headlines, links)
    total_list = make_word_lists()
    summary_list = summarize_artciles(list_links)
    object_ls = object_list(total_list, summary_list)
    # Print to new file called 'popular topics'
    with open('data/final_objects.txt', 'w') as f:
        for items in reversed(object_ls):
            f.write(items+ '\n')
    f.close
    print('Back search complete!')
    print('Check the file "final_objects.txt" for the results!')

