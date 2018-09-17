#!/bin/bash
for entry in $(ls -d */)
do
	echo $entry
	#/bin/cp input.hnb $entry
	/bin/cp user.in $entry
	/bin/cp M.in $entry
	/bin/cp stream.in $entry
	#cd $entry
	#/home/lyx/bin/stream2.pl stream2.in > M0.in
	#/home/lyx/bin/hndrag input.hnb
	#cd -
done

hndragM *

