import os
import datetime

now = datetime.datetime.now()
tail = now.strftime("%Y-%m-%d")

try:
    os.mkdir("temp_info")
    if not(os.path.isfile("count_prices.txt")):
        with open("count_info.txt", "w") as count:
            count.write("0")
except Exception as e:
    print "File exists"+str(e)