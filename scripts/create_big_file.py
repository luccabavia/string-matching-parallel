#!/usr/bin/env python

from string_matching import load_text
import argparse
import os
import sys

def create_parser():

    parser = argparse.ArgumentParser(usage="create_big_file.py <options>",
                                    description=("Create large sample text "
                                                "files, via replicating the "
                                                "contents of given .txt file")  
    )

    parser.add_argument("-f", 
                        "--file",
                        type=str,
                        help=("Path to file tha will be replicated "
                                "to create a large text"),
                        default=os.path.join(os.path.split(os.path.abspath(__file__))[0], "../sample_txts/kafka.txt")
    )                   

    parser.add_argument("-t",
                        "--times",
                        type=int,
                        help="How many times given file will be replicated",
                        required=True
    )
    return parser       

def create_large_file(input_file, replications):
    """
    Create large .txt sample files via replication of input file.

    Parameters:
    -----------
    input_file: `str`
        Path to input file
    replications: `int`
        How many times input will be replicated
    """
    
    
    file_name, file_extension = os.path.splitext(os.path.split(input_file)[1])
    if not os.path.exists("./sample_txts"):
        os.makedirs("./sample_txts")
    output_file = "{0}_{1}.txt".format(file_name, replications)
    output = os.path.join("./sample_txts", output_file)

    if os.path.exists(output):
        print("File {0} already exists!".format(output))
        return


    with open(os.path.join("./sample_txts", output_file), "w+") as output:
        with open(input_file, "r") as input:
            input_lines = input.readlines()
        
        for i in range(replications):
            output.writelines(input_lines)
    
        print("File {0} created!".format(output))

if __name__ == "__main__":

    parser = create_parser()
    args = parser.parse_args()

    create_large_file(args.file, args.times)


    