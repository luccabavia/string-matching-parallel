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
# import pandas as pd

def get_core_increment(max_core_count):
    
    i = 0
    core_count = []
    while True:
        if 2**i < max_core_count:
            core_count.append(2**i)
        else:
            core_count.append(max_core_count)
            break
        i += 1
    
    print(core_count)
    return core_count
    
def log_data(file, result):

    with open(file, "a+") as f:
        f.write("\n")
        f.write(result)

def execute_algorithm(pattern, text, log_file,
            max_cores=mp.cpu_count(), naive=True, exec_async=False, repeat=10):
    print(len(text))
    sequentialSM = sm()
    parallelSM = psm()
    
    core_count_list = get_core_increment(max_cores)
    result_data = []

    if exec_async:
        if naive:
            
            for cores in core_count_list:
                print(f"\nStarting tests with {cores} cores")
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
                        # print("Naive parallel synced elapsed: ", end - start)
                    time.sleep(1)
            print(result_data)
            log_data(log_file, result_data)

        else:
            lps = sequentialSM.build_lps(pattern)

            for cores in core_count_list:
                print(f"Starting tests with {cores} core(s)")
                sliced_text, segments = pp.get_text_segments(text, cores)

                with mp.Pool(cores) as pool:
                    for iteration in range(repeat):
                        print(f"    Iteration {iteration}") 
                        start = time.time()
                        results_pool = pool.starmap_async(
                            parallelSM.kmp_algorithm, 
                            [(pattern, x, y) for x, y in zip(sliced_text, segments)]
                        )
                        end = time.time()

                        results = list()
                        for i in results_pool.get():
                            results = results + i
                        result_data.append((cores, end - start, len(results)))
                        # print("Naive parallel synced elapsed: ", end - start)
                    time.sleep(1)
            print(result_data)
            log_data(log_file, result_data)
    else:
        if naive:
            
            for cores in core_count_list:
                print(f"\nStarting tests with {cores} cores")
                sliced_text, segments = pp.get_text_segments(text, cores)

                with mp.Pool(cores) as pool:
                    for iteration in range(repeat): 
                        start = time.time()
                        results_pool = pool.starmap(
                            parallelSM.naive_algorithm, 
                            [(pattern, x, y) for x, y in zip(sliced_text, segments)]
                        )
                        end = time.time()

                        results = list()
                        for i in results_pool:
                            results = results + i
                        result_data.append((cores, end - start, len(results)))
                        # print("Naive parallel synced elapsed: ", end - start)
                    time.sleep(1)
            print(result_data)
            log_data(log_file, result_data)

        else:
            lps = sequentialSM.build_lps(pattern)

            for cores in core_count_list:
                print(f"Starting tests with {cores} core(s)")
                sliced_text, segments = pp.get_text_segments(text, cores)

                with mp.Pool(cores) as pool:
                    for iteration in range(repeat):
                        print(f"    Iteration {iteration}") 
                        start = time.time()
                        results_pool = pool.starmap(
                            parallelSM.kmp_algorithm, 
                            [(pattern, x, y) for x, y in zip(sliced_text, segments)]
                        )
                        end = time.time()

                        results = list()
                        for i in results_pool:
                            results = results + i
                        result_data.append((cores, end - start, len(results)))
                        # print("Naive parallel synced elapsed: ", end - start)
                    time.sleep(1)
            print(result_data)
            log_data(log_file, result_data)

if __name__ == "__main__":

    for i in range(250, 2001, 250):
        #print(f"Creating file with {i} times the size of base sample text!")
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
    # print(get_core_increment(4))
    log_output_file = "results_log.txt"
    log_data(log_output_file, "RESULTS LOG FILE")

    pat = "people"
    for i in files:
        print(f"Searching in {i} file!")
        current_text = os.path.join(base_path, i)
        loaded_text = load_text(current_text)
        execute_algorithm(pat, loaded_text, log_output_file, naive=False)
        del loaded_text
        time.sleep(2)

        
 
