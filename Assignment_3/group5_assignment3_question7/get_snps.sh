#/bin/sh
# script for problem 7, takes reference genome fasta and sam file
if [ "$#" -ne 3 ];then
    echo "./group5_assignment3_question7.sh <aligned.sam> <hg19.fa> <snp.txt>"
    exit
fi

align_sam=$1
ref_fa=$2
output_fn=$3

samtools mpileup --max-depth 8000 -I $align_sam -f $ref_fa | grep -v "\t0\t" | awk '{ print $3 "\t"$5 }' > $output_fn
