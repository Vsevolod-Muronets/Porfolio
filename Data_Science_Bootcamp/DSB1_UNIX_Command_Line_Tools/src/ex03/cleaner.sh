#!/bin/bash

cp ../ex02/hh_sorted.csv hh_positions.csv

for i in {2..21}
do
	LINE=$(head -n $i hh_positions.csv | tail -n 1)
	NUMB=$(echo "$LINE" | grep -cie Junior -e Middle -e Senior)
	value=""
	counter=0
	if [ $NUMB -gt 0 ]; then
		if [ $(echo "$LINE" | grep -ci Junior) -gt 0 ]; then
			value+="Junior"
			(( counter++ ))
		fi
		if [ $(echo "$LINE" | grep -ci Middle) -gt 0 ]; then
			if [ $counter -gt 0 ]; then
				value+="\/"
			fi
			value+="Middle"
			(( counter++ ))
		fi
		if [ $(echo "$LINE" | grep -ci Senior) -gt 0 ]; then
			if [ $counter -gt 0 ]; then
                                value+="\/"
                        fi
                        value+="Senior"
                        (( counter++ ))
                fi
		fin_value="\"$value"
		value=$fin_value
		value+="\""
	else 
		value+="\"-\""
	fi	
	sed -i "${i}s/^\([^,]*,[^,]*,\)\"[^\"]*[^,]*\",/\1$value,/" hh_positions.csv 
done
