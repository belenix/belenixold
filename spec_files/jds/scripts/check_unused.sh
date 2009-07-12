#!/bin/sh

# $Id: check_unused.sh 10701 2007-02-28 23:28:48Z laca $
#
# Search for files in cvs that are not referenced in spec files.
# Depending on command line switch, script searches for:
#  - patches not referenced in any spec file
#  - ext-sources not referenced in any spec file
#  - Linux spec files not mentioned in any Solaris spec file.
#


# Display usage if no arguments on command line.
if [ $# -eq 0 ]
then
  cat << END_OF_USAGE
Usage: `basename $0` [-patches|-ext-sources|-linux-only]

-patches     list patches not referenced in any spec file.
-ext-sources list ext-sources files not referenced in any spec file
-linux-only  list Linux spec files not mentioned in any Solaris spec file.
END_OF_USAGE
  exit 1
fi


# Determine the script directory.
ScriptDir=`dirname $0`    # Get potentially relative script directory.
ScriptDir=`( cd $ScriptDir; pwd )`  # Get absolute directory.

# Go to the spec-files directory and ensure other dirs present.
cd $ScriptDir/..
if [ ! -d patches -o ! -d base-specs -o ! -d closed -o ! -d ext-sources ]
then
  echo "ERROR: Expected directory structure not present. Contact gnome-re@sun.com."
  exit 1
fi


case "$1" in
  # Search for '^Patch.*' in Solaris, base and closed spec files.
  -patches|-p*)
      for d in patches
      do
        for f in `cd $d; ls *.diff`
        do
          found=`grep "^Patch.*$f" *.spec base-specs/*.spec closed/*.spec`
          if [ -z "$found" ]
          then
            echo $d/$f
          fi
        done
      done ;;

  # Search '^Source' in all spec files, '^SUNW_Copyright' in Solaris spec
  # files and then '^%.class' (rclass and iclass) in Solaris spec files.
  -ext-sources|-e*)
      for f in `cd ext-sources; ls`
      do
        if [ -f ext-sources/$f ]
        then
          found=`grep "^Source.*$f" *.spec base-specs/*.spec closed/*.spec`
          if [ -z "$found" ]
          then
            found=`grep "^SUNW_Copyright.*$f" *.spec closed/*.spec`
            if [ -z "$found" ]
            then
              found=`grep "^%.class.*$f" *.spec closed/*.spec`
              if [ -z "$found" ]
              then
                echo $f
              fi
            fi
          fi
        fi
      done ;;

  # Search for '^%use.*' in Solaris spec files.
  -linux-only|-l*)
      for f in *.spec
      do
        found=`grep "^%use.*$f" *.spec closed/*.spec`
        if [ -z "$found" ]
        then
          echo $f
        fi
      done ;;
esac

