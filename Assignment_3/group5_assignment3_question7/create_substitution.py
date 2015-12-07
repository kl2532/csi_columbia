"""Create substitution creates a substitution matrix from a tsv of snps

First column is the reference, second is read

"""

import sys

BASES = ['a', 'c', 't', 'g','gap']

def initialize_substitution():
    matrix = {}
    for b_ref in BASES:
        matrix[b_ref]={}
        for b_read in BASES:
            matrix[b_ref][b_read]=0
    return matrix

def main(argv):
    # Check valid inputs given.
    if len(argv) != 2:
        sys.stderr.write("invalid usage: python create_substitution.py" +
                         " <snps.txt>\n")
        sys.exit(2)

    snps_fn = argv[1]

    snps_file = open(snps_fn)

    conf_mat = initialize_substitution()

    for l in snps_file:
        # skip the first line.
        fields = l.strip("\n").split("\t")
        (ref, read) = (fields[2],fields[4])
        ref = ref.lower() 
        read = read.lower() # case is a function of ref/complement 
        if ref not in BASES:
            print "base \"" + str(ref) +"\" not in dict"
            continue

        # to keep things simple we ignore multiply mapped reads and reads
        # called as indels
        if read not in BASES: 
            if read in [",", "."]: # matching reads
                conf_mat[ref][ref]+=1
                continue
            elif read[0] in [",","."]:
                conf_mat[ref][ref]+=1
                if read[1] == '+':
                    if read[3].isdigit():
                        gap_size = int(read[2:3])
                        gap_start = 4
                    else:
                        gap_size = int(read[2])
                        gap_start = 3
                    for i in range(gap_start,gap_start+gap_size):
                        print "gap, read: %s"%read
                        conf_mat["gap"][read[i]]+=1
                if read[1] == '-':
                    if read[3].isdigit():
                        gap_size = int(read[2:3])
                        gap_start = 4
                    else:
                        gap_size = int(read[2])
                        gap_start = 3
                    for i in range(gap_start,gap_start+gap_size):
                        print "gap, read: %s"%read
                        conf_mat[read[i]]["gap"]+=1
                continue
        else:
            conf_mat[ref][read]+=1
    print str(conf_mat)


if __name__ == "__main__":
    main(sys.argv)
