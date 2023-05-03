# main.py

# import the required modules
import os
import argparse

# import the components
import website_scrapping
import keyword_processing
import back_search
import popular_objects_to_html
import headline_to_html


# define the main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    print('Running website scrapping...')
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