#!/bin/bash

# testing trapping signal

trap "echo 'Sorry! I have trapped Ctrl-C'" SIGINT SIGTERM
echo "This is test program"

count=1
while [ $count -lt 10 ]
do
    echo "Loop #$count"
    sleep 3
    count=$[ $count + 1 ]
done

echo "This is the end of test program"
