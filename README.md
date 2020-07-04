## Parallel String Matching

#### Description

Parallel string matching implementation with Python, utilizing the multiprocessing module.

### Requirements

- Python version 3.7 or greater (developed on Python 3.8 and tested on 3.8 and 3.7)

#### How to use

1. Use the script _create_big_file.py_ to create the desired file for testing. You may provide a sample text (.txt file) and how many times the sample text will be repeated.
```bash
Create large sample text files, via replicating the contents of given .txt file

optional arguments:
  -h, --help            show this help message and exit
  -f FILE, --file FILE  Path to file tha will be replicated to create a large text
  -t TIMES, --times TIMES
                        How many times given file will be replicated
```                        

2. Use the script _string_match.py_ to search for a given pattern (string), in a given text.

```bash
Search for a pattern inside of a text. The given pattern is limited to a full word, no strings with spaces are allowed (such as 'Darth Vader'); separation between lower and upper case is also not
supported.

optional arguments:
  -h, --help            show this help message and exit
  -p PATTERN, --pattern PATTERN
                        Pattern to be searched for in input text
  -t TEXT, --text TEXT  Absolute path to text where search will occur
  -a {naive,kmp}, --algorithm {naive,kmp}
                        Algorithm used for string search
  --parallel
  --processor_count PROCESSOR_COUNT
                        Number of processors used in parallel execution
```
3. Use the script _scale_execution.py_ to test the execution on our system, it will create large files based on _kafka.txt_ and will iterate over the files and a range of processor cores to use, until it reaches the max core count of your machines processor. (Execute from project root, as it will search for _sample_txt_ directory and try to create multiple files - from aproximately 200MB to 1GB)

#### References used

* Algorithms adapted from GeeksForGeeks website: [Naive algorithm], [Knuth-Morris-Pratt algorithm]
* Python's multiprocessing references: [Multiprocessing module documentation], [Parallel Processing in Python]

[Naive algorithm]: https://www.geeksforgeeks.org/naive-algorithm-for-pattern-searching/
[Knuth-Morris-Pratt algorithm]: https://www.geeksforgeeks.org/kmp-algorithm-for-pattern-searching/
[Multiprocessing module documentation]: https://docs.python.org/3/library/multiprocessing.html
[Parallel Processing in Python]: https://www.machinelearningplus.com/python/parallel-processing-python/
