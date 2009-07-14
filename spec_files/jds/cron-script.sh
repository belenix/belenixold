#!/bin/bash

# Sample usage in crontab:
# Run, Mon-Fri at 1:30am. Add to build user's crontab.
#   30 1 * * 1-5 . /jds/cbe/bin/env.sh; cd /jds/spec-files; I_KNOW_WHAT_IM_DOING=yes ./cron-script.sh
#
# The same with a jail. Add to root's crontab. Example assumes 'gbuild' is the
# build user
#   30 1 * * 1-5 /usr/sbin/chroot /path/to/jail/root /usr/bin/su - gbuild -c ". /jds/cbe/bin/env.sh; cd /jds/spec-files; I_KNOW_WHAT_IM_DOING=yes ./cron-script.sh"
#
# $Id: cron-script.sh 18010 2009-04-02 06:22:56Z davelam $


# Determine whether to do debug or non-debug build.
# On 'even' days of the week (Sun, Tues, Thur, Sat) to a debug build.
DEBUG_BUILD=
DEBUG_DIR=
DOW=$[ $(date +"%w") % 2 ]
#if [ $DOW -eq "0" ]; then
#  DEBUG_BUILD="--with-debug"
#  DEBUG_DIR=.dbg
#fi

OSrel=`uname -r | cut -f2 -d.`
OSarch_full=`uname -p`
if [ "x$OSarch_full" = "xsparc" ]; then
    OSarch=s
else
    OSarch_full=x86
    OSarch=x
fi

GNOME_VER="2.26"
PRODNAME="G${GNOME_VER}"

# directory to copy rpms/srpms to on the remote host
RPMSDIR=/sgnome/pkgs/gnome${GNOME_VER}/S${OSrel}${OSarch}/nightly${DEBUG_DIR}
LOCKFILE=/sgnome/pkgs/gnome${GNOME_VER}/S${OSrel}${OSarch}/.build.lock

# reply-to/to address to send the build log as/to
REPLY_TO=laszlo.peter@sun.com
EMAIL_ADDR=gnome-re@sun.com

# date format appended to the Release tag in the spec files
# (passed to the date command on the cmd line)
RELEASE_DATE_FMT="%y%m%d"

# date format used for naming the directories
DIR_DATE_FMT="%Y-%m-%d"

RELEASE_DATE=`date +$RELEASE_DATE_FMT`
DIR_DATE=`date +$DIR_DATE_FMT`

# document root of the web server
WEBROOT=/net/jdsserv.ireland/webroots/jds.ireland/htdocs

# subdir to keep logs and reports on the webserver
WEBDIR=build_reports/gnome${GNOME_VER}/nightly/S${OSrel}${OSarch}
LOGDIR=$WEBDIR/$DIR_DATE

# ------------ nothing to configure below this line --------------

if [ "x$I_KNOW_WHAT_IM_DOING" != xyes ]; then
    echo " ,---------------------------------------------------------------."
    echo "| This script is intended to be run from cron for producing      |"
    echo "| official nightly builds. It will mail responsible engineers    |"
    echo "| if any build failure occurs, sends build reports to            v"
    echo "| RE and update web pages."
    echo "|"
    echo "| Don't run it unless you know what you are doing. Thanks."
    echo "|"
    echo "| Mail gnome-re@sun.com if you need more info."
    echo "\`------>                                                         +"
    exit 1
fi

MYNAME="$0"
MYDIR=$(cd `dirname $0`; pwd)

if [ "x$1" != x ]; then
    SPECDIR="$1"
else
    SPECDIR="$MYDIR"
fi

# remove temporary files on exit
clean_up () {
  case "$MYNAME" in
  /tmp/cron-script.copy.* )
        rm -f $MYNAME
        ;;
  esac
  exit
}

trap clean_up HUP INT TERM QUIT EXIT

# make a copy of the cron script in /tmp and execute that in order to
# avoid disasters caused by cvs update.
case "$MYNAME" in
    /tmp/cron-script.copy.* )
        ;;
    *)
        cp $MYNAME /tmp/cron-script.copy.$$
        chmod 755 /tmp/cron-script.copy.$$
        cd /tmp
        exec /tmp/cron-script.copy.$$ "$MYDIR"
        ;;
esac

fatal_error () {
  echo "ERROR: $*"
  exit 1
}

# Update spec-files-other files and uninstall packages.
cd $SPECDIR/../spec-files-other

# Revert any local changes
svn revert -R .

