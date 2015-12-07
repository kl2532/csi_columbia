# Assignment 4

Group 5: Brian Trippe (blt2114), David Streid (dcs2153), Diego Paris (drp2121), Katie Lin (kl2532)



## General Approach

 Though all humans share the same same set of autosomal and mitochrondrial genes, there variations in the specific sequences.  These variations in a person's genome are inherited from one's parents and a few also arise de novo.

 The specific set of variations that exist in one's genome are unique to that person and are responsible for heritable traits.  Additionally, because the vast majority of SNP's are inherited from one's parents (and by extension, his ancestors), these variations carry information about an individuals ancestry.

###Identifying a person uniquely

 The likelihood of given set of SNP's occurring is proportional to the number individuals we expect to carry that set of SNP's.  This means that if we would like to identify a person uniquely, we will need to be considering a set of SNP's whose probability of occurring is on average equal to 1/P, where P is the population size.

####Methodology
 From the perspective of information theory, this means that we are looking to have a distribution over SNP's that whose entropy is -log<sub>2</sub>(1/P).  So, if we are consider the entire world population, we require a distribution with entropy ~= 33, because then draws from the distribution will on average provide 33 bits of information, enough to describe one in 7 Billion people.

####Our Task
 In our case, the task is simpler, as we have been told that our mystery man (or woman) is of of ~2000 people, i.e.  the person is either James Watson, Craig Venter, Professor Erlich, or someone from the 1000 genomes project.  Given this hint, We need only approximately 12 bits of information to identify our person.

 To calculate the number of SNP's we need to identify someone in this case, must consider the amount of information we will get from each one.  This varies by SNP (since a SNP that corresponds to one of 3 equally likely alleles will carry more information than an SNP that takes the same value in 90% of individuals.

 Nevertheless, the expected bits of information from a SNP is a useful quantity to know, so we wrote a script to calculate the average entropy of SNP's reported in the 1000 genomes project release of dbsnp.vcf .  From this, the expected information gain of an SNP was found to be 0.21 bits.  Given this, <b>only 55 independent SNP's would be needed</b>.

 This assumption is violated, however, by any linkage disequilibrium(LD) that might occur between SNP's.  Had we been working with Illumina reads, LD would not be a very significant concern as SNP's on different chromosomes or far apart along the same chromosome are independently distributed.  However, since we have multiple SNP's on each read (on average), this is potentially quite significant in our case.

 The number of SNP's in our experiments that are required will be larger than 50, however, given that some of the SNP's found will likely be erroneous due to the large amount of noise in our data.

###Discovering Ancestry and Population History
 Because SNP's are obtained from ancestors, given the frequencies of occurrence of different SNP's in different populations, one can use observed SNP's to back out most probable ancestral populations.  We used the SPSmart tool to do this analysis for us freely online.

 Additionally, the mixed membership model introduced in the 2001 Pritchard paper discussed in class describes one can discover hidden population structure and ancestral genomes from the SNP's of a set of individuals. If time allowed, we hoped to run their algorithm on the 1000 genomes project genomes and then compare SNP's present in our sample with the discovered components.

###Trait/Phenotype Prediction
 Since SNP's are responsible for many of traits, the probability of our individual possessing given traits can potentially be assessed from the SNP's we observe in our sample.  The correlations of many SNP's with disease traits has been investigated by an array of different Genome Wide Association Studies (GWAS's).  These correlations are <b>often included in annotations of SNP's such as those in the 1000 genomes project release of dbsnp.vcf</b> 

 It is worth of note, however, that most SNP's are not directly responsible for observable traits.

####Disease Phenotypes
 Disease phenotypes are the most common annotated correlations.  This is because of much of the public genomic information is produced in medical research studies.  This fact biases the composition of SNP annotations towards many disease-focussed annotations.  We hope to use these annotations to predict possible disease phenotypes in our individual.

####Traits of Appearance
 A handful of traits exist for which the relationship between genetics and phenotype is well understood.  For a few of these, we looked to see if we had observed SNP's with known correlation to see if we could predict the traits.  This was not a hopeful endeavor, however, because our read coverage of a MinIon  nano-pore sequencer is very low.  We looked for SNP's in our data associated with eye-color, hair-color, and earwax texture, but were unfortunately unable to find success.

####Using Imputation for More Information
 To get more information on traits, we sought to use genetic imputation.  Imputation takes advantage of LD to predict the likely variants of SNP's nearby those you have observed.  The technique is founded on the assumption that nearby SNP's are in linkage disequilibrium and uses calculated ancestral sequences and SNP's.  A seemingly convenient online <b>tool for performing imputation is the Michigan Imputation Server</b>.

 We attempted to use the Michigan Imputation Server on our data but after hours of struggling to massage our VCF's into the proper format, and understand cryptic error messages, we admitted defeat and settled for using only our observed SNP's.

