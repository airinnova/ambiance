#!/usr/bin/env bash

make_list="$@"

if [[ "$make_list" == "" ]]; then
    echo "W: Format not specified. Using HTML."
    make_list="html"
fi

while true; do
    make clean

    for format in $make_list; do
        make $format
    done

    read -p "Press enter to recompile..."
done
