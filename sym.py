import csv
companyfiles = []
for i in xrange(28):
    p = ""
    if i == 0:
        p = "/Users/mgallagher/Downloads/companylist.csv"
    else:
        p = "/Users/mgallagher/Downloads/companylist ("+str(i)+").csv"
    f = open(p, "rb")
    reader = csv.reader(f)
    temp = list(reader)
    for each in temp:
        companyfiles.append(each)

companies = {}

for each in companyfiles[1:]:
    temp = each[0]
    companies[temp]={}
    for i,x in enumerate(each[1:]):
        companies[temp][companyfiles[0][1:][i]]=x

print companies.keys()

