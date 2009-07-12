#!/bin/bash

if [ -z $1 ]; then
    echo "usage: $0 <specfile1> [specfile2 ...]"
    exit 1
fi

export http_proxy="webcache.uk.sun.com:8080"
export ftp_proxy=${http_proxy}
PULL_NEW_TARBALLS=1

while [ $# -ne 0 ]
do
    specfile=$1

    if [ -f $specfile ]; then
        NAME=$(grep "^Name:" $specfile | sed -e "s/Name: *//" )
        NAME=$( echo $NAME )    # Gets rid of spaces and tabs that sed didn't.
        CURRENT=$(grep "^Version:" $specfile | sed -e "s/Version:[\t ]*//")
        CURRENT=$( echo $CURRENT )
        SOURCE=$(grep "^Source:" $specfile | sed -e "s/Source:[\t ]*//")
        SOURCE=$( echo $SOURCE )
        # Replace '%{Name}' with $NAME.
        SOURCE=$(echo $SOURCE | sed -e "s/\%{*[Nn]ame}*/${NAME}/g")
        #SOURCE=$(echo $SOURCE | sed -e "s/\%{*[Vv]ersion}*/${CURRENT}/g")
        SOURCEDIR=$(dirname $SOURCE)
        # Substitute '%version' if present in directory.
        SOURCEDIR=$(echo $SOURCEDIR | sed -e "s/\%{*[Vv]ersion}*/${CURRENT}/g")
    
        proto=$(echo $SOURCEDIR | cut -d ":" -f 1)
        if [ $proto != "http" -a $proto != "ftp" ]; then
            echo "Not fetching latest version for $NAME - can't use \"$SOURCEDIR\""
        else
	    LATEST=$(wget $SOURCEDIR -O - 2>/dev/null | grep "LATEST-IS" | sed -e "s/.*LATEST-IS-\([0-9][0-9\.]*\).*/\1/")
	    if [ -z $LATEST ]; then
	        echo "Cannot get latest version of $NAME from \"$SOURCEDIR/LATEST-IS*\""
	    else
	        if [ $LATEST = $CURRENT ]; then
                    echo "Okay with $NAME-$LATEST"
	        else if [ -z $PULL_NEW_TARBALLS ]; then
                         echo "Need to update to $NAME-$LATEST from $CURRENT"
	             else
# TODO: It may not be bz2!
# TODO: Use original $SOURCE with %{Version} replaced.
                         SOURCE=$(echo $SOURCE | sed -e "s/\%{*[Vv]ersion}*/${LATEST}/g")
                         wget -nv --no-clobber $SOURCE
                         if [ $? -eq 0 ]; then
                             echo "Update $specfile to $LATEST"
                         fi
	             fi
                fi 
            fi
	fi
    else
        echo "WARNING: $specfile does not exist."
    fi

    shift
done

