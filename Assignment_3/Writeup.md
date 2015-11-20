#Assignment 3
##QC and alignment
1. EDIT
Statistics on 1D vs 2D reads in Pass and Fail
 * Number of 2D reads classified as 'failed' = 3109
 * Number of 2D reads classified as 'passed' = 2272
 * % of 2D reads that are 'Failed' = 42%
 * % of 2D reads that are 'Pass' = 100%

2. 
   Active Channels =  216

   Average reads per channel =  24.912037037

   Channel 224 has most reads with 123 reads
   
   `$ python group5_assignment3_question2.py fastq/2D-fail.fastq fastq/2D-pass.fastq fastq/1D-fail.fastq fastq/1D-pass.fastq`

3. 

   Plot Cummulative Distribution of Nucleotides over Time (hours)

   **Cummulative Distribution of Nucleotide reads, 2d passed**

   <img src="./img/question3/pass_2d.png" width="600">

   **Cummulative Distribution of Nucleotide reads, 2d failed**

   <img src="./img/question3/fail_2d.png" width="600">

   **Cummulative Distribution of Nucleotide reads, 1d failed**

   <img src="./img/question3/fail_1d.png" width="600">

   **Cummulative Distribution of Nucleotide reads, 1d failed**
   `There are no 1D pass reads`

4. 
   **Length distribution of 2D reads, failed**
   
   `$ python group5_assignment3_question4.py fastq/2D-fail.fastq 2D-fail.png`
   
   <img src="./img/question4/2D-fail.png" width="600">
   
   **Length distribution of 2D reads, passed**
   
   `$ python group5_assignment3_question4.py fastq/2D-pass.fastq 2D-pass.png`
   
   <img src="./img/question4/2D-pass.png" width="600">
   
5. Longest reads:

   | 2D | Nucleotides |
   | --- | --- | 
   | Passed |42974 |
   | Failed | 46250 |
   
   `$ python group5_assignment3_question5.py fastq/2D-pass.fastq`
   
   `$ python group5_assignment3_question5.py fastq/2D-fail.fastq`
   
6. 
7. EDIT
followed [tutorial](http://biobits.org/samtools_primer.html)

Confusion Matrix
Columns are reference
Rows are calls
        | Nucleotide    | A | C | T | G |
        | --- | --- | --- | --- |
        | A | 264985 |  1200 | 1159 | 1741 |
        | C | 2587 | 174292 | 2758 | 1731 |
        | T | 1158 | 1787 | 268059 | 1127 |
        | G | 2653 | 1772 | 2431 | 175448 |


8. EDIT - Three Strategis to Reduce the Number of Errors in the Reads
I) Greedy Algorithm - Check for highly interoperable regions
	Fill in based on many reference reads
II) Cross-Reference overlapping reads
III) Plotting frequency of alignments at positions
	-Should have a uniform distribution
IV) Map regions that map to highly variable regions 
	-Exclude regions that only align to highly variable regions
	-Mask areas of the genome that we are uncertain about


