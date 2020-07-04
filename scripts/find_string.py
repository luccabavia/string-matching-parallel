#!/usr/bin/env python

import sys
import time
import argparse
from string_matching import StringMatching as sm
from string_matching import load_text, compare_results
from string_matching import ParallelPreprocessing as pp
from string_matching import ParallelStringMatching as psm
import multiprocessing as mp

def create_parser():
    
    parser = argparse.ArgumentParser(
        usage="python3 find_string.py <options>",
        description=("Search for a pattern inside of a text. "
                    "The given pattern is limited to a full word, "
                    "no strings with spaces are allowed "
                    "(such as 'Darth Vader'); separation between "
                    "lower and upper case is also not supported.")
                   
    )

    parser.add_argument("-p", "--pattern",
                        type=str,
                        help="Pattern to be searched for in input text",
                        required=True
    )       

    parser.add_argument("-t", "--text",
                        type=str,
                        help="Absolute path to text where search will occur",
                        required=True
    )

    parser.add_argument("-a", "--algorithm",
                        choices=("naive", "kmp"),
                        default="kmp",
                        help="Algorithm used for string search"
    )              

    parser.add_argument("--parallel",
                        action="store_true")
    #                     choices=("sequential", "parallel"),
    #                     default="parallel",
    #                     help="Execution mode"
    # )
    parser.add_argument("--processor_count",
                        type=int,
                        help="Number of processors used in parallel execution",
                        default=2
    )                   

    return parser

def main(input_path, pattern, processor_count=2, 
                                            algorithm="kmp", parallel=True):
    """
    Search for pattern in input text.

    Parameters:
    -----------
    input_path: `str`
        Absolute path to text
    pattern: `str`
        Pattern to look for in text
    processor_count: `int`
        Number of processors used in parallel execution
    algorithm: `str`
        Choose between 'naive' and 'kmp' algorithms
    parallel: `bool`
        Execute search with parallel processes
    """

    if parallel:    
        search_parallel(input_path, pattern, processor_count, algorithm)
    else:
        search_sequential(input_path, pattern, algorithm)    
    
def search_sequential(input_path, pattern, algorithm="kmp"):
    """
    Search for pattern in input text, sequentially.

    Parameters:
    -----------
    input_path: `str`
        Absolute path to text
    pattern: `str`
        Pattern to look for in text
    algorithm: `str`
        Choose between 'naive' and 'kmp' algorithms
    """

    sequentialSM = sm()

    start = time.time()
    text = load_text(input_path)
    end = time.time()
    print("File loaded! Time elapsed: {}".format(end - start))

    if algorithm == "naive":
        print("Naive sequential selected!")
        start = time.time()
        results = sequentialSM.naive_algorithm(pattern, text)    
        end = time.time()
        print("Naive -> time elapsed: ", end - start)
        print("Matches found: ", len(results))
    else:
        print("KMP sequential selected!")
        lps = sequentialSM.build_lps(pattern)
        start = time.time()
        results = sequentialSM.kmp_algorithm(pattern, text, lps)    
        end = time.time()
        print("KMP -> time elapsed: ", end - start)
        print("Matches found: ", len(results))

def search_parallel(input_path, pattern, processor_count, algorithm="kmp"):
    """
    Search for pattern in input text, using parallel processes.

    Parameters:
    -----------
    input_path: `str`
        Absolute path to text
    pattern: `str`
        Pattern to look for in text
    processor_count: `int`
        Number of processors used
    algorithm: `str`
        Choose between 'naive' and 'kmp' algorithms
    """

    sequentialSM = sm()
    parallelSM = psm()

    start = time.time()
    text = load_text(input_path)
    sliced_text, segments = pp.get_text_segments(text, processor_count)
    end = time.time()
    print("File loaded and sliced! Time elapsed: {}".format(end - start))

    if algorithm == "naive":
        print(
            "Naive parallel with {} core(s) selected!".format(processor_count)
        )
        with mp.Pool(processor_count) as pool:
            start = time.time()
            results = pool.starmap_async(
                                    parallelSM.naive_algorithm, 
                                    [(pattern, x, y) 
                                    for x, y in zip(sliced_text, segments)]
            )
            end = time.time()
            results = results.get()
        print("Naive parallel -> time elapsed: ", end - start)                        
        
    else:
        print("KMP parallel with {} core(s) selected!".format(processor_count))
        lps = sequentialSM.build_lps(pattern)
        with mp.Pool(processor_count) as pool:
            start = time.time()
            results = pool.starmap_async(
                                    parallelSM.kmp_algorithm, 
                                    [(pattern, x, y, lps) 
                                    for x, y in zip(sliced_text, segments)]
            )
            end = time.time()
            results = results.get()
        print("KMP parallel -> time elapsed: ", end - start)   
    

    final_results = list()
    for i in results:
        final_results = final_results + i
    print("Matches found: ", len(final_results))


if __name__ == "__main__":

    parser = create_parser()
    args = parser.parse_args()
    main(  
        args.text, 
        args.pattern, 
        args.processor_count, 
        args.algorithm, 
        args.parallel
    )
