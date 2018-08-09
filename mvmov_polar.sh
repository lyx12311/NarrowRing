#!/bin/bash
for entry in $(ls -d */):
do	
	echo $entry
	entry_name=${entry%\/}
	/bin/cp $entry_name/movie_polar.mp4 ./Movies_polar/$entry_name.mp4
done
