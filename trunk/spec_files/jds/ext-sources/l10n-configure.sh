#!/bin/sh
#
# This script modifies configure.in, .po files, po/Makefile.in.in and so on
# to configure l10n for Sun platforms. '--help' option shows the usage.
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License, Version 1.0 only
# (the "License").  You may not use this file except in compliance
# with the License.
#
# You can obtain a copy of the license at usr/src/OPENSOLARIS.LICENSE
# or http://www.opensolaris.org/os/licensing.
# See the License for the specific language governing permissions
# and limitations under the License.
#
# When distributing Covered Code, include this CDDL HEADER in each
# file and include the License file at usr/src/OPENSOLARIS.LICENSE.
# If applicable, add the following below this CDDL HEADER, with the
# fields enclosed by brackets "[]" replaced with your own identifying
# information: Portions Copyright [yyyy] [name of copyright owner]
#
# CDDL HEADER END
#
#
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#

PROGNAME=`basename $0`
PROG_VERSION=1.1
SUN_ALL_LINGUAS="cs de es fr hu it ja ko pl pt_BR ru sv zh_CN zh_HK zh_TW"
ENABLE_COPYRIGHT=0
ENABLE_SUN_ALL_LINGUAS=0
DISABLE_GNU_EXTENSIONS=0
L10N_POTFILES=${L10N_POTFILES:-"no"}
CONFIGURE=
SED=/usr/xpg4/bin/sed

usage () {
  printf "This script modify ALL_LINGUAS parameter in configure.in file.              \n"
  printf "\n"
  printf "usage: $PROGNAME Version $PROG_VERSION [OPTION...]                                   \n"
  printf "  -c, --enable-copyright            Modify po/Makefile.in.in and gnome-doc-utils.make\n"
  printf "                                    so that the copyright information is installed\n"
  printf "                                    from .po files. intltoolize and\n"
  printf "                                    gnome-doc-prepare need to be run before\n"
  printf "                                    this script is run if you run them.\n"
  printf "  -l, --enable-sun-linguas          Modify ALL_LINGUAS for Sun translations.\n"
  printf "  -p, --enable-pot                  Generate .pot file for internal.        \n"
  printf "  -x, --disable-gnu-extensions      Remove GNU extensions in po/*.po files. \n"
  printf "  -h, --help                        Show this message.                      \n"
  printf "  -V, --version                     Show version.                           \n"
}

check_args_solgetopts ()
{
  while [ $# -gt 0 ]
  do
    case "$1" in
    -c|--enable-copyright)
      ENABLE_COPYRIGHT=1;;
    -h|--help|--usage)
      usage
      exit 0;;
    -l|--enable-sun-linguas)
      ENABLE_SUN_ALL_LINGUAS=1;;
    -p|--enable-pot)
      L10N_POTFILES="yes";;
    -V|--version)
      echo $PROG_VERSION;
      exit 0;;
    -x|--disable-gnu-extensions)
      DISABLE_GNU_EXTENSIONS=1;;
    *)
      echo "$PROGNAME: processing error: $1" 1>&2
      exit 1;;
    esac
    shift
  done
}

init () {
  # GNU SUNWgnugetopt is not installed on Solaris.
  check_args_solgetopts $@

  if [ -f configure.in ] ; then
    CONFIGURE=configure.in
  elif [ -f configure.ac ] ; then
    CONFIGURE=configure.ac
  fi
}

pre_check () {
  if [ "$CONFIGURE" = "" -a $ENABLE_SUN_ALL_LINGUAS -eq 1 ] ; then
    echo "#### Not Found configure.in"
    exit 0
  fi

  if [ ! -d po ] ; then
    echo "#### Not Found po dir"
    exit 0
  fi
}

