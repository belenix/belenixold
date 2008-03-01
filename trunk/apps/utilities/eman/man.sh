#!/bin/sh
# man/nroff -	Wrapper for man(1) which does better high-lighting
#
# tim.cook@sun.com, 13 Aug 2002
#
# Modified:
#	10 Nov 2005, suggestion from "Tom" via blogs.sun.com/timc
#	- Improved LESS options
#
# Man uses (what used to be) an undocumented flag of nroff; "-u"; to
# control highlighting.  We intercept this, and use our own setting.
#
# NOTE: This man/nroff script needs to be found in PATH before the real
#	versions in /usr/bin.  Link the script to man & nroff.

case $0 in
*man )
    #-- While I am at it, use a custom PAGER for viewing man pages
    export LESS ; LESS="-Rsm -Pm--More--(?eEND:%PB\%.)"
    export PAGER ; PAGER="exec less"
    #-- Hint to nroff wrapper script
    export _NROFF_U ; _NROFF_U=1

    #-- Make sure the nroff wrapper script is found before /bin/nroff
    PATH=$HOME/bin:$PATH

    exec /usr/bin/man "$@"
    ;;
*nroff )
    if [ -n "$_NROFF_U" -a "$1,$2,$3" = "-u0,-Tlp,-man" ]; then
	shift
	exec /usr/bin/nroff -u${_NROFF_U} "$@"
    fi

    #-- Some other invocation of nroff
    exec /bin/nroff "$@"
    ;;
esac
