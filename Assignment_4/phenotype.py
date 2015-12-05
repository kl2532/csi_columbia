# -*- coding: utf-8 -*-
"""
Usage: Usage: (python) phenotype.py sample2geno.txt
Web script for looking up phenotypes on SNPedia from a list of RSIDs
"""

from lxml import html
import requests
import sys

def get_phenotype(genome_snps):
    phenotype_dict = {}
    f = open(genome_snps)  
    for line in f:
        row = line.split()
        rsid = row[0].strip()
        base = row[1].strip()
        # example URL: http://www.snpedia.com/index.php/rs79063870(G;G)
        uri = rsid + '(' + base + ';' + base + ')'
        url = 'http://www.snpedia.com/index.php/' + uri  
        page = requests.get(url)

        tree = html.fromstring(page.content)
        all_rows = tree.xpath('//table[@class="table"]/tr')
        row_info = []
        
        # retrieve all contents of table
        for row in all_rows:
            row_info.append(row.text_content())
        # if there is a table on the webpage
        if len(row_info) != 0:
            # retrieve description of phenotype and gene
            phenotype_dict[uri] = [row_info[0], row_info[3]]
            info = uri + "\t" + row_info[0] + "\t" + row_info[3]
            # write rsid, alleles, description, and gene to file
            with open('phenotype.txt','ab') as f: f.write(info)
    return phenotype_dict

if __name__ == '__main__':
    if len(sys.argv) != 1:
        genome_snps = sys.argv[1]
        get_phenotype(genome_snps)
    else:
        print 'Usage: (python) phenotype.py sample2geno.txt'