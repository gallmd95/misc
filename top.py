import csv
import os
import json
import numpy as np

f = []

d = "/Users/mgallagher/Downloads"
infodir = "data_info"

for (dirpath, dirnames, filenames) in os.walk(d):
    f.extend(filenames)
    break

top = []
for each in f:
    if len(each) == 45:
        top.append(each)

a = []
for each in top:
    with open(d+"/"+each) as f:
        temp = [{k: str(v) for k, v in row.items()} for row in csv.DictReader(f, skipinitialspace=True)]
        for i in temp:
            i["date"] = each
        a = a + temp
sym = {}

k = a[0].keys()

for each in a:
    if None not in each.keys():
        sym[each[k[4]]] = {}

def optoval(op):
    if op == "Hold":
        return 0
    if "Sell" in op:
        return -1*int(op.split()[0].strip('%'))
    else:
        return int(op.split()[0].strip('%'))


for each in a:
    if None not in each.keys() and each['Last Week'] != 'None':
        val = optoval(each['Last Week'])
        val = val + optoval(each['Last Month'])
        val = val + optoval(each['Opinion'])
        val = val + optoval(each['Previous'])
        if not("price" in sym[each[k[4]]].keys()):
            sym[each[k[4]]]["price"] = 0
        sym[each[k[4]]]["price"] = sym[each[k[4]]]["price"]+val
for each in sym.keys():
    if 'Downloaded' in each:
        sym.pop(each)
    else:
        sym[each]['price'] = sym[each]['price'] /49
        sym[each]['price'] = sym[each]['price']/4

infofilenames=[]
f=[]
for (dirpath, dirnames, filenames) in os.walk(infodir):
    f.extend(dirnames)
    break
for (dirpath, dirnames, filenames) in os.walk(infodir+'/'+f[0]):
    infofilenames.extend(filenames)
    break

for i,each in enumerate(infofilenames):
    infofilenames[i] = infodir+'/'+f[0] +'/'+each



for each in infofilenames:
    try:
        data = {}
        stock = each.split('_')[3].upper()
        with open(each) as jsondata:
            data = json.load(jsondata)
        summary = data["summaryProfile"]["longBusinessSummary"]
        cash = data["financialData"]["totalDebt"]["raw"]
        debt = data["financialData"]["totalDebt"]["raw"]
        sym[stock]["cash"] = cash
        sym[stock]["debt"] = debt
        sym[stock]["summary"] = summary
        
    except KeyError, e:
        print 'I got a KeyError for '+ each +'- reason "%s"' % str(e)
    except TypeError, e:
        print 'I got a TypeError for '+ each +'- reason "%s"' % str(e)

for each in sym.keys():
    if not("summary" in sym[each].keys()):
        sym.pop(each)

print [sym[each]["price"] for each in sym.keys() if "tech" in sym[each]["summary"]]
for each in sym.keys():
    if not("cash" in sym[each].keys() and "debt" in sym[each].keys()):
        sym.pop(each)




