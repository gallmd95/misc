import requests
import json
import csv
import os
import time
import datetime
import string
import random


now = datetime.datetime.now()

tail = now.strftime("%Y-%m-%d_%H-%M-%S")

start_time = time.time()

def req(x):
    ur = "https://finance.yahoo.com/quote/"+x
    try:
        headers = {
            'User-Agent': 'My User Agent 1.0'
        }
        print ur
        r = requests.get(ur,allow_redirects=False, headers=headers)
        if r.status_code != 404 and r.text[:6] != "Moved ":
            if "root.App.main" in r.text and "}(this));" in r.text:
                start =r.text.index("root.App.main")+16
                end = r.text.index("}(this));")-start
                t = r.text[start:][:end].strip()[:-1]
                data = json.loads(t)["context"]["dispatcher"]["stores"]["QuoteSummaryStore"]
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
    
    
count = 0
with open("count_info.txt", "r+") as f:
    data = f.read()
    count = int(data)
    f.seek(0)
    f.write(str((count+1)))
    f.truncate()
if not(count > 18897):
    symFile = open("symbols.txt")
    syms = symFile.readlines()[count].rstrip()
    a = []
    try:
        a = req(syms)
    finally:
        print "Swim time over!"        
        filetail = tail.split("_")[0]
        with open('temp_info/info_'+a[0]+'_'+filetail+'.txt', 'w') as outfile:
            json.dump(a[1], outfile)
        print("--- %s seconds ---" % (time.time() - start_time))
else:
    print "done"
    time.sleep(5)
    

    