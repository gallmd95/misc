import requests
import json
import csv
import os
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
import time
import datetime
import string
import random

def id_generator(size=6,chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))



now = datetime.datetime.now()

tail = now.strftime("%Y-%m-%d_%H-%M-%S")

tempid = "temp_price_"+now.strftime("%M")+id_generator()


start_time = time.time()

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

def req(x):
    ur = "https://finance.yahoo.com/quote/"+x
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0'+id_generator()
        }
        print ur
        r = requests.get(ur,allow_redirects=False, headers=headers)
        if r.status_code != 404 and r.text[:6] != "Moved ":
            if "root.App.main" in r.text and "}(this));" in r.text:
                start =r.text.index("root.App.main")+16
                end = r.text.index("}(this));")-start
                t = r.text[start:][:end].strip()[:-1]
                data = json.loads(t)["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]["financialData"]["currentPrice"]["raw"]
                print data
                return [x,data]
            else:
                print "fmt"
                return [x, "fmt"]
        else:
            print "mov"
            return [x, "Moved"]
    except requests.exceptions.HTTPError as errh:
        print "Http Error:",errh," ",x
    except requests.exceptions.ConnectionError as errc:
        print "Error Connecting:",errc," ",x
    except requests.exceptions.Timeout as errt:
        print "Timeout Error:",errt," ",x
    except requests.exceptions.RequestException as e:
        print "Req ",e," ",x
    except KeyError, e:
        print 'I got a KeyError for '+ x +'- reason "%s"' % str(e)
        return [x,"err"]
    
    
l = file_len("symbols.txt")
count = 0
with open("count.txt", "r+") as f:
    data = f.read()
    count = int(data)
    f.seek(0)
    f.write(str((count+1)%l))
    f.truncate()
symFile = open("symbols.txt")
syms = [symFile.readlines()[count].rstrip()]
a = []
try:
    a = map(req,syms)
finally:
    print "Swim time over!"        
    filetail = tail.split("_")[0]
    temp = a[0]
    temp.append(tail)
    with open('temp_prices/prices_'+filetail+'.csv', 'a') as outfile:
        writer = csv.writer(outfile)
        writer.writerow(temp)
    print("--- %s seconds ---" % (time.time() - start_time))