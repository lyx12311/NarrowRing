#!/bin/bash
for entry in $(ls -d */):
do	
	echo $entry
	/bin/cp DrawPNG_polar.py $entry 
	cd $entry
	./DrawPNG_polar.py ./ 0
	cd ..
done