####Gender
 Predicting gender from reads is by far the most straight-forward task we could hope to perform.  Since males carry a Y-Chromosome but women do not, observing reads that align to the Y chromosome with high significance would signal that the sample comes from a male, while observing no reads on chrY would signal the sample is likely female.

 This later case is, however, slightly complicated by the fact that, with only a small number of aligned reads, there is a non-trivial probability of observing no reads on the Y-Chromosome even if the individual is a male.  If this were the case, we planned to predict male v.s. female based on the likelihoods of getting the observed number of reads aligned to the X chromosome and 0 reads aligned to the Y chromosome given that the sample came from a man or from a woman.  <b>The number of reads on the X chromosome is informative because women have two copies of the X chromosome while men have only one</b>.

 Luckily, we observed several reads on the Y chromosome and did not need to delve into this analysis.


## Findings
### MinIon Sequencing Information

 Comparing our sequencer output to the previous Hackathon, we see that the average reads per channel is much less. This may be attributed to longer reads, which would lead to fewer reads per channel.

|                           | What did Sophie eat?                     | CSI Columbia                              |
|---------------------------|:----------------------------------------:|:-----------------------------------------:|
| Active Channels           | 251                                      | 216                                       |
| Average reads per channel | 101.25498008                             | 24.912037037                              |
|                           | Channel 90 has most reads with 449 reads | Channel 224 has most reads with 123 reads |

#### Statistics regarding *2D reads*:

|        | Total # of Reads | Longest Read (bp) |
|--------|------------------|-------------------|
| Passed | 2,272 (42%)      | 42,974            |
| Failed | 3,109 (58%)      | 46,250            |

#### Alignment to hg19 using BWA-MEM ONT

 2,091 reads aligned (92%) out of 2,272 2D passed reads

#### Substitution matrix:

| Nucleotide | A | C | T | G | Del |
| --- | --- | --- | --- | --- | --- |
| A | 364290 | 3459 | 1618 | 3591 | 10947 |
| C | 1691 | 246343 | 2550 | 2505 | 6171 |
| T | 1576 | 3743 | 365034 | 3290 | 18011 |
| G | 2443 | 2466 | 1591 | 246612 | 6213 |
| Ins | 7596 | 8785 | 10782 | 9589 | N/A |

### Analysis Pipeline

<img src="./img/pipeline1.JPG" width="800">

 1. Align reads `bwa mem -x ont2d ref.fasta reads.fastq > aln1.sam`
 2. Creates .bam file from .sam `samtools view -b -S -o aln1.bam aln1.sam`
 3. Creates aln1sorted.bam (ordered by chromosome) `samtools sort aln1.bam aln1sorted`
 4. Creates bcf (can use sorted bam too) `samtools mpileup -uf h19.fasta aln1sorted.bam > aln1.bcf`
 
 Determined 2,091 reads aligned (92%) out of 2,272 2D passed reads.
 5. Generate RSIDs

     To generate RSIDs, we had 2 approaches:

       A. *BAM Analysis Kit* generated 1,344 RSIDs

       B. `samtools` generated 2,370 RSIDs

 At first, we used the BAM Analysis Kit's generated RSIDs to perform our analysis. We wanted to check the RSIDs using `samtools` as a verification method but it generated RSIDs that were disjoint from BAM Analysis Kit's. We decided to use the RSIDs from `samtools` for the following reasons:
  * Double the number of RSIDs 
    * 2,370 (samtools) vs. 1,344 (BAM analysis kit)
  * ~10x more hits on potential candidates
  * Better Documentation

 6. Use RSIDs to find more information about individual

 <img src="./img/pipeline2.JPG" width="800">
 

  With the RSIDs, we used the following resources:
  * SPSmart
    * Ancestry
      * Matched RSIDs with 1000 Genome data set

  * NCBI dbSNP database
    * Reference SNP Cluster Report
      * Looked at report for each rsid
    * Genotype Report
      * Submitted RSIDs via batch query and received XML with information about population and individuals
    * SNP-Phenotype Association 
      * Submitted RSIDs via batch query and received XML with information regarding genes

### Comparing Genomes

