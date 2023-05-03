# main.py

# import the required modules
import os
import sys
import argparse
sys.path.append('/Users/rhessa/OA_RobotAstro/Astro-Website')
from COMPONENTS import website_scrapping
from COMPONENTS import keyword_processing
from COMPONENTS import back_search
from COMPONENTS import popular_objects_to_html
from COMPONENTS import headline_to_html
#from COMPONENTS import back_search


# define the main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    print('Running website scrapping...')
    print(os.path.getsize('data/headlines.txt'))
    while os.path.getsize('data/headlines.txt') == 0:
        website_scrapping.run_sites()
    
    print('Running keyword processing...')
    keyword_processing.run_keywords()
    
    print('Running back search...')
    back_search.run_back_search()
    
    print('Populate objects and images to html...')
    popular_objects_to_html.update_obj_html()
    
    print('Populate headlines to html...')
    headline_to_html.update_headline_html()

if __name__ == '__main__':
    main()