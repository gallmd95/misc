import requests
import csv
from itertools import product
from string import ascii_lowercase
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
import time

n = 4

start_time = time.time()

pool = ThreadPool(8) 


def req(x):
    ur = "https://finance.yahoo.com/quote/"+x
    print ur
    try:
        r = requests.get(ur,allow_redirects=False)
        if r.status_code != 404 and r.text[:6] != "Moved ":
            return x
    except requests.exceptions.HTTPError as errh:
        print "Http Error:",errh," ",x
    except requests.exceptions.ConnectionError as errc:
        print "Error Connecting:",errc," ",x
    except requests.exceptions.Timeout as errt:
        print "Timeout Error:",errt," ",x
    except requests.exceptions.RequestException as e:
        print "Req ",e," ",x
    
    

syms = (''.join(i) for i in product(ascii_lowercase, repeat=n))
a = []
try:
    a = pool.map(req,syms)
finally:
    pool.close() 
    pool.join() 
    print "Swim time over!"
    print len(a)
    f = open('symbols'+str(n)+'.txt', 'wb')
    for item in a:
        if item is not None:
            f.write("%s\n" % item)
    print("--- %s seconds ---" % (time.time() - start_time))
