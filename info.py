import requests
import json
import zipfile
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

tail = now.strftime("%Y-%m-%d_%H-%M")

tempid = "temp_info_"+now.strftime("%M")+id_generator()



n = 4

start_time = time.time()

pool = ThreadPool(8) 

def zip(src, dst):
    zf = zipfile.ZipFile("%s.zip" % (dst), "w", zipfile.ZIP_DEFLATED)
    abs_src = os.path.abspath(src)
    for dirname, subdirs, files in os.walk(src):
        for filename in files:
            absname = os.path.abspath(os.path.join(dirname, filename))
            arcname = absname[len(abs_src) + 1:]
            print 'zipping %s as %s' % (os.path.join(dirname, filename),
                                        arcname)
            zf.write(absname, arcname)
            os.remove(absname)
    zf.close()

def req(x):
    ur = "https://finance.yahoo.com/quote/"+x
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0'
        }        
        r = requests.get(ur,allow_redirects=False, headers=headers)

        if r.status_code != 404 and r.text[:6] != "Moved ":
            if "root.App.main" in r.text and "}(this));" in r.text:
                start =r.text.index("root.App.main")+16
                end = r.text.index("}(this));")-start
                t = r.text[start:][:end].strip()[:-1]
                data = json.loads(t)["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]
                return (x,data)
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
    os.mkdir(tempid)
    a = pool.map(req,syms)
finally:
    pool.close() 
    pool.join()
    print "Swim time over!"        
    if len(a) > 0: 
        for each in a:
            if each is not None:
                with open(tempid+'/info_'+each[0]+'_'+tail+'.txt', 'w') as outfile:
                    json.dump(each[1], outfile)
    zip(tempid,"data_info/infos_"+tail)
    os.rmdir(tempid)
    print("--- %s seconds ---" % (time.time() - start_time))