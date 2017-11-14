#!/bin/sh
python start_prices.py
while (( $(date +%H) < 20 )) ; do
    python prices.py
done
python finish_prices.py
