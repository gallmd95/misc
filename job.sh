#!/bin/sh
python start.py
while (( $(date +%H) < 20 )) ; do
    python prices.py
done
python finish.py
