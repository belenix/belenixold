#!/bin/sh

CFLAGS="-Wall -g"

gcc $CFLAGS -c vesamode.c
gcc $CFLAGS -c vbe.c
gcc $CFLAGS -c ddcxinfo-belenix.c
gcc $CFLAGS -c parse-edid.c

gcc -o ddcxinfo-belenix vesamode.o vbe.o ddcxinfo-belenix.o parse-edid.o -lpicl

if [ "$1" = "-pkg" ]
then
	pkgmk -o -d ./ -a i386
	chmod -R a+r FSWddcxinfo
	chmod 555 FSWddcxinfo
fi

if [ "$1" = "-clean" ]
then
	rm *.o
	rm ddcxinfo-belenix
	chmod -R a+rw FSWddcxinfo 2> /dev/null
	rm -rf FSWddcxinfo 2> /dev/null
fi
