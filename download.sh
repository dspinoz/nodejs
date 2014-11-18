#!/bin/sh
# Download source files from the internet 

mkdir ./SOURCES

for s in `egrep '^Source[0-9]+' *.spec | awk '{print $2}'`
do
  out=`basename $s`
  wget --continue --no-check-certificate --output-document=./SOURCES/$out $s
done