# checkout-out SVN copy *MUST* be read-only, or "update" needs passwd
svn -q up > /dev/null 2>&1 || fatal_error "SVN update of spec-files-other failed"

# Uninstall the spec-files-other packages.
pkgtool uninstall-pkgs --with-l10n --with-sun-branding core/*.spec experimental/*.spec l10n/*.spec

# Uninstall and cleanup spec-files packages.
cd $SPECDIR || fatal_error "$SPECDIR not found"

#revert any local changes
svn revert -R .

# checkout-out SVN copy *MUST* be read-only, or "update" needs passwd
svn -q up > /dev/null 2>&1 || fatal_error "SVN update failed"

# change some components to use Sun Studio 12 to 
# workaround the compiler related issue
ss12_env_fl=/home/gbuild/dave/env.sh.ss12.cconly
ss12_specs="SUNWfirefox.spec
SUNWPython25.spec
../spec-files-other/core/SUNWbrasero.spec"
if [ -f $ss12_env_fl ]; then
    cd $SPECDIR
    IFS_save=$IFS
    IFS="
"
    for spec in $ss12_specs; do
        sed -e "/^%build/a\\
source $ss12_env_fl" \
            -e "/^%install/a\\
source $ss12_env_fl" $spec > ${spec}.tmp.$$
        mv ${spec}.tmp.$$ $spec 
    done
    IFS=$IFS_save
fi

# if the script changed during cvs update, restart with the updated script
cd $SPECDIR
if ! /usr/bin/cmp -s ./cron-script.sh $MYNAME; then exec ./cron-script.sh; fi

# uninstall all pkgs left behind by a previous build
pkgtool uninstall-pkgs --with-l10n --with-sun-branding --define 'support_level supported' closed/*.spec *.spec >/dev/null
# remove-gnome will now remove anything left from uninstall-pkgs in case
# or a packaging change for example
$SPECDIR/scripts/remove-gnome --version jds -q -f --no_extras > /dev/null 2>&1


rm -rf /jds/packages/PKGS/*
rm -rf /jds/packages/SPKGS/*
rm -rf /jds/packages/BUILD/*
rm -rf /var/tmp/pkgbuild-*/*

# if the log directory exists, open a new one with numbered suffix
NEW_LOGDIR=$LOGDIR
N=1
while [ -d $WEBROOT/$NEW_LOGDIR ]; do
    NEW_LOGDIR=$LOGDIR.$N
    N=`expr $N + 1`
done

LOGDIR=$NEW_LOGDIR
mkdir -p $WEBROOT/$LOGDIR || exit 5

mkdir -p $RPMSDIR
touch $LOCKFILE

# Rebuild the manpage tarballs
cd $SPECDIR
rm -r po-sun/po-sun-tarballs manpages/sun-manpage-tarballs
make 
cd $SPECDIR/../spec-files-other/manpages
rm -r sun-manpage-tarballs
make

cd $SPECDIR

# start the build
pkgtool -v --nightly --date "$RELEASE_DATE" build  closed/SUNWevolution-bdb-devel.spec closed/*.spec *.spec \
        --logdir=$WEBROOT/$LOGDIR \
        --logdir-url=http://jds.ireland/$LOGDIR \
	--mail-errors-to=gnome-2-10-build-reports@sun.com \
        --prodname="${PRODNAME}/s${OSrel}${OSarch}" \
        --live --with-l10n ${DEBUG_BUILD} \
        --define "nightly 1" --with-sun-branding --define 'support_level supported' \
        --summary-log=$WEBROOT/$LOGDIR.html \
        --summary-title="${PRODNAME} S${OSrel}/${OSarch_full} Nightly Build Report `date +'%d %B %Y'`" \
        --rpm-url=file:///net/jdsserv.ireland/$RPMSDIR/all_pkgs \
         > /tmp/build.log.$$ 2>&1

# the number of failed pkgs is returned
FAILED=$?

# Build spec-files-other
cd $SPECDIR/../spec-files-other

pkgtool -v --nightly --date "$RELEASE_DATE" build core/*.spec experimental/*.spec l10n/*.spec \
        --logdir=$WEBROOT/$LOGDIR \
        --logdir-url=http://jds.ireland/$LOGDIR \
	--mail-errors-to=gnome-2-10-build-reports@sun.com \
        --prodname="${PRODNAME}/s${OSrel}${OSarch}" \
        --live --with-l10n ${DEBUG_BUILD} \
        --define "nightly 1" --with-sun-branding --define 'support_level supported' \
        --summary-log=$WEBROOT/$LOGDIR-other.html \
        --summary-title="${PRODNAME} S${OSrel}/${OSarch_full} SFO Nightly Build Report `date +'%d %B %Y'`" \
        --rpm-url=file:///net/jdsserv.ireland/$RPMSDIR/all_pkgs \
         >> /tmp/build.log.$$ 2>&1

# The number of failed pkgs is returned
FAILED_OTHER=$?
# End spec-files-other build.

# rotate rpms dir
rm -rf $RPMSDIR.prev
mv $RPMSDIR $RPMSDIR.prev; mkdir -p $RPMSDIR

# make dist
/sgnome/tools/re-scripts/jds-build/make-jds-dist.pl -l /sgnome/tools/re-scripts/jds-build/vermillion-devel.lst --nightly /jds/packages/PKGS /jds/dist nightly- > /dev/null 2>&1
cp -r /jds/dist/nightly-/${OSarch_full}/* /jds/dist/nightly-/${OSarch_full}/.??* $RPMSDIR
chmod a+x $RPMSDIR/install-jds
mkdir -p $RPMSDIR/all_pkgs
cd $RPMSDIR/all_pkgs
ln -s ../*/*.tar.gz .
rm -rf /jds/dist/nightly-

