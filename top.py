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
for each in f:
    temp = []
    for (dirpath, dirnames, filenames) in os.walk(infodir+'/'+each):
        temp.extend(filenames)
        break
    for i,name in enumerate(temp):
        temp[i] = infodir+'/'+each +'/'+name
    infofilenames.extend(temp)


count = 0
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

for each in sym.keys():
    if not("cash" in sym[each].keys() and "debt" in sym[each].keys()):
        sym.pop(each)

for each in sym.keys():
    print each
    print sym[each]
print len(sym.keys())

def nonlin(x,deriv=False):
    if deriv==True:
        return x*(1-x)
    return 1/(1+np.exp(-x))

x = np.array([[sym[each]["cash"]/1000000,sym[each]["debt"]/1000000] for each in sym.keys()])
y = np.array([[sym[each]["price"]] for each in sym.keys()])

np.random.seed(1)

syn0 =2*np.random.random((2,1547))-1
syn1 =2*np.random.random((1547,1))-1

for j in xrange(60000):
    
    l0 = x
    l1 = nonlin(np.dot(l0,syn0))
    l2 = nonlin(np.dot(l1,syn1))
    l2_error = y-l2
    if j%10000==0:
        print "Error"+str(np.mean(np.abs(l2_error)))
    l2_delta = l2_error*nonlin(l2,deriv=True)
    l1_error = l2_delta.dot(syn1.T)
    l1_delta = l1_error*nonlin(l1,deriv=True)
    syn1 += l1.T.dot(l2_delta)
    syn0 += l0.T.dot(l1_delta)