#!/bin/bash

for f in ./*.html
do
 echo "$f: " `cat $f | ../detect.py`
 # do something on $f
done
