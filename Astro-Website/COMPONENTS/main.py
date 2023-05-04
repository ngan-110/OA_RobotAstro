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
import webbrowser


# define the main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    print('RUNNING WEBSITE SCRAPPING...')
    website_scrapping.run_sites()
    
    print('RUNNING KEYWORD PROCESSING...')
    keyword_processing.run_keywords()
    
    print('RUNNING BACK SEARCH...')
    back_search.run_back_search()
    
    print('POPULATE OBJECTS TO HTML...')
    popular_objects_to_html.update_obj_html()
    
    print('POPULATE HEADLINES HTML...')
    headline_to_html.update_headline_html()

    print('OPENING WEBSITE...')
    website = 'Astro-Website/PAGES/object-1-page.html'
    webbrowser.get('chrome').open(website)

if __name__ == '__main__':
    main()