# -*- coding: utf-8 -*-
"""
Usage: (python) python group5_assignment3_question5.py <.fastq file>
Finds the longest read in a single FASTQ file. 
Examples:
        $ python group5_assignment3_question5.py fastq/2D-pass.fastq
        $ python group5_assignment3_question5.py fastq/2D-fail.fastq
"""

import sys
import itertools
                
def find_longest_read(fastq_file):
    """Prints longest read for a given FASTQ file"""
    sizes = []
    with open(fastq_file, 'rb') as f:
        # skip first line
        for _ in itertools.islice(f, 0, 1):
            pass
        fourthlines = itertools.islice(f, 0, None, 4)
        for line in fourthlines:
            sizes.append(len(line.strip()))
            
    sizes_max = max(sizes)
    
    print "Longest read for", fastq_file, "is", sizes_max, "nucleotides"

if __name__ == '__main__':
    if len(sys.argv) == 2:
        script, fastq_file = sys.argv

        find_longest_read(fastq_file)
    else:
        print 'Usage: python group5_assignment3_question5.py <.fastq file>'
        print 'Example: \
            python group5_assignment3_question5.py fastq/2D-pass.fastq'