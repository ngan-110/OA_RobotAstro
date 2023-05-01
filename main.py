# main.py

# import the required modules
import os
import sys
import argparse
sys.path.append('/Users/rhessa/OA_RobotAstro/Astro-Website')
from COMPONENTS import website_scrapping
from COMPONENTS import keyword_processing
#from COMPONENTS import back_search


# define the main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    print(os.path.getsize('data/headlines.txt'))
    while os.path.getsize('data/headlines.txt') == 0:
        website_scrapping.run_sites()
    
    keyword_processing.run_keywords()


if __name__ == '__main__':
    main()