#!/usr/bin/env bash

for year in `seq 2006 2016`;
do
    for month in `seq 1 12`;
    do
        file_name="On_Time_On_Time_Performance_${year}_${month}.zip"
        if [ ! -f "$file_name" ]; then
            wget "http://tsdata.bts.gov/PREZIP/$file_name"
        fi
    done
done
