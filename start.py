import os
import datetime

now = datetime.datetime.now()
tail = now.strftime("%Y-%m-%d")


os.mkdir("temp_prices")
open("temp_prices/prices_"+tail+".csv", 'a')