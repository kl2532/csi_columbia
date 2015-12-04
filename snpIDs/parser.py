rsids = open("variants_from_sample.vcf")

output = []

for line in rsids.readlines() :
	if line.startswith("#") :
		pass
	else :
		rsid = line.split()[2]
		output.append(rsid)

for rsid in output :
	print rsid