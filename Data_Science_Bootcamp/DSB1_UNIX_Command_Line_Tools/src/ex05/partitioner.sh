#!/bin/bash

file=../ex03/hh_positions.csv
first_col=$(head -n 1 $file)
dates=$(awk -F, 'NR > 1 {print $2}' $file | cut -d'T' -f1 | cut -d'"' -f2 | sort | uniq)

for date in $dates; do
  dated_file=${date}.csv
  echo "$first_col" > $dated_file
  awk -F, -v date="$date" 'NR > 1 && $2 ~ date {print $0}' $file >> $dated_file
done
