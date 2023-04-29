# main.py

# import the required modules
import os
import argparse
import website_scrapping
import keyword_processing
import back_search

# define the main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    args = parser.parse_args()
    
    print(os.path.getsize('data/headlines.txt'))
    while os.path.getsize('data/headlines.txt') == 0:
        website_scrapping.run_sites()
    
    keyword_processing.run_keywords()
    back_search.run_back_search()


if __name__ == '__main__':
    main()