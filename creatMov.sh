#!/bin/bash
for entry in $(ls -d */)
do
        echo $entry
	entryname=${entry%/}
        /Users/lucy/Desktop/NarrowRings/bin/DrawPNG.py $entry 0 1
        /Users/lucy/Desktop/NarrowRings/bin/FFTRingMov.py $entry r > out_r_$entryname
	/Users/lucy/Desktop/NarrowRings/bin/FFTRingMov.py $entry z > out_z_$entryname
done
