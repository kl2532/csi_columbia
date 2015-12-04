import os
import random
import sys
import re

assay = open("sample2ssids.txt")
samgeno = open("sample2geno.txt")
rsids = open("watsonrsidMatches2.txt")
geno = open("watsongeno.txt")

assay = [line.strip() for line in assay.readlines()]
rsids = [line.strip() for line in rsids.readlines()]

samgeno = [line.strip() for line in samgeno.readlines() if line.split()[0] in rsids]
geno = [line.strip() for line in geno.readlines() if line.split()[0] in rsids]
#samgeno = sorted(samgeno, key = lambda x : (x.split()[0])[2:] )
#geno = sorted(geno, key = lambda x : (x.split()[0])[2:] )

#print samgeno[1:5]
#print ""
#print geno[1:5]

#matches = set(assay).intersection(rsids)

matches = set(samgeno).intersection(geno)

#matchrs = []

#for match in matches :
#	num = ssids.index(match)
#	matchrs.append("rs" + rsids[num])

#matchrs = set(matchrs)
#for rs in matchrs :
#	print rs

#print len(matches)


for hit in matches :
	print hit