configure_copyright ()
{
  DQ='"'
  DL='$'
  GA='`'
  BS='\\\'

  if [ -f .sun-l10n-copyright ] ; then
    return 0;
  fi

  if [ -f po/Makefile.in.in ] ; then
    sed -e "/^install-data-yes: all/a\\
	mkdir_p=$DL(mkdir_p); $BS
	mkdir_p=$DL${DL}{mkdir_p:-${DQ}mkdir -p$DQ}; $BS
	itlocaledir=$DL(itlocaledir); $BS
	itlocaledir=$DL${DL}{itlocaledir:-${DL}(gnulocaledir)}; $BS
	itlocaledir=$DL${DL}{itlocaledir:-${DL}(localedir)}; $BS
	GETTEXT_PACKAGE=$DL(GETTEXT_PACKAGE); $BS
	GETTEXT_PACKAGE=$DL${DL}{GETTEXT_PACKAGE:-${DL}(DOMAIN)}; $BS
	$DL${DL}mkdir_p $DL(DESTDIR)$DL${DL}itlocaledir; $BS
	catalogs=$DQ$DL(CATALOGS)$DQ; $BS
	for cat in $DL${DL}catalogs; do $BS
	  cat=${GA}basename $DL${DL}cat$GA; $BS
	  lang=${GA}echo $DL${DL}cat | sed -e 's/${BS}.gmo$DL${DL}//'$GA; $BS
	  dir=$DL(DESTDIR)$DL${DL}itlocaledir/$DL${DL}lang/LC_MESSAGES; $BS
	  $DL${DL}mkdir_p $DL${DL}dir; $BS
	  echo ${DQ}Copyright for $DL${DL}{GETTEXT_PACKAGE}.mo$DQ > $DL${DL}dir/$DL${DL}{GETTEXT_PACKAGE}.ui.copyright; $BS
	  cat $DL${DL}lang.po | while read line; $BS
	  do $BS
	    is_comment=${GA}echo $DL${DL}line | grep '^#' | grep -v '^#,'$GA; $BS
	    if [ x$DQ$DL${DL}is_comment$DQ = x ] ; then $BS
	      break; $BS
	    fi; $BS
	    echo $DQ$DL${DL}line$DQ | sed -e ${DQ}s/^#$BS(.*$BS)/ ${BS}1/$DQ >> $DL${DL}dir/$DL${DL}{GETTEXT_PACKAGE}.ui.copyright; $BS
	  done; $BS
	  echo ${DQ}-------------------------------------------------------------$DQ $BS
	    >> $DL${DL}dir/$DL${DL}{GETTEXT_PACKAGE}.ui.copyright; $BS
	  echo $DQ$DQ >> $DL${DL}dir/$DL${DL}{GETTEXT_PACKAGE}.ui.copyright; $BS
	  echo ${DQ}installing $DL${DL}{GETTEXT_PACKAGE}.ui.copyright in $DL${DL}dir$DQ; $BS
	done" po/Makefile.in.in >> po/Makefile.in.in.$$
    mv po/Makefile.in.in.$$ po/Makefile.in.in
  fi

  if [ -f gnome-doc-utils.make ] ; then
    sed -e "/^install-doc-docs:/a\\
	@for lc in $DL(_DOC_REAL_LINGUAS); do ${BS}
	  echo $DQ$DL(mkinstalldirs) $DL(DESTDIR)$DL(HELP_DIR)/$DL(DOC_MODULE)/$DL${DL}lc$DQ; ${BS}
	  $DL(mkinstalldirs) $DL(DESTDIR)$DL(HELP_DIR)/$DL(DOC_MODULE)/$DL${DL}lc; ${BS}
	  if test -d $DQ$DL${DL}lc$DQ; then d=; else d=$DQ$DL(srcdir)/$DQ; fi; ${BS}
	  if [ -f $DL${DL}d$DL${DL}lc/$DL${DL}lc.po ] ; then ${BS}
	    echo ${DQ}Copyright for $DL(DOC_MODULE)$DQ >> $DL(DESTDIR)/$DL(HELP_DIR)/$DL(DOC_MODULE)/$DL${DL}lc/$DL(DOC_MODULE).help.copyright; ${BS}
	    cat $DL${DL}d$DL${DL}lc/$DL${DL}lc.po | while read line; ${BS}
	    do ${BS}
	      is_comment=${GA}echo $DL${DL}line | grep '^#' | grep -v '^#,'$GA; ${BS}
	      if [ x$DQ$DL${DL}is_comment$DQ = x ] ; then ${BS}
	        break; ${BS}
	      fi; ${BS}
	      echo $DQ$DL${DL}line$DQ | sed -e ${DQ}s/^#$BS(.*$BS)/ ${BS}1/$DQ >> $DL(DESTDIR)/$DL(HELP_DIR)/$DL(DOC_MODULE)/$DL${DL}lc/$DL(DOC_MODULE).help.copyright; ${BS}
	    done; ${BS}
	    echo ${DQ}-------------------------------------------------------------$DQ ${BS}
	      >> $DL(DESTDIR)/$DL(HELP_DIR)/$DL(DOC_MODULE)/$DL${DL}lc/$DL(DOC_MODULE).help.copyright; ${BS}
	    echo $DQ$DQ >> $DL(DESTDIR)/$DL(HELP_DIR)/$DL(DOC_MODULE)/$DL${DL}lc/$DL(DOC_MODULE).help.copyright; ${BS}
	    echo ${DQ}installing $DL(DOC_MODULE).help.copyright in $DL(DESTDIR)/$DL(HELP_DIR)/$DL(DOC_MODULE)/$DL${DL}lc$DQ; ${BS}
	  fi; ${BS}
	done" gnome-doc-utils.make > gnome-doc-utils.make.$$
    mv gnome-doc-utils.make.$$ gnome-doc-utils.make
  fi

  touch .sun-l10n-copyright
  return 0
}


