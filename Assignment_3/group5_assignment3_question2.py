# -*- coding: utf-8 -*-
"""
Usage: (python) group5_assignment3_question2.py <.fastq files>
Calculates the average reads per active channel among inputted FASTQ files.
Also provides channel in flow-cell that produced the most reads with the
amont read.
Example:
        $ python group5_assignment3_question2.py \
            fastq/2D-fail.fastq fastq/2D-pass.fastq \
            fastq/1D-fail.fastq fastq/1D-pass.fastq
"""

import sys
import itertools
from collections import Counter

def average_reads(fastq_files):
    """Prints number of active channels, average reads, and 
        channel with most reads"""
    active_channel_count = Counter()
    total_reads = 0
    for fastq_file in fastq_files:
        #print fastq_file
        with open(fastq_file, 'rb') as f:
            # Get every 4th line
            fourthlines = itertools.islice(f, 0, None, 4)
            for id_line in fourthlines:
                # id line is formatted as such: TeamDiego_2542_1_ch101_file32_
                # need to extract "101"
                index_of_ch = id_line.find("ch")
                start = index_of_ch + 2
                end = start + id_line[start:].find("_")
                chan_num = id_line[start:end]
                # update count
                active_channel_count[chan_num] += 1
                total_reads += 1
            
    active_channels = float(len(active_channel_count))
    print "Active Channels = ", active_channels
    avg_reads = total_reads / active_channels
    print "Average reads = ", avg_reads
    
    # Find channel with most reads
    max_reads = 0
    max_channel = 0
    for ch in active_channel_count:
        if active_channel_count[ch] > max_reads:
            max_reads = active_channel_count[ch]
            max_channel = ch
            
    print "Channel", max_channel, "has most reads with", max_reads, "reads"
   
if __name__ == '__main__':
    if len(sys.argv) != 1:
        fastq_files = sys.argv[1:]

        average_reads(fastq_files)
    else:
        print 'Usage: (python) group5_assignment3_question2.py <.fastq files>'
        print 'Example: \
            python group5_assignment3_question2.py \
            fastq/2D-fail.fastq fastq/2D-pass.fastq\
            fastq/1D-fail.fastq fastq/1D-pass.fastq'