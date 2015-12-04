# -*- coding: utf-8 -*-
"""
Usage: (python) get_ancestry.py genome_full_snps.txt <.csv files>
Returns a dictionary of the ancestry likelihood based on SNPs
Example:
        $ python get_ancestry.py genome_full_snps.txt results.csv results2.csv
"""

import sys
import csv

def build_population_dict(csv_files):
    """Returns dictionary of the following form:
            { rs2753318 : 
                {'Population Set 1': [freq_A, freq_C, freq_G, freq_T],
                 'EUROPE': [freq_A, freq_C, freq_G, freq_T],
                 'AMERICA': [freq_A, freq_C, freq_G, freq_T],
                 'AFRICA': [freq_A, freq_C, freq_G, freq_T],
                 'EAST ASIA': [freq_A, freq_C, freq_G, freq_T]
                }
            }
        built from csv_files information"""
        
    population_dict = {}
    for csv_file in csv_files:
        f = open(csv_file)
        csv_f = csv.reader(f)
        
        #skip 2 header lines
        next(csv_f)
        next(csv_f)

        for row in csv_f:
            rsid = row[0]
            ancestry = row[7]
            if row[9] == '':
                continue
            else:  
                freq_A = float(row[9])
                freq_C = float(row[10])
                freq_G = float(row[11])
                freq_T = float(row[12])
            if rsid not in population_dict:
                population_dict[rsid] = {}
            population_dict[rsid][ancestry] = [freq_A, freq_C, freq_G, freq_T]
    return population_dict
        
def get_ancestry(genome_snps, csv_files):
    """Returns dictionary of the ancestry likelihood of the form:
            {'Population Set 1': ###,
                 'EUROPE': ###,
                 'AMERICA': ###,
                 'AFRICA': ###,
                 'EAST ASIA': ###
            }"""
    population_dict = build_population_dict(csv_files)
    ancestry_dict = {}
    total_frequencies = 0
    unmatched = 0
    
    f = open(genome_snps)  
    # skip header
    next(f)   
    for line in f:
        row = line.split()
        rsid = row[0]
        print rsid
        with open('rsid.txt','a') as f2: f2.write(rsid + '\n')
        base = row[3][0]
        if base == 'A':
            base = 0
        elif base == 'C':
            base = 1
        elif base == 'G':
            base = 2
        elif base == 'T':
            base = 3
        else:
            print 'error ', base, ' not found'
            continue
        # retrieve frequencies for each ancestry aligning to base in genome_snps
        if rsid in population_dict:     
            for ancestry in population_dict[rsid]:
                if ancestry not in ancestry_dict:
                    ancestry_dict[ancestry] = 0.0
                # add to cumulative frequency
                if ancestry == 'Population Set 1':
                    if population_dict[rsid][ancestry][base] == 0:
                        print rsid, " not found in any ancestry"
                ancestry_dict[ancestry] += population_dict[rsid][ancestry][base]
            total_frequencies += 1
        else:
            unmatched += 1
    # finally, divide cumulative frequency / total_frequencies
    for key in ancestry_dict:
        cumulative_frequency = ancestry_dict[key]
        ancestry_dict[key] = cumulative_frequency / total_frequencies
        
    print ancestry_dict
    print '# of matched rsids = ', total_frequencies
    print '# of unmatched rsids = ', unmatched
        
   
if __name__ == '__main__':
    if len(sys.argv) != 1:
        genome_snps = sys.argv[1]
        csv_files = sys.argv[2:]
        get_ancestry(genome_snps, csv_files)
    else:
        print 'Usage: (python) get_ancestry.py genome_full_snps.txt <.csv files>'
        print 'Example: \
            python get_ancestry.py genome_full_snps.txt results.csv'