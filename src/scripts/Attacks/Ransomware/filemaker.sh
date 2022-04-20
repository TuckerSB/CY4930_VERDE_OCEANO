#!/bin/bash

for i in {1..100}; do
    if (($i % 2));
    then echo "important data" > $RANDOM.xlsx
    else echo "important data" > $RANDOM.pdf
fi
done;