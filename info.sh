#!/bin/sh
python start_info.py
while (( $(date +%H) < 17 )) ; do
    python info.py
done
python finish_info.py