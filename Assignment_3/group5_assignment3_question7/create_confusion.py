"""Create Confusion creates a confusion matrix from a tsv of snps

"""

import sys

BASES = ['a', 'c', 't', 'g']

def initialize_confusion():
    matrix = {}
    for b_ref in BASES:
        matrix[b_ref]={}
        for b_read in BASES:
            matrix[b_ref][b_read]=0
    return matrix

def main(argv):
    # Check valid inputs given.
    if len(argv) != 2:
        sys.stderr.write("invalid usage: python create_confusion.py" +
                         " <snps.txt>\n")
        sys.exit(2)

    snps_fn = argv[1]

    snps_file = open(snps_fn)

    conf_mat = initialize_confusion()

    for l in snps_file:
        # skip the first line.
        (ref, read) = l.strip("\n").split("\t")
        if ref not in BASES:
            print "base \"" + str(ref) +"\" not in dict"
            continue
        if read not in BASES:
            if len(read) == 3 and read[:2] == "^~":
                read = read[2]
            elif len(read) == 2 and read[1] == "$":
                read = read[0]
            else:
                print "base \"" + str(read) +"\" not in dict"
                continue
        conf_mat[ref][read]+=1

    print str(conf_mat)


if __name__ == "__main__":
    main(sys.argv)
