import requests
import json
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
import time
import datetime


now = datetime.datetime.now()

tail = now.strftime("%Y-%m-%d_%H:%M")

n = 4

start_time = time.time()

pool = ThreadPool(8) 


def req(x):
    ur = "https://finance.yahoo.com/quote/"+x
    print ur
    try:
        r = requests.get(ur,allow_redirects=False)
        if r.status_code != 404 and r.text[:6] != "Moved " and "root.App.main" in r.text and "}(this));" in r.text:
            start =r.text.index("root.App.main")+16
            end = r.text.index("}(this));")-start
            t = r.text[start:][:end].strip()[:-1]
            data = json.loads(t)
            print data["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]
            #print json.loads(r.text[start:][:end].strip())
            return x,data
    except requests.exceptions.HTTPError as errh:
        print "Http Error:",errh," ",x
    except requests.exceptions.ConnectionError as errc:
        print "Error Connecting:",errc," ",x
    except requests.exceptions.Timeout as errt:
        print "Timeout Error:",errt," ",x
    except requests.exceptions.RequestException as e:
        print "Req ",e," ",x
    
    
symFile = open("symbols.txt")
syms = (''.join(i) for i in symFile.readlines())
a = []
try:
    a = pool.map(req,syms)
finally:
    pool.close() 
    pool.join() 
    print "Swim time over!"
    for each in a:
        if not all(each):
            with open('info_'+each[0]+'_'+tail+'.txt', 'w') as outfile:
                json.dump(each[1], outfile)
    print("--- %s seconds ---" % (time.time() - start_time))