|                | Yaniv Erlich | James Watson (NCBI ftp file) | James Watson (NCBI dbSNP Genomic Report) | Craig Venter (Venter Institute ftp file) | Craig Venter (NCBI dbSNP Genomic Report) | 1000 Genomes |
|----------------|--------------|------------------------------|------------------------------------------|------------------------------------------|------------------------------------------|--------------|
| RSID matches   | 87           | 402                          | 723                                      | 248                                      | 554                                      | 0            |
| RSIDs reported | 960,614      | 2,060,544                    | Unknown                                  | 4,017,989 ssids                          | Unknown                                  | N/A          |

 Notes:

   * Yaniv Erlich's RSIDs restricted to 23andMe assay
   * James Watson: NCBI ftp file from ftp://ftp.ncbi.nlm.nih.gov/hapmap/jimwatsonsequence/
   * Craig Venter: Venter Institute ftp file from ftp://ftp.jcvi.org/pub/data/huref/
   * NCBI Genomic Report generated from [here] (http://www.ncbi.nlm.nih.gov/projects/SNP/dbSNP.cgi?list=rslist)
     * 1000 Genomes is included in NCBI report as population categories (i.e. EUR, AFR, AMR) but individuals are not included

#### Comparison using ftp files

<img src="./img/ftp_comparison.JPG" width="400">

|                | Watson    | Venter    | Erlich  |
|----------------|-----------|-----------|---------|
| matches        | 402       | 248       | 87      |
| RSIDs reported | 2,060,544 | 4,017,989 | 960,614 |

#### Comparison using NCBI dbSNP Genomic Report

<img src="./img/ncbi_comparison.JPG" width="500">

|         | Bushman KB1 | Watson | Venter | Erlich |
|---------|-------------|--------|--------|--------|
| matches | 838         | 723    | 554    | 87     |

It is interesting to note that Bushman KB1 was the individual with the greatest number of matching alleles compared to our sample. However, we can eliminate him because based on the 1000 Genomes, our individual is most likely of European descent.

`python parse_genotype_report2.py sample2geno.txt ncbi_genotype_report2.xml`

#### Identifying 

Only looking at Erlich, Watson, and Venter, our best guess would be Watson. 

Keep in mind that:

  * 20,102,536 bases read
  * 14,681,244 bases aligned 
  * 31,170 variants
  * 2,370 rsids tagged SNP's

### Findings of Individual

#### SNP's on the mitochondria?

 None detected

 Reasons:

 * Mitochondrial Size is small, but high copy number
     * human genome 3.2 Gbp, copy number 2 (6.4 Gbp)
     * mitochondrial genome 16 Kbp, copy number ~100 (1.6 Mbp)
     * 1.6:6400 MtDNA:nDNA… that’s 1:4000!
 * MinIon Reads on every chromosome, none on MtDNA


#### Gender

Male

 * 10 reads on Y chromosome
 * 94 SNP's found on Y chromosome

 * Genes found:
     * SPATA9
       * Spermatogenesis
     * PATE3
       * prostate and testis expressed


#### Ancestry

<img src="./img/ancestry_comparison.JPG" width="500">

 Using [SPSmart] (http://spsmart.cesga.es/), rsid matcher with 1000 Genomes dataset:

| Group            | Frequency allele from sample matched |
|------------------|--------------------------------------|
| Population Set 1 | 0.5012488888888882                   |
| Europe           | 0.5225288888888893                   |
| America          | 0.5131288888888886                   |
| Africa           | 0.4668466666666665                   |
| East Asia        | 0.4950622222222223                   |

 Num of matched rsids =  900

 Num of unmatched rsids =  1470
 
 `python get_ancestry2.py sample2geno.txt results_sample2.csv`

#### Phenotypic Traits

 High number of Exon rsids (3.65% of rsids) -- relative to background (1.1-1.4% of DNA exonic) -- but still not enough to be useful (only 49 rsids!)

 Exon rsids:

  * rs1421085 -- allele: C
      * Gene: FTO
          * (C;C) ~1.7x increased obesity risk
          * (C;T) ~1.3x increased obesity risk

Consulted [SNPedia] (http://www.snpedia.com/index.php) for phenotypes.

Web scraper for [SNPedia] (http://www.snpedia.com/index.php) `python phenotype.py sample2geno.txt`

#### Diseases

| rsid        | Gene     | Allele | Description                                                    |
|-------------|----------|--------|----------------------------------------------------------------|
| rs148226094 | SLC4A1AP | C      | Associated with lung cancer                                    |
| rs61421071  | ISG20    | C      | Associated with mast cell disease and malignant glioma (tumor) |
| rs2487303   | KIF26A   | G/A    | Associated with megacolon (abnormal dilation of the colon)     |
| rs375771024 | SLIT2    | A      | Associated with Crohn's colitis                                |
| rs238406    | ERCC2    | A      | Associated disease xeroderma pigmentosum, group d              |

 Information mapping rsid to gene generated from [NCBI XML(Full) report] (http://www.ncbi.nlm.nih.gov/projects/SNP/dbSNP.cgi?list=rslist)
 
 Parsing XML file: `python parse_full_xml_report.py ncbi_full_report.xml`

 Further details about genes found at [GeneCards] (http://www.genecards.org/)

### Conclusions

Only looking at Erlich, Watson, and Venter, our best guess would be Watson.  This is our guess because we had the largest number of SNP's in our sample also present in Watson's genome.  However, due to the large number of SNP's present in Watson's genome along our read sequence which we did not observe, this identification is made with very little confidence.  We believe it is more likely that our individual is a someone who is in the 1000 genomes project.  Given more time to check our found SNP's against the SNP's for all of these individuals, we would be able to better assess this possibility and likely would be able to make a much more confident identification. 

#### Information Usefulness

 * 73% of Bases aligned
 * 9% of Variants have RSID tags
 * ~2,000 rsids, ~500 expected by chance
 * Linkage disequilibrium reduces information gain
 * 659 reads have rsids 

