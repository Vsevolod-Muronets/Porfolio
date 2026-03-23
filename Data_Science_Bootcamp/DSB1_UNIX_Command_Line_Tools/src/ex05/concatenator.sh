#!/bin/bash

output="joint_dates.csv"

is_first=true
for file in ./*.csv; do
  if [ $is_first == true ]; then
    cat $file > $output
    is_first=false
  else
    tail -n +2 $file >> $output
  fi
done

(head -n 1 $output && tail -n +2 $output | sort -t, -k2,2 -k1,1) > reserve.csv && mv reserve.csv $output

if cmp -s $output ../ex03/hh_positions.csv
then
	echo "Great! Concatenated file and file in Ex03 are identical!"
else
	echo "Result is different from file in Ex03. Something went wrong"
fi

