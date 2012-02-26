#!/bin/bash

# Pick a random sample of 30 URLs and test them. This
# will give us some idea of how clean the data is and
# how good the detector is.

for i in `cat ./inputdata/dmoz.txt | shuf | head -30`
do
    echo $i `./testSite.sh $i` &
done

wait
