#!/bin/bash

jun_counter=0
mid_counter=0
sen_counter=0

for i in {2..21}
do
	LINE=$(head -n $i ../ex03/hh_positions.csv | tail -n 1)
	NUMB=$(echo "$LINE" | grep -cie Junior -e Middle -e Senior)
	if [ $NUMB -gt 0 ]; then
		if [ $(echo "$LINE" | grep -ci Junior) -gt 0 ]; then
			(( jun_counter++ ))
		fi
		if [ $(echo "$LINE" | grep -ci Middle) -gt 0 ]; then
			(( mid_counter++ ))
		fi
		if [ $(echo "$LINE" | grep -ci Senior) -gt 0 ]; then
                        (( sen_counter++ ))
                fi
	fi	
done

echo "\"name\",\"count\"" > hh_uniq_positions.csv
if [ $jun_counter -gt 0 ]; then
	echo "\"Junior\",$jun_counter" >> hh_uniq_positions.csv
fi
if [ $mid_counter -gt 0 ]; then
        echo "\"Middle\",$mid_counter" >> hh_uniq_positions.csv
fi
if [ $sen_counter -gt 0 ]; then
        echo "\"Senior\",$sen_counter" >> hh_uniq_positions.csv
fi

(head -n 1 hh_uniq_positions.csv && tail -n +2 hh_uniq_positions.csv | sort -t, -k2,2 -n -r) > reserve.csv && mv reserve.csv hh_uniq_positions.csv
