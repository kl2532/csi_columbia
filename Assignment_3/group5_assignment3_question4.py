# -*- coding: utf-8 -*-
"""
Usage: (python) group5_assignment3_question4.py <.fastq file> <.png file>
Plots histogram of the length distribution of FASTQ file.
Outputs plot into provided .png filename.
Examples:
        $ python group5_assignment3_question4.py fastq/2D-fail.fastq 2D-fail.png
        $ python group5_assignment3_question4.py fastq/2D-pass.fastq 2D-pass.png
"""

import sys
import itertools
import rpy2.robjects as robjects
import rpy2.robjects.lib.ggplot2 as ggplot2
from rpy2.robjects.packages import importr
                
def plot_histogram(fastq_file, plot_filename_png):
    """Plots histogram of length distribution of sequence in fastq_file and
        saves to plot_filename_png"""
    r = robjects.r
    r.library("ggplot2")
    grdevices = importr('grDevices')
    
    sizes = []
    
    with open(fastq_file, 'rb') as f:
        # skip first line
        for _ in itertools.islice(f, 0, 1):
            pass
        # Get every 4th line with raw sequence letters
        fourthlines = itertools.islice(f, 0, None, 4)
        for line in fourthlines:
            sizes.append(len(line.strip()))
            
    sizes = robjects.IntVector([s for s in sizes])

    sizes_min = min(sizes)
    sizes_max = max(sizes)
    
    binwidth = (sizes_max - sizes_min) / 20
    
    d = {'sizes' : sizes}
    df = robjects.DataFrame(d)
    
    # plot
    gp = ggplot2.ggplot(df)
    
    pp = gp + ggplot2.aes_string(x='sizes') \
            + ggplot2.geom_histogram(binwidth=binwidth) \
            + ggplot2.theme_grey() \
            + ggplot2.labs(title =plot_filename_png, \
                x = "Size (in nucleotides)", y = "Count") 
            
    grdevices.png(plot_filename_png, width = 8.5, height = 8.5, 
                units = "in", res = 300)
    pp.plot()
    grdevices.dev_off()

if __name__ == '__main__':
    if len(sys.argv) == 3:
        script, fastq_file, plot_filename_png = sys.argv
        if(plot_filename_png.lower().endswith('.png')):
            plot_histogram(fastq_file, plot_filename_png)
        else:
            print '2nd argument must be a .png file'
    else:
        print 'Usage: \
            python group5_assignment3_question4.py <.fastq file> <.png file>'
        print 'Example: \
            python group5_assignment3_question4.py fastq/2D-fail.fastq 2D-fail.png'