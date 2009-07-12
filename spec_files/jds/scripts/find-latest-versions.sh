#!/bin/bash

old_IFS=$IFS;
IFS=":"

for product in *.spec; do
    IFS=$old_IFS

    NAME=$(grep "^Name:" $product | sed -e "s/Name: *//" )
    NAME=$( echo $NAME )    # Gets rid of spaces and tabs that sed didn't.
    CURRENT=$(grep "^Version:" $product | sed -e "s/Version:[\t ]*//")
    SOURCE=$(grep "^Source:" $product | sed -e "s/Source:[\t ]*//")
    SOURCE=$(echo $SOURCE | sed -e "s/\%{*[Nn]ame}*/${NAME}/g")

    IS_GNOME=$(echo $SOURCE | grep GNOME) 
    if [ $IS_GNOME ]; then
        if [ $SOURCE ]; then
            LOCATION=$(dirname $SOURCE)
        fi

        echo "===== $product ====="

        proto=$(echo $LOCATION | cut -d ":" -f 1)
            if [ $proto != "http" ]; then
        	echo "Not fetching latest version for $product - can't use \"$LOCATION\""
        else
	    LATEST=$(wget $LOCATION -O - 2>/dev/null | grep "LATEST-IS" | sed -e "s/.*LATEST-IS-\([0-9][0-9\.]*\).*/\1/")
	    if [ -z $LATEST ]; then
	        echo "Cannot get latest version of $product from \"$LOCATION/LATEST-IS*\""
	    else
	        if [ $LATEST = $CURRENT ]; then
		    echo "Okay with $product-$LATEST"
	        else if [ -z $PULL_NEW_TARBALLS ]; then
		    echo "Need to update to $product-$LATEST from $CURRENT"
	        else
		    wget $LOCATION/$product-$LATEST.tar.bz2
	        fi fi
	    fi
        fi
    echo;
    fi

    IFS=":"
done

IFS=$old_IFS

