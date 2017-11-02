import requests
import csv
from itertools import product
from string import ascii_lowercase
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
import time
start_time = time.time()

pool = ThreadPool(8) 

def req(x):
    ur = "https://finance.yahoo.com/quote/"+x
    print ur
    try:
        r = requests.get(ur)
        if r.status_code != 404 and r.text[:6] != "Moved ":
            return r
    except requests.exceptions.ContentDecodingError:
        print x
    


syms = (''.join(i) for i in product(ascii_lowercase, repeat=2))

a = pool.map(req,syms)
pool.close() 
pool.join() 
print "Swim time over!"

with open("symbols2.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(a)

print("--- %s seconds ---" % (time.time() - start_time))
