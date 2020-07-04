#!/usr/bin/env python

import sys
import time
import os
from string_matching import StringMatching as sm
from string_matching import load_text, compare_results
from string_matching import ParallelPreprocessing as pp
from string_matching import ParallelStringMatching as psm
import multiprocessing as mp
from create_big_file import create_large_file

def get_core_increment(max_core_count):
    """
    Create list with core counts used in scaling test (values are power of 2).

    Parameters:
    -----------
    max_core_count: `int`
        Max core count used
    """
    
    i = 0
    core_count = []
    while True:
        if 2**i < max_core_count:
            core_count.append(2**i)
        else:
            core_count.append(max_core_count)
            break
        i += 1
    
    print("Core counts used in test -> {}".format(core_count))
    return core_count
    
def log_data(file, result):
    """
    Log results from tests.

    Parameters:
    -----------
    file: `str`
        Path to file used for logging
    result:
        Data entry to be saved.
    """

    with open(file, "a+") as f:
        f.write("\n")
        for i in result:
            f.write(str(i)+"\n")

def execute_algorithm(pattern, text, log_file,
            max_cores=mp.cpu_count(), naive=True, repeat=10):
    """
    Execute algorithm repeatedly, to test scaling.

    Parameters:
    -----------
    pattern: `str`
        Pattern to look for in text
    text: `text`
        Text used as haystack
    log_file: `str`
        Path to file used for logging data
    max_cores: `int`
        Max core count used for tests
    naive: `bool`
        Execute with Naive algorithm
    repeat: `int`
        Number of iterations used for test
    """
    
    sequentialSM = sm()
    parallelSM = psm()
    
    core_count_list = get_core_increment(max_cores)
    result_data = []
        
    if naive:
        print("Using Naive search algorithm!")
        for cores in core_count_list:
            print("Starting tests with {} core(s)".format(cores))
            sliced_text, segments = pp.get_text_segments(text, cores)

            with mp.Pool(cores) as pool:
                for iteration in range(repeat): 
                    start = time.time()
                    results_pool = pool.starmap_async(
                        parallelSM.naive_algorithm, 
                        [(pattern, x, y) for x, y in zip(sliced_text, segments)]
                    )
                    end = time.time()

                    results = list()
                    for i in results_pool.get():
                        results = results + i
                    result_data.append((cores, end - start, len(results)))
                    print("        Naive parallel elapsed: ", end - start)
                time.sleep(1)
        log_data(log_file, result_data)

    else:
        print("Using KMP search algorithm!")
        lps = sequentialSM.build_lps(pattern)
        core_count_list=[4]
        for cores in core_count_list:
            print("Starting tests with {} core(s)".format(cores))
            sliced_text, segments = pp.get_text_segments(text, cores)

            with mp.Pool(cores) as pool:
                for iteration in range(repeat):
                    print("    Iteration {}".format(iteration)) 
                    start = time.time()
                    results_pool = pool.starmap_async(
                        parallelSM.kmp_algorithm, 
                        [(pattern, x, y, lps) for x, y in zip(sliced_text, segments)]
                    )
                    results_pool = results_pool.get()
                    end = time.time()

                    results = list()
                    for i in results_pool:
                        results = results + i
                    result_data.append((cores, end - start, len(results)))
                    print("        KMP parallel elapsed: ", end - start)
                time.sleep(1)
        log_data(log_file, result_data)

def main():
    """
    Test used for scaling analisys data collection.
    """

    for i in range(250, 2001, 250):
        create_large_file("sample_txts/kafka.txt", i)
    
    # Incremets the file size in aproximately 200MB
    base_path = "sample_txts/"
    files = ["kafka_250.txt", 
                "kafka_500.txt", 
                "kafka_750.txt", 
                "kafka_1000.txt",
                "kafka_1250.txt",
                "kafka_1500.txt",
                "kafka_1750.txt",
                "kafka_2000.txt"
    ]
    log_output_file = "results_log.txt"
    log_data(log_output_file, "RESULTS LOG FILE")

    pat = "people"
    for i in files:
        print("Searching in {} file!".format(i))
        current_text = os.path.join(base_path, i)
        loaded_text = load_text(current_text)
        execute_algorithm(pat, loaded_text, log_output_file, naive=False)
        del loaded_text
        time.sleep(1)

if __name__ == "__main__":

    ## This script must be executed from project source 
    ## (string-matching-parallel directory)

    ## Use python3 scripts/scale_execution.py
    main()

        
 
