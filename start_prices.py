import os
import datetime

now = datetime.datetime.now()
tail = now.strftime("%Y-%m-%d")

try:
    os.mkdir("temp_prices")
    if not(os.path.isfile("count_prices.txt")):
        with open("count_prices.txt", "w") as count:
            count.write("0")
    open("temp_prices/prices_"+tail+".csv", 'a')
except Exception as e:
    print "File exists"+str(e)