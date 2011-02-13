#!/bin/sh

infodir="${1}"

PATH=/usr/bin:/usr/sfw/bin; export PATH
for info in `cat "${infodir}/${2}.ilist"`
do
  install-info --quiet --info-dir="${infodir}" "${infodir}/$info"
done

