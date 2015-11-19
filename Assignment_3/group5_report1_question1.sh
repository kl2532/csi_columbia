# script for problem one, takes two fastq files
if [ "$#" -ne 1 ];then
    echo "./group5_report1_question1.sh <downloads_dir_path>"
    exit
fi

downloads_dir_path=$1
fail_dir=$downloads_dir_path"/fail"
pass_dir=$downloads_dir_path"/pass"

# get number of pass 2D sequences.
pass_2d=`poretools fasta --type 2D $pass_dir | wc -l`
pass_2d=`echo $pass_2d / 2 | bc`
echo "number of pass 2D: $pass_2d"

# get number of pass sequences total.  This is the same as the number of 
# forward pass reads.
pass_fwd=`poretools fasta --type fwd $pass_dir | wc -l`
pass_fwd=`echo $pass_fwd / 2 | bc` # this is equal to the total number of sequences.
echo "number of passed sequences: $pass_fwd"

# by subtracting, find the number of 1D reads
pass_1d=`echo $pass_fwd - $pass_2d | bc`
echo "number of pass 1D: $pass_1d"

# do the same for the 'fail' reads.
fail_2d=`poretools fasta --type 2D $fail_dir | wc -l`
fail_2d=`echo $fail_2d / 2 | bc`
echo "number of failed 2D: $fail_2d"

fail_fwd=`poretools fasta --type fwd $fail_dir | wc -l`
fail_fwd=`echo $fail_fwd / 2 | bc` # this the total number of sequences.
echo "number of failed sequences: $fail_fwd"

fail_1d=`echo $fail_fwd - $fail_2d | bc`
echo "number of failed 1D: $fail_1d"

# calculate and report the percent of reads in pass and fail that are 2D.
pass_2D_percent=`echo $pass_2d '*' 100 / $pass_fwd | bc`
echo $pass_2D_percent "% of Pass reads are 2D"

fail_2D_percent=`echo $fail_2d '*' 100 / $fail_fwd | bc`
echo $fail_2D_percent "% of fail reads are 2D"

total_2D=`echo $fail_2d + $pass_2d | bc`
percent_2D_pass=`echo $pass_2d '*' 100 / $total_2D | bc`
echo $percent_2D_pass"% of 2D reads are 'Pass'"

total_1D=`echo $fail_1d + $pass_1d | bc`
percent_1D_pass=`echo $pass_1d '*' 100 / $total_1D | bc`
echo $percent_1D_pass"% of 1D reads are 'Pass'"
