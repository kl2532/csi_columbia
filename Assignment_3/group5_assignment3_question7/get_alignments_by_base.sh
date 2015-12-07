#/bin/sh
# script for problem 7, takes reference genome fasta and sam file
if [ "$#" -ne 3 ];then
    echo "./group5_assignment3_question7.sh <aligned.sam> <reference.fa> <alignment_by_base.txt>"
    exit
fi

align_sam=$1
ref_fa=$2
output_fn=$3

# grep for lines that have 1 read since too much output with 0 reads.
samtools mpileup --max-depth 8000 $align_sam -f $ref_fa | grep "\t1\t" > $output_fn
