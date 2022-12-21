#!/bin/bash

FILES="$1/*"
for f in $FILES
do
  echo "Processing $f file..."
  python formatChange.py $f
  # take action on each file. $f store current file name
  # perform some operation with the file
done