# GNU .po has several GNU extensions.
# http://www.gnu.org/software/libc/manual/html_node/Formatting-Calendar-Time.html
# http://gcc.gnu.org/ml/gcc-patches/2000-08/msg00881.html
disable_gnu_extensions () {
  cd po

  # Replace "%-m" with "%m" for strftime(3C).
  # Replace "%Id" with "%d" for printf(3C) and don't use "." for the workaround 
  # Replace "%l" with "%I" for strptime(3C) and also grep %M for the workaround 
  # so that we do not change %ld for printf(3C).
  # Replace "%k" with "%H" for strptime(3C).
  for po in `egrep -l \
'^msgstr ".*%[_0^-][md].*"|'\
'^msgstr "%I[doxXnfFeEgGaAcspCSm]"|'\
'^msgstr ".*%[_0^-]*l.*%[MpP].*"|'\
'^msgstr ".*%[MpP].*%[_0^-]*l.*"|'\
'^msgstr ".*%[_0^-]*k.*"'\
  *.po`
  do
    env LANG=C LC_ALL=C \
      $SED -e '/^msgstr "/s/%[_0^-]\([md]\)/%\1/g' $po     |
    env LANG=C LC_ALL=C \
      $SED -e 's/^\(msgstr "%\)I\([doxXnfFeEgGaAcspCSm]"\)/\1\2/g' |
    env LANG=C LC_ALL=C \
      $SED -e '/^msgstr ".*%[_0^-]*l.*%[MpP]/s/%[_0^-]*l/%I/g' |
    env LANG=C LC_ALL=C \
      $SED -e '/^msgstr ".*%[MpP].*%[_0^-]*l/s/%[_0^-]*l/%I/g' |
    env LANG=C LC_ALL=C \
      $SED -e '/^msgstr "/s/%[_0^-]*k/%H/g'                > $po.$$
    mv $po.$$ $po
  done

  # Replace "%Id" with "%d" for printf(3C) forcibly for RTL languages only.
  for po in `egrep -l \
'%I[doxXnfFeEgGaAcspCSm][^a-zA-Z]'\
  ar.po az.po fa.po he.po ur.po yi.po`
  do
    env LANG=C LC_ALL=C \
      $SED -e 's/\(%\)I\([doxXnfFeEgGaAcspCSm][^a-zA-Z]\)/\1\2/g' $po > $po.$$
    mv $po.$$ $po
  done

  cd ..
}

