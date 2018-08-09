#!/bin/bash
for entry in $(ls -d */):
do	
	echo $entry
	entry_name=${entry%\/}
	/bin/cp $entry_name/movie.mp4 ./Movies/$entry_name.mp4
done
