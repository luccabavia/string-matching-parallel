#!/usr/bin/env python

import sys
import time
from string_matching import StringMatching as sm
from string_matching import load_text, compare_results
from string_matching import ParallelPreprocessing as pp
from string_matching import ParallelStringMatching as psm
import multiprocessing as mp
    
if __name__ == "__main__":
    
    sequentialSM = sm()
    parallelSM = psm()
    processor_count = mp.cpu_count()

    pattern = "people"   
    lps = sequentialSM.build_lps(pattern)

    processor_count = mp.cpu_count()

    start = time.time()
    text = load_text("../very_large.txt")
    sliced_text, segments = pp.get_text_segments(text, processor_count)
    print("Len sliced text: ", len(sliced_text))
    print("Len segments:    ", len(segments))

    for i in sliced_text:
        print("Length: ", len(i))
    print("Len :", len(text))

    print("Last index text: ", segments[-1][0] + (len(sliced_text[-1]) -1))
    print("Last index seg:  ", segments[-1][1])
    end = time.time()
    
    print("File loaded and sliced! Time elapsed: {}".format(end - start))

    i = 0
    for x, y in zip(sliced_text, segments):
        try:
            i += 1
        except Exception as e:
            raise e
    # sys.exit()
     
    pool = mp.Pool(processor_count)
    for i  in range(1): 

        start = time.time()
        resultsSynced = pool.starmap(
                                sequentialSM.naive_algorithm, 
                                [(pattern, x) for x in sliced_text]
        )
        end = time.time()
        print("Naive parallel synced elapsed: ", end - start)                        
    pool.close()
    print("RESULTS: ")
    synced = list()
    for i in resultsSynced:
        synced = synced + i
    print(len(synced))
    print("")

    with mp.Pool(processor_count) as pool:
        for i  in range(1): 

            start = time.time()
            resultsSynced = pool.starmap(
                                    parallelSM.naive_algorithm, 
                                    [(pattern, x, y) 
                                    for x, y in zip(sliced_text, segments)]
            )
            end = time.time()
            print("Naive parallel synced elapsed: ", end - start)                        
    # pool.close()
    print("RESULTS: ")
    synced = list()
    for i in resultsSynced:
        synced = synced + i
    print(len(synced))
    print("")


    # pool = mp.Pool(processor_count)
    # for i in range(1):
    #     start = time.time()
    #     resultsAsync = pool.starmap_async(
    #                             sm.naive_algorithm, 
    #                             [(pattern, x) for x in sliced_text],
    #                             callback=None
    #     )
    #     end = time.time()
    #     print("Naive parallel async elapsed:  ", end - start)
    # pool.close()
    # print("RESULTS: ")
    # asynced = list()
    # for i in resultsAsync.get():
    #     asynced = asynced + i
    # print(len(asynced))
    # print("")

    for i in range(1):
        start = time.time()
        resultsNaive = sequentialSM.naive_algorithm(pattern, text)    
        end = time.time()
        print("Naive elapsed:                 ", end - start)
    print("RESULTS: ")
    print(len(resultsNaive))

    
    compare_results(sorted(resultsNaive), sorted(synced))

    dif_index = []
    for i in range(len(synced)):
        if synced[i] != resultsNaive[i]:
            dif_index.append(i)