#!/bin/sh

BLDROOT="$1"
INFODIR="$2"
PKG_NAME="$3"

[ ! -d ${BLDROOT}/${INFODIR} ] && exit 0

for info in `ls ${BLDROOT}/${INFODIR}/*.info*`
do
	ifile=`basename $info`
	echo ${ifile} >> ${BLDROOT}/${INFODIR}/${PKG_NAME}.ilist
done