# Send output of make-jds-dist.pl to GNOME RE for review.
/sgnome/tools/re-scripts/jds-build/make-jds-dist.pl -l /sgnome/tools/re-scripts/jds-build/vermillion-devel.lst --nightly /jds/packages/PKGS /jds/dist nightly- -dryrun 2>&1 | \
    mailx -s "${PRODNAME} S${OSrel} ${OSarch_full} nightly build: make-jds-dist.pl output" "gnome-re@sun.com"

ALL_REPORTS=$WEBROOT/$WEBDIR/all_reports.html
touch $ALL_REPORTS

cp $ALL_REPORTS $ALL_REPORTS.old
export FAILED FAILED_OTHER ALL_REPORTS

# update web page
( echo "<tr><td><a href=/$LOGDIR.html>$DIR_DATE</a></td>"; \
  echo "    <td>$FAILED package(s) failed</td></tr>"; \
  echo "<tr><td><a href=/$LOGDIR-other.html>$DIR_DATE</a></td>"; \
  echo "    <td>$FAILED_OTHER SFO package(s) failed</td></tr>"; \
  cat $ALL_REPORTS.old ) > $ALL_REPORTS

# Report absolute symlinks. These are blockers for Solaris integration.
grep 'is an absolute symlink' $WEBROOT/$LOGDIR/*.log >>/tmp/build.log.$$

# Count the number of local patches.
patch_count=`ls $SPECDIR/patches/*.diff | wc -l`
echo "PATCH COUNT: $patch_count local patches used in this build.">>/tmp/build.log.$$

# send warnings, errors and summary in email
grep -v '^INFO:' /tmp/build.log.$$ | \
    mailx -s "${PRODNAME} S${OSrel} ${OSarch_full} nightly build: $FAILED pkgs failed" $EMAIL_ADDR

rm -f /tmp/build.log.$$

# Email Beijing team to begin downloading packages.
/usr/bin/echo "*Date: `date '+%Y-%m-%d'`*\n${PRODNAME} S${OSrel} ${OSarch_full} Development nightly build finished: jdsserv.ireland:${RPMSDIR}/download" | 
    mailx -s "${PRODNAME} S${OSrel} ${OSarch_full} Development nightly build: $FAILED pkgs failed" "sunop@triathlon.prc.sun.com,sunop@mhw.prc.sun.com"


rm $LOCKFILE

# find any differences from the prototype files saved after the
# last milestone build
cd /jds/spec-files/prototypes/${OSarch_full}
for f in *.proto; do
    test -f /jds/packages/PKGMAPS/proto/$f || continue
    cmp -s $f /jds/packages/PKGMAPS/proto/$f && continue
    echo $f:
    diff $f /jds/packages/PKGMAPS/proto/$f
    echo
done > /tmp/proto-changes.$$

# if any diffs found mail the result to RE
test -s /tmp/proto-changes.$$ && {
    ( echo "Prototype changes found since the last milestone build:"
      echo
      cat /tmp/proto-changes.$$ ) | \
	  mailx -s "${PRODNAME} S${OSrel} ${OSarch_full} prototype changes" \
	  $EMAIL_ADDR
}

rm -f /tmp/proto-changes.$$

exit 0
