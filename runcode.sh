#!/bin/bash
for entry in $(ls -d */):
do
	echo $entry
	/bin/cp input.hnb $entry
	cd $entry
	#/home/lyx/bin/stream2.pl stream2.in > M0.in
	/home/lyx/bin/hndrag input.hnb
	cd ..
done

