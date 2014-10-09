#!/bin/sh
# Download source files from the internet 

for s in `egrep '^Source[0-9]+' *.spec | awk '{print $2}'`
do
  wget --no-check-certificate $s
done


