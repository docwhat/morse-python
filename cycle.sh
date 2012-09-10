#!/bin/sh

#  Use this to run morse in the background all day...
#
#  requires osdlib for onscreen display.

set -e

while true; do
    nice ./rndwords.py -a -c -n1 -g -h | \
        osd_cat -c 'lightblue2' -d 10 -o 50 -b -f '-jmk-neep-medium-r-normal-*-24-*-*-*-c-*-iso8859-1'
done
