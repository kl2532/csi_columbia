# -*- coding: utf-8 -*-
"""
Usage: (python) parse_genotype_report.py genome_full_snps.txt <.xml files>
Returns number of rsid matches with Watson, Venter, and NCBI results
Example:
        $ python parse_genotype_report.py genome_full_snps.txt ncbi_genotype_report.xml
"""

import sys

WATSON_INDId = 30346
VENTER_INDId = 30342

THOUSAND_GENOME_popId = [13136, 13148, 13149, 13150, 16651, 16652, 16653, 16654, 16655];

def build_thousand_genotype_dict(genotype_reports):
    """Returns dictionary with 1000 Genomes information of the form:
            { rsid : [{popId: {allele: [freq, counter], allele: [freq,counter]}, ... } ,
                      {gtype T/T: [indId, indId, ...], ... }
                     ]
            }
        built from genotype_reports information"""
        
    population_dict = {}
    # retrieve information from each XML file
    for genotype_report in genotype_reports:
        f = open(genotype_report)
        for line in f:
            # reached a rsid
            if "<SnpInfo rsId=" in line:
                start_quote = line.index('"')
                end_quote = line.index('"', start_quote+1)
                rsid = line[start_quote+1:end_quote]
                if rsid not in population_dict:
                    population_dict[rsid] = [{}, {}]
                try:
                    # while we haven't reached the end of the rsid information
                    while line.strip() != "</SnpInfo>":
                        line = f.next()
                        if "<ByPop popId=" in line:
                            start_quote = line.index('"')
                            end_quote = line.index('"', start_quote+1)
                            popId = line[start_quote+1:end_quote]
                            # check if popId is one of the 1000 Genome popIds
                            if int(popId) in THOUSAND_GENOME_popId:
                                line = f.next()
                                while line.strip() != "</ByPop>":
                                    if "<AlleleFreq allele=" in line:
                                        start_quote = line.index('"')
                                        end_quote = line.index('"', start_quote+1)
                                        allele = line[start_quote+1:end_quote]
                                        start_quote = line.index('"', end_quote+1)
                                        end_quote = line.index('"', start_quote+1)
                                        freq = line[start_quote+1:end_quote]
                                        # update dictionary with popId information about allele frequency and update counter
                                        if popId not in population_dict[rsid][0]:
                                            population_dict[rsid][0][popId] = {}
                                        if allele not in population_dict[rsid][0][popId]:
                                            population_dict[rsid][0][popId][allele] = [float(freq), 1]
                                        else:
                                            population_dict[rsid][0][popId][allele][0] += float(freq)
                                            population_dict[rsid][0][popId][allele][1] += 1
                                    if "<GTypeByInd gtype=" in line:
                                        start_quote = line.index('"')
                                        end_quote = line.index('"', start_quote+1)
                                        gtype = line[start_quote+1:end_quote]
                                        # remove gtypes that are "-/AAA"
                                        # only look at gtypes that are of the form "A/A"
                                        if len(gtype) <= 3:
                                            if len(gtype) != 1:
                                                gtype = gtype[0] + gtype[2]
                                            start_quote = line.index('"', end_quote+1)
                                            end_quote = line.index('"', start_quote+1)
                                            indId = line[start_quote+1:end_quote]
                                            if gtype not in population_dict[rsid][1]:
                                                population_dict[rsid][1][gtype] = set()
                                            population_dict[rsid][1][gtype].add(indId)
                                    line = f.next()
                                # end while line != "</ByPop>":
                        # end if "<ByPop popId=" in line:
                    # end while line != "</SnpInfo>"
                except StopIteration:
                    continue
    return population_dict
    
