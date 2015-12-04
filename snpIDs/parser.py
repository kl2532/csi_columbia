rsids = open("RSRsample2.txt")
ssids = open("venterssidMatches2.txt")
geno = open("sample2geno.txt")

rsids = [line.strip() for line in rsids.readlines()]
ssids = [(line.strip())[2:] for line in ssids.readlines()]
geno = [line.strip() for line in geno.readlines()]

rsids = [rsid for rsid in rsids if rsid.split()[1] in ssids]
rsidonly = [rsid.split()[0] for rsid in rsids]
geno = [gen for gen in geno if (gen.split()[0])[2:] in rsidonly]

output = []

for line in geno :
	rsid = line.split()[0]
	ssid = [ssid.split()[1] for ssid in rsids if ssid.split()[0] == rsid[2:]]
	ssid = ssid[0]
	output.append("ss" + ssid + "\t" + line.split()[1])

for ssid in output :
	print ssid