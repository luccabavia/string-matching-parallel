#!/usr/bin/env python

def load_text(path, lowercase=True):
    """
    Load text file data.

    Parameters:
    -----------
    path: `str`
        Path to input text.
    lowercase: `bool`
        Convert read text to lowercase.
    """

    with open(path, "r") as file:
        text = file.readlines()

    char_array = list()
    if lowercase:
        for i in text:
            char_array.append(i.lower())
    else:
        for i in text:
            char_array.append(i)
    
    return "".join(char_array)

def compare_results(list_a, list_b):
    """
    Compare two lists.

    Parameters:
    -----------
    list_a: `list``
        First list.
    list_b: `list`
        Second list
    """

    if (len(list_a)== len(list_b) and 
        len(list_a) == sum(
                        [1 for i, j in zip(list_a, list_b) if i == j])
    ): 
        print ("Lists are dentical") 
    else : 
        print ("Lists are not identical") 

class StringMatching():
    """
    String matching algorithms.
    """

    def naive_algorithm(self, pattern, text):
        """
        Naive algorithm for string searching.

        Parameters:
        -----------
        pattern: `str`
            Pattern to search for.
        text: `str`
            Text to search in.

        Returns:
        --------
        matches: `int`
            List of indices where mathces where found.
        """
        
        M = len(pattern) 
        N = len(text)
        matches = list() 

        for i in range(N - M + 1): 
        
            j = 0

            while(j < M): 
                if (text[i + j] != pattern[j]): 
                    break
                j += 1

            if (j == M): 
                matches.append(i)
        return matches

    def kmp_algorithm(self, pattern, text, lps):
        """
        Knuth-Morris-Pratt string matching algorithm.

        Parameters:
        -----------
        pattern: `str`
            Pattern to search for.
        text: `str`
            Text to search in.

        Returns:
        --------
        matches: `int`
            List of indices where mathces where found.
        """
            
        M = len(pattern) 
        N = len(text) 
    
        j = 0 
            
        matches = list()
        i = 0 
        while i < N: 
            if pattern[j] == text[i]: 
                i += 1
                j += 1
    
            if j == M: 
                matches.append(i-j)
                j = lps[j-1] 

            elif i < N and pattern[j] != text[i]: 

                if j != 0: 
                    j = lps[j-1] 
                else: 
                    i += 1
        return matches

    def build_lps(self, pattern):
        """
        Build longest prefix that is also a suffix lookup table, for
        KMP string matching.

        Parameters:
        -----------
        pattern: `str`
            Pattern to search for.
        Returns:
        ----------
        lps: `int`
            List of longest prefix that is also a suffix for each substring 
            length.

        """


        length = 0 
        M = len(pattern) 

        lps = [0]*M
        lps[0] 
        i = 1

        while i < M: 
            if pattern[i] == pattern[length]: 
                length += 1
                lps[i] = length
                i += 1
            else: 

                if length != 0: 
                    length = lps[length-1] 
                else: 
                    lps[i] = 0
                    i += 1
        
        return lps

class ParallelStringMatching(StringMatching):
    """
    String matching algorithms adapted for parallel execution.
    """

    def result_shifting(self, matches, lower_limit):
        """
        Shift parallel results to match original text indices.

        Parameters:
        -----------
        matches: `int`
            Array of string matches indices
        lower_limit: `int`
            Lower segment limit
        
        Returns:
        ----------
        matches: `int`
            Corrected array of string matches indices
        """

        for i in range(len(matches)):
            matches[i] = matches[i] + lower_limit
        return matches

    def naive_algorithm(self, pattern, text, segment):
        """
        Parallel adapted naive algorithm for string searching.

        Parameters:
        -----------
        pattern: `str`
            Pattern to search for.
        text: `str`
            Text to search in.

        Returns:
        --------
        matches: `int`
            List of indices where mathces where found.
        """

        matches = super().naive_algorithm(pattern, text)
        return self.result_shifting(matches, segment[0])

    def kmp_algorithm(self, pattern, text, segment, lps):
        """
        Parallel adapted naive algorithm for string searching.

        Parameters:
        -----------
        pattern: `str`
            Pattern to search for.
        text: `str`
            Text to search in.

        Returns:
        --------
        matches: `int`
            List of indices where mathces where found.
        """

        matches = super().kmp_algorithm(pattern, text, lps)
        return self.result_shifting(matches, segment[0])
        
class ParallelPreprocessing():
    """
    Preprocessing steps, preparing input to parallel workflow.
    """

    @staticmethod
    def calculate_segment_size(text, processors):
        """
        Calculate segments sizes to be treated by parallel string 
        search algorithm.

        Parameters:
        -----------
        text: `str`
            Input text
        processors: `int`
            Processor count

        Returns:
        ----------
        segments: 
            Array of with segment sizes
        """
        
        t_lenght = len(text)
        seg_size = int(t_lenght/processors)
        
        add = 0
        
        if t_lenght % processors != 0:
            add = (t_lenght % processors)

        # Loop sets the segment length based on the processor count
        segments = []
        for i in range(processors):
            if i != 0:
                segments.append(
                        [((seg_size * i) + add), ((seg_size * (i+1)) + add)]
                )     
            else:
                segments.append(
                        [(seg_size * (i)), ((seg_size * (i+1)) + add)]
                )
        
        # While setting segment length words may get cut, this loop searches for
        # sequences of characters and separates them when it finds a space or 
        # punctuation. In this way, the length to be processed is scaled through 
        # processors, giving the first processor the biggest data to treat, and 
        # lowering data size for subsequent processors.
        last_upper_limit = 0
        for i in segments:

            if last_upper_limit != i[0]:
                i[0] = last_upper_limit

            j = 0
            while True:
                if i[1] + j < len(text) and text[i[1] + j].isalnum():
                        j += 1   
                else:
                    i[1] = i[1] + j
                    break
            last_upper_limit = i[1]

        return segments
    
    @staticmethod
    def get_text_segments(text, processors):
        """
        Get text segments.
        
        Parameters:
        -----------
        text: `str`
            Input text.
        processors: `int`
            Processor count.
        Returns:
        ----------
        sliced_text: `str`
            Input text sliced in segments
        segments: `int`
            Array with boundaries for segments
        """

        segments = ParallelPreprocessing.calculate_segment_size(
                                                                text, 
                                                                processors
        )
        sliced_text = []
        for seg in segments:
            sliced_text.append(text[seg[0]:seg[1]])
        
        return sliced_text, segments