def build_genotype_dict(genotype_reports):
    """Returns 3 dictionary:
        #1 General population information of the form:
            { rsid : [{popId: {allele: [freq, counter], allele: [freq,counter]}, ... } ,
                      {gtype T/T: [indId, indId, ...], ... }
                     ]
            }
        #2 Watson (indId = 30346):
            {rsid: gtypeT/T, rsid: gtype, ...}
        #3 Venter (indId = 30342):
            {rsid: gtypeT/T, rsid: gtype, ...}
        built from genotype_reports information"""
        
    population_dict = {}
    watson_dict = {}
    venter_dict = {}
    # retrieve information from each XML file
    for genotype_report in genotype_reports:
        f = open(genotype_report)
        for line in f:
            # reached a rsid
            if "<SnpInfo rsId=" in line:
                start_quote = line.index('"')
                end_quote = line.index('"', start_quote+1)
                rsid = line[start_quote+1:end_quote]
                if rsid not in population_dict:
                    population_dict[rsid] = [{}, {}]
                try:
                    # while we haven't reached the end of the rsid information
                    while line.strip() != "</SnpInfo>":
                        line = f.next()
                        #fill up dictionaries
                        if "<ByPop popId=" in line:
                            start_quote = line.index('"')
                            end_quote = line.index('"', start_quote+1)
                            popId = line[start_quote+1:end_quote]
                            line = f.next()
                            while line.strip() != "</ByPop>":
                                if "<AlleleFreq allele=" in line:
                                    start_quote = line.index('"')
                                    end_quote = line.index('"', start_quote+1)
                                    allele = line[start_quote+1:end_quote]
                                    start_quote = line.index('"', end_quote+1)
                                    end_quote = line.index('"', start_quote+1)
                                    freq = line[start_quote+1:end_quote]
                                    # update dictionary with popId information about allele frequency and update counter
                                    if popId not in population_dict[rsid][0]:
                                        population_dict[rsid][0][popId] = {}
                                    if allele not in population_dict[rsid][0][popId]:
                                        population_dict[rsid][0][popId][allele] = [float(freq), 1]
                                    else:
                                        population_dict[rsid][0][popId][allele][0] += float(freq)
                                        population_dict[rsid][0][popId][allele][1] += 1
                                if "<GTypeByInd gtype=" in line:
                                    start_quote = line.index('"')
                                    end_quote = line.index('"', start_quote+1)
                                    gtype = line[start_quote+1:end_quote]
                                    # remove gtypes that are "-/AAA"
                                    # only look at gtypes that are of the form "A/A"
                                    if len(gtype) <= 3:
                                        if len(gtype) != 1:
                                            gtype = gtype[0] + gtype[2]
                                        start_quote = line.index('"', end_quote+1)
                                        end_quote = line.index('"', start_quote+1)
                                        indId = line[start_quote+1:end_quote]
                                        if gtype not in population_dict[rsid][1]:
                                            population_dict[rsid][1][gtype] = set()
                                        population_dict[rsid][1][gtype].add(indId)
                                        if int(indId) == WATSON_INDId:
                                            if rsid not in watson_dict:
                                                watson_dict[rsid] = gtype
                                        if int(indId) == VENTER_INDId:
                                            if rsid not in venter_dict:
                                                venter_dict[rsid] = gtype
                                line = f.next()
                            # end while line != "</ByPop>":
                        # end if "<ByPop popId=" in line:
                    # end while line != "</SnpInfo>"
                except StopIteration:
                    continue
    return population_dict, watson_dict, venter_dict

def reverse_dict(orig_dict):
    """Returns reversed_dictionary where key is the frequency and value is array of indIds"""
    reverse_dict = {}
    for key in orig_dict:
        value = orig_dict[key]
        if value not in reverse_dict:
            reverse_dict[value] = [key]
        else:
            reverse_dict[value].append(key)
    return reverse_dict

