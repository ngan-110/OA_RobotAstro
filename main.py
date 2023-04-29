# main.py

# import the required modules
import os
import argparse
import my_module1
import my_module2

# define the main function
def main():
    # parse command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--input_file', required=True)
    parser.add_argument('--output_dir', required=True)
    args = parser.parse_args()

    # call the functions from the dependent scripts
    my_module1.process_input(args.input_file)
    my_module2.save_output(args.output_dir)

if __name__ == '__main__':
    main()