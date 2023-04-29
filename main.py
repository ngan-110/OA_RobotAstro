# main.py

# import the required modules
import os
import argparse
from website_scrapping import run_sites
from keyword_processing import run_keywords
from back_search import run_back_search

# define the main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--output_dir', required=True)
    args = parser.parse_args()

    run_sites()
    run_keywords()
    run_back_search()
    
    # call the functions from the dependent scripts
    #my_module1.process_input(args.input_file)
    #my_module2.save_output(args.output_dir)

if __name__ == '__main__':
    main()