def parse_genotype_report(genome_snps, genotype_reports):
    """Returns number of rsid matches with Watson, Venter, and NCBI results"""
    population_dict, watson_dict, venter_dict = build_genotype_dict(genotype_reports)
    thousand_dict = build_thousand_genotype_dict(genotype_reports)
    indId_dict_exact = {}
    indId_dict_allele = {}
    max_freq_exact = 0
    max_freq_allele = 0
    num_exact_watson = 0
    num_exact_venter = 0
    num_similar_watson = 0
    num_similar_venter = 0
    w_counter = 0
    v_counter = 0
    
    f = open(genome_snps)  
    # skip header
    next(f)
    for line in f:
        row = line.split()
        rsid = row[0][2:].strip()
        genotype = row[3].strip()
        
        # build dictionaries indId_dict_exact and indId_dict_allele with data from 1000 Genomes individuals
        # dictionary will determine how many matches each individual has with sample
        # if rsid in thousand_dict:
        #      genotype_dict = thousand_dict[rsid][1]
        #      if genotype in genotype_dict:
        #          for eachInd in genotype_dict[genotype]:
        #              if eachInd not in indId_dict_exact:
        #                  indId_dict_exact[eachInd] = 1
        #              else:
        #                 indId_dict_exact[eachInd] += 1
        #      for key in genotype_dict:
        #          if genotype[0] in key:
        #              for eachInd in genotype_dict[key]:
        #                  if eachInd not in indId_dict_allele:
        #                      indId_dict_allele[eachInd] = 1
        #                  else:
        #                      indId_dict_allele[eachInd] += 1 

        # build dictionaries indId_dict_exact and indId_dict_allele with data from all individuals
        # dictionary will determine how many matches each individual has with sample        
        if rsid in population_dict:
            genotype_dict = population_dict[rsid][1]
            if genotype in genotype_dict:
                for eachInd in genotype_dict[genotype]:
                    if eachInd not in indId_dict_exact:
                        indId_dict_exact[eachInd] = 1
                    else:
                       indId_dict_exact[eachInd] += 1
            for key in genotype_dict:
                if genotype[0] in key:
                    for eachInd in genotype_dict[key]:
                        if eachInd not in indId_dict_allele:
                            indId_dict_allele[eachInd] = 1
                        else:
                            indId_dict_allele[eachInd] += 1 

        # build dictionary to determine number of matches with Watson
        if rsid in watson_dict:
            watson_genotype = watson_dict[rsid]
            w_counter += 1
            if watson_genotype == genotype:
                num_exact_watson += 1
            if genotype[0] in watson_genotype:
                num_similar_watson += 1
        
        # build dictionary to determine number of matches with Venter
        if rsid in venter_dict:
            venter_genotype = venter_dict[rsid]
            v_counter += 1
            if venter_genotype == genotype:
                num_exact_venter += 1  
            if genotype[0] in venter_genotype:
                num_similar_venter += 1
    
    if len(indId_dict_exact) > 0:
        reverse_indId_dict_exact = reverse_dict(indId_dict_exact) 
        for freq in reverse_indId_dict_exact:
            if freq > max_freq_exact:
                max_freq_exact = freq
        print "indId", reverse_indId_dict_exact[max_freq_exact], "with", max_freq_exact, "exact genotype match"
        
    if len(indId_dict_allele) > 0:
        reverse_indId_dict_allele = reverse_dict(indId_dict_allele) 
        for freq in reverse_indId_dict_allele:
            if freq > max_freq_allele:
                max_freq_allele = freq
        print "indId", reverse_indId_dict_allele[max_freq_allele], "with", max_freq_allele, "allele match"
    
    print "# exact genotypes to Watson =", num_exact_watson
    print "# exact genotypes to Venter =", num_exact_venter
    print "# similar allele to Watson =", num_similar_watson
    print "# similar allele to Venter =", num_similar_venter
    print "rsid matches (Watson) =", w_counter
    print "rsid matches (Venter) ", v_counter
    print "# of rsids compared =", len(population_dict)
   
if __name__ == '__main__':
    if len(sys.argv) != 1:
        genome_snps = sys.argv[1]
        genotype_report = sys.argv[2:]
        parse_genotype_report(genome_snps, genotype_report)
    else:
        print 'Usage: (python) parse_genotype_report.py genome_full_snps.txt <.xml files>'
        print 'Example: \
            python parse_genotype_report.py genome_full_snps.txt ncbi_genotype_report.xml'