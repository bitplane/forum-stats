#!/bin/bash

read site

while [ 1 ]
do
    echo $site = `./testSite.sh $site`
    echo Enter next site or CTRL+C to exit
    read site
done
