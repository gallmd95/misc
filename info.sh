#!/bin/sh
python start_info.py
while (( $(date +%H) < 21 )) ; do
    python info.py
done
python finish_info.py