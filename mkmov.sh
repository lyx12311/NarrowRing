#!/bin/bash
for entry in $(ls -d */):
do	
	echo $entry
	/bin/cp DrawPNG.py $entry
	cd $entry
	./DrawPNG.py ./
	cd ..
done

