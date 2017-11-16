#!/bin/sh
python start_prices.py
while (( $(date +%H) < 16 )) ; do
    python prices.py
done
