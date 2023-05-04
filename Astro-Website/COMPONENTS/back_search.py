import nltk
import os
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
from collections.abc import Mapping
from gensim import summarization

POPULAR_TOPICS = 'Astro-Website/DATA/popular_topics.txt'
LIST_OBJECTS = 'Astro-Website/DATA/list_objects.txt'
HEADLINES = 'Astro-Website/DATA/headlines.txt'
LINKS = 'Astro-Website/DATA/links.txt'
NGC_OBJECTS = 'Astro-Website/DATA/NGC.xlsx'
MESSIER_OBJECTS = 'Astro-Website/DATA/mesr-mas.xls'
DWARF_PLANETS = 'Astro-Website/DATA/dwarf_planets.txt'
MARS_MOONS = 'Astro-Website/DATA/mars_moons.txt'
JUPITER_MOONS = 'Astro-Website/DATA/jupiter_moons.txt'
SATURN_MOONS = 'Astro-Website/DATA/saturn_moons.txt'
URANUS_MOONS = 'Astro-Website/DATA/uranus_moons.txt'
NEPTUNE_MOONS = 'Astro-Website/DATA/neptune_moons.txt'
PLUTO_MOONS = 'Astro-Website/DATA/pluto_moons.txt'
EXOPLANETS = 'Astro-Website/DATA/exoplanets.txt'

 
def read_file(filename):
    '''
    Reads headlines.txt file into list
    input: filename, string
    return: array list of headlines, list
    '''
    # Check if file exists
    if not os.path.exists(filename):
        # If not, create file
        with open(filename, 'w') as f:
            f.write('')
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

def read_file_word(filename):
    '''
    Read .txt file into list
    input: filename, string
    return: list of words, list
    '''
    # Check if file exists
    if not os.path.exists(filename):
        # If not, create file
        with open(filename, 'w') as f:
            f.write('')
    with open(filename, 'r') as f:
        each_line = f.read().split()
        return each_line
   
def read_lines(filename):
    '''
    Read lines from .txt file into list
    input: filename, string
    return: list of links, list
    '''
    # Check if file exists
    if not os.path.exists(filename):
        # If not, create file
        with open(filename, 'w') as f:
            f.write('')
    with open(filename, 'r') as l:
        lines = [line.strip() for line in l]
        return lines

def return_noun(line):
    '''Return nouns from string
    input: line, string
    return: nouns, list
    '''
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(line)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    return nouns


def get_headlines(words, headlines):
    '''
    Gets the headlines that have the top words
    input: words, list
           headlines, list
    return: popular_headlines, list
    '''
    popular_headlines = []
    for word in words:
        for headline in headlines:
            if word in headline.split():
                popular_headlines.append(headline)
            else:
                continue
    return popular_headlines


def get_links(popular_headlines, headlines, links):
    '''
    Find link for given headline and add it to list_links with headline
    input: popular_headlines, list
           headlines, list
           links, list
    return: list_links, list
    '''
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
    '''
    Make list of celestial objects
    input: none
    return: list of celestial objects, list
    '''
    # Read the NGC Excel file into a dataframe
    df1 = pd.read_excel(NGC_OBJECTS, sheet_name='NGC')

    # Read the Messier Excel file into a dataframe
    df2 = pd.read_excel(MESSIER_OBJECTS, sheet_name='Messier Objects', skiprows = 8, nrows=110, usecols=range(2))

    # Create lists for each Messier and NGC objects
    messier1 = df2.iloc[:,0].tolist()
    NGC2 = df2.iloc[:,1].dropna().tolist()
    NGC1 = df1.iloc[:,24].dropna().tolist()

    # Combine two NGC to find missing elements
    NGC_str = list(set(NGC1).union(set(NGC2)))

    # Convert to string plus catalog identifier
    messier = ['M' + str(element) for element in messier1]
    NGC = ['NGC ' + str(element).rstrip('.0') for element in NGC_str]
    d_planets = read_lines(DWARF_PLANETS)
    mars_moons = read_lines(MARS_MOONS)
    jupiter_moons = read_lines(JUPITER_MOONS)
    saturn_moons = read_lines(SATURN_MOONS)
    uranus_moons = read_lines(URANUS_MOONS)
    neptune_moons = read_lines(NEPTUNE_MOONS)
    pluto_moons = read_lines(PLUTO_MOONS)
    exoplanets = read_lines(EXOPLANETS)

    # Create one total list
    total_list = messier+NGC+d_planets+mars_moons+uranus_moons+jupiter_moons+neptune_moons+pluto_moons+saturn_moons+exoplanets
    return total_list

def summarize_artciles(list_links):
    '''
    Summarize articles from list of links
    input: list_links, list
    return: summary_list, list
    '''
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


def object_list(total_list, summary_list):
    '''
    Compare each summary to the list of celestial objects
    input: total_list, list
           summary_list, list
    return: object_ls, list
    '''
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
    words = read_file_word(POPULAR_TOPICS)
    headlines = read_file(HEADLINES)
    links = read_lines(LINKS)
    popular_headlines = get_headlines(words, headlines)
    list_links = get_links(popular_headlines, headlines, links)
    total_list = make_word_lists()
    summary_list = summarize_artciles(list_links)
    object_ls = object_list(total_list, summary_list)
    # Get exact names of objects
    with open(LIST_OBJECTS, 'w') as f:
        for items in reversed(object_ls):
            f.write(items+ '\n')
    f.close
    print('Check "Astro-Website\DATA\list_objects.txt" for exact names of 10 most mentioned objects')