apply_sun_all_linguas_file () {
  PO_LINGUAS=`cat po/LINGUAS | grep -v "^#"`
  PO_LINGUAS=`echo "$PO_LINGUAS $SUN_ALL_LINGUAS"\
    | tr " " "\n" \
    | env LC_ALL=C LANG=C sort \
    | uniq \
    | tr "\n" " "`

  SAVE_COMMENT=`grep "^#" po/LINGUAS`
  echo "$SAVE_COMMENT"    >   po/LINGUAS
  echo "$PO_LINGUAS"      >>  po/LINGUAS
}

apply_sun_all_linguas_configure () {
  ALL_LINGUAS=`grep '^ALL_LINGUAS=' $CONFIGURE \
    | $SED -e 's/ALL_LINGUAS=//' -e 's/"//g'`
  ALL_LINGUAS=`echo "${ALL_LINGUAS} ${SUN_ALL_LINGUAS}"\
    | tr " " "\n" \
    | sort \
    | uniq \
    | tr "\n" " "`
  
  DQ='"'
  $SED -e "/^ALL_LINGUAS=/s/^\(ALL_LINGUAS=\)\(.*\)/\1$DQ${ALL_LINGUAS}$DQ/" \
    $CONFIGURE > ${CONFIGURE}.chg
  mv ${CONFIGURE}.chg $CONFIGURE
}

apply_sun_all_linguas () {
  if [ -f po/LINGUAS ] ; then
    apply_sun_all_linguas_file
  else
    apply_sun_all_linguas_configure
  fi
}

update_po () {
  PO_DIRS=po*/POTFILES.in
  PO_DIRS=`echo $PO_DIRS | $SED -e 's|/POTFILES.in||g'`
  
  for po in $PO_DIRS
  do
#
# This is needed to avoid build errors.
#
    (cd $po; touch `echo "$SUN_ALL_LINGUAS" | $SED -e 's/\([a-z_A-Z][a-z_A-Z]*\)/\1.po/g'`)
  done
}
  
update_pot () {
  OS=`uname -s`
  if [ "$OS" = Linux ] ; then
    TOPDIR=/usr/src/packages
  else
    TOPDIR=/jds/packages
  fi
  POT_DATA='"POT-Creation-Date: '

  cd po
  rm -f *.pot
  echo "[encoding: UTF-8]" > POTFILES.in
  intltool-update --maintain 2>/dev/null
  cat missing >> POTFILES.in
  intltool-update --pot
  POT=`ls *.pot`
  if [ "x$POT" != "x" ] ; then
    $SED -e "/^$POT_DATA/d" $POT > ${POT}.$$
    mv ${POT}.$$ $POT
    mkdir -p $TOPDIR/l10n/pot
    mkdir -p $TOPDIR/l10n/diff
    mkdir -p $TOPDIR/l10n/new
    if [ -f $TOPDIR/l10n/pot/$POT ] ; then
      diff $TOPDIR/l10n/pot/$POT $POT > ${POT}.diff
      if [ -s ${POT}.diff ] ; then
        cp ${POT}.diff $TOPDIR/l10n/diff
        echo "#### Translation should be updated!!!"
      fi
    else
      cp $POT $TOPDIR/l10n/pot
      cp $POT $TOPDIR/l10n/new
    fi
  else
    echo "#### Failed to create the potfile in `pwd`"
  fi
  cd ..
}

main () {
  init $@
  pre_check

  if [ $DISABLE_GNU_EXTENSIONS -eq 1 ] ; then
    disable_gnu_extensions
  fi
  if [ $ENABLE_SUN_ALL_LINGUAS -eq 1 ] ; then
    apply_sun_all_linguas
    update_po
  fi
  if [ $ENABLE_COPYRIGHT -eq 1 ] ; then
    configure_copyright
  fi
  if [ "x$L10N_POTFILES" = "xyes" ] ; then
    update_pot
  fi
}

main $@
