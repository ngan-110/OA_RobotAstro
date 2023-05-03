import os
import operator
import numpy as np
import nltk

# Read string from text file and returns all nouns from file
def read_file(filename):
    with open(filename, 'r') as f:
        each_line = f.read()
        if not each_line or each_line == '\n':
            return each_line
        each_line = each_line.strip()
        for word in each_line:
            if word.isalpha():
                each_line = each_line.replace(word, word.lower())       
        return each_line

# Returns nouns from string
def return_noun(line):
    # function to test if something is a noun
    is_noun = lambda pos: pos[:2] == 'NN'
    # do the nlp stuff
    tokenized = nltk.word_tokenize(line)
    nouns = [word for (word, pos) in nltk.pos_tag(tokenized) if is_noun(pos)]
    return nouns

# Returns dict of sorted noun, count and filters out generic words
def popular_topics(filename):
    nouns = return_noun(read_file(filename))
    dict_noun = {}
    word_counts = 0
    top_list = []

    for item in nouns:
        if item in dict_noun:
            word_counts = dict_noun[item] 
            dict_noun[item] = word_counts + 1
        else:
            dict_noun[item] = 1
        word_counts = 0

    # Sort dictionary
    sorted_d = dict(sorted(dict_noun.items(), key=operator.itemgetter(1),reverse=True))
    
    # Add top ten to list
    top_list.append([key for key in sorted_d.items()])

    # Filters out generic keywords 
    # List of common generic keywords and organization names
    generic_keywords = ['A', 'world', 'scientist', 'scientists', 'sky', 'space', 'science', 'bookshelf', 'nature', 'ideas', 'doesn', 't', 'bodies', 'telescope', 'today']
    names = ['fish','turing','james', 'webb', 's', '’', 'time', 'day', 'earth','astronomers','reveals', 'thanks', 'secrets', 'call' ]
    org_names = ['NASA', 'nasa']

    # Create a new list of words that do not match any generic keywords, website or org names
    filtered_list = [(word, num) for word, num in top_list[0] if word not in generic_keywords + names + org_names]
    
    return filtered_list[:10]

# Print to new file called 'popular topics'
def run_keywords():
    with open('data/popular_topics.txt', 'w') as f:
        t = popular_topics('data/headlines.txt')
        for items in t:
            f.write(items[0]+ '\n')
    f.close
    print('Done running keyword processing...')
    print('Popular topics saved to data/popular_topics.txt')

