#!/bin/bash

# Sample usage in crontab:
# Run, Mon-Fri at 1:30am. Add to build user's crontab.
#   30 1 * * 1-5 . /jds/cbe/bin/env.sh; I_KNOW_WHAT_IM_DOING=yes myEnv=nightly-beijing.env $0
#
# The same with a jail. Add to root's crontab. Example assumes 'gbuild' is the
# build user
#   30 1 * * 1-5 /usr/sbin/chroot /path/to/jail/root /usr/bin/su - gbuild -c ". /jds/cbe/bin/env.sh; I_KNOW_WHAT_IM_DOING=yes myEnv=nightly-beijing.env $0"
#
# Or - you may choose to only build a particular package
#   30 1 * * 1-5 . /jds/cbe/bin/env.sh; thisSpec=SUNWTiff.spec I_KNOW_WHAT_IM_DOING=yes myEnv=nightly-beijing.env $0
#
# History:
# --------
#
# Damien Carbery:
#       cron-script.sh, original script
#
# Alexandre Berman:
#       based on the original script, created cron-nightly.sh
#       added/changed features:
#         - added sub-routines for easy debugging, clarity
#         - changed to SVN (original script used cvs)
#         - took all site-dependent variable declarations out of the script and adopted it to use env file
#         - added support for building individual components (must specify spec file), useful for debugging and others..
#         - added more verbosity to the script for debugging and clarity

if [ -r $myEnv ]; then
   . $myEnv # setup our env
else
   echo "-- ENV is NOT defined ! Exiting..."
   exit 1
fi

# host to rcp the rpms to
RHOST="$RHOST"
# user to rcp as (has to have root@<this host> in it's .rhosts file)
RUSER="$RUSER"
# other vars
TEMP_DIR="$TEMP_DIR"
SPECDIR="$SPECDIR"
BUILD_BASE="$BUILD_BASE"
PRODNAME="$PRODNAME"
# directory to copy rpms/srpms to on the remote host
RPMSDIR="$RPMSDIR"
LOCKFILE="$RPMSDIR/.build.lock"
# reply-to/to address to send the build log as/to
EMAIL_ERRORS_TO="$EMAIL_ERRORS_TO"
EMAIL_NOTIFICATION="$EMAIL_NOTIFICATION"
# document root of the web server
WEBROOT="$WEBROOT"
LOGDIR_BASE_URL="$LOGDIR_BASE_URL"
# tarballsdir
TARBALLSDIR="$TARBALLSDIR"
# subdir to keep logs and reports on the webserver
WEBDIR="$WEBDIR"

# date format appended to the Release tag in the spec files
# (passed to the date command on the cmd line)
RELEASE_DATE_FMT="%y%m%d"
# date format used for naming the directories
DIR_DATE_FMT="%Y-%m-%d"
RELEASE_DATE=`date +$RELEASE_DATE_FMT`
DIR_DATE=`date +$DIR_DATE_FMT`
LOGDIR="$WEBDIR/$DIR_DATE"

# ------------ nothing to configure below this line --------------

if [ "x$I_KNOW_WHAT_IM_DOING" != xyes ]; then
    echo " ,---------------------------------------------------------------."
    echo "| This script is intended to be run from cron for producing      |"
    echo "| official nightly builds (Beijing site).                        |"
    echo "| It will mail responsible engineers                             |"
    echo "| if any build failure occurs, sends build reports to            |"
    echo "| RE and update web pages.                                       |"
    echo "|"
    echo "| Don't run it unless you know what you are doing. Thanks."
    echo "|"
    echo "| Mail jdsbj-re@sun.com if you need more info."
    echo ".................................................................+"
    exit 1
fi

MYNAME="$0"
MYDIR=$(cd `dirname $0`; pwd)
shortName=`echo $MYNAME | sed -e 's|^.*\/||g'`

# remove temporary files on exit
clean_up () {
  case "$MYNAME" in
  /tmp/$shortName.copy.* )
        rm -f $MYNAME
        ;;
  esac
  exit
}

trap clean_up HUP INT TERM QUIT EXIT

# make a copy of the cron script in /tmp and execute that in order to
# avoid disasters caused by cvs update.
case "$MYNAME" in
    /tmp/*.copy.* )
        ;;
    *)
        cp $MYNAME /tmp/$shortName.copy.$$
        chmod 755 /tmp/$shortName.copy.$$
        cd /tmp
        exec /tmp/$shortName.copy.$$ "$MYDIR"
        ;;
esac

fatal_error () {
  echo "ERROR: $*"
  exit 1
}

# prepare TEMP_DIR and repository - using SVN now
prep_repository() {
   if [ -d $SPECDIR ]; then
      cd $SPECDIR || fatal_error "$SPECDIR not found"
      echo "-- updating SVN rep ..."
      #revert any local changes
      svn revert -R .

      svn -q up > /dev/null 2>&1 || fatal_error "SVN update failed"
   else
      echo "-- checking out fresh copy of Spec files from SVN rep ..."
      rm -rf $TEMP_DIR
      mkdir $TEMP_DIR; cd $TEMP_DIR
      svn -q checkout svn://dtsvn.ireland.sun.com/sgnome/svn/repos/jds-spec-files/trunk \
                                 > /dev/null 2>&1 || fatal_error "SVN checkout failed"
   fi
   # if the script changed during repository update, restart with the updated script
   if ! /usr/bin/cmp -s $SPECDIR/$shortName $MYNAME; then exec $SPECDIR/$shortName; fi
}


# uninstall all pkgs left behind by a previous build
do_uninst() {
   echo "-- uninstalling packages..."
   pkgtool uninstall-pkgs --with-l10n --with-tjds $thisSpec >/dev/null
   # remove-gnome will now remove anything left from uninstall-pkgs in case
   # of a packaging change for example
   $SPECDIR/scripts/remove-gnome --version jds -q -f --no_extras > /dev/null 2>&1
}

do_clean_pkgs() {
   rm -rf $BUILD_BASE/PKGS/*
   rm -rf $BUILD_BASE/SPKGS/*
   rm -rf $BUILD_BASE/BUILD/*
   rm -rf /var/tmp/*-build
}

# if the log directory exists, open a new one with numbered suffix
do_log_dir() {
   echo "-- setting up logs..."
   NEW_LOGDIR=$LOGDIR
   N=1
   while [ -d $WEBROOT/$NEW_LOGDIR ]; do
       NEW_LOGDIR=$LOGDIR.$N
       N=`expr $N + 1`
       echo "-- LOGDIR exists, changing to: $NEW_LOGDIR"
   done
   LOGDIR=$NEW_LOGDIR
   echo "-- LOGDIR:     $WEBROOT/$LOGDIR"
   echo "-- LOGDIR URL: $LOGDIR_BASE_URL/$LOGDIR"
   mkdir -p $WEBROOT/$LOGDIR || exit 5
}

# start the build
do_build() {
   echo "-- build started, using log: /tmp/build.log.$$ ..."
   cd $SPECDIR || fatal_error "$SPECDIR not found"
   echo '' | rsh $RHOST -l $RUSER "mkdir -p $RPMSDIR; touch $LOCKFILE"
   pkgtool -v --nightly --date "$RELEASE_DATE" build $thisSpec \
        --logdir=$WEBROOT/$LOGDIR \
        --summary-log=$WEBROOT/$LOGDIR.html \
        --logdir-url=$LOGDIR_BASE_URL/$LOGDIR \
	--mail-errors-to=$EMAIL_ERRORS_TO \
        --prodname="${PRODNAME}/s${OSrel}${OSarch}" \
        --live --with-l10n --with-tjds \
	--norc \
	--tarballdirs=$TARBALLSDIR \
        --define "nightly 1" \
        --summary-title="${PRODNAME} S${OSrel}/${OSarch_full} Nightly Build Report `date +'%d %B %Y'`" \
         > /tmp/build.log.$$ 2>&1
   #     --rpm-url=file:///net/allstar.prc$RPMSDIR/all_pkgs \
   # the number of failed pkgs is returned
   FAILED=$?; export FAILED
}

# choose what to build ?
# coices are: everything or specific spec file
choose_build() {
   if [ "x$thisSpec" = "x" ]; then
      # no spec file was chosen, build everything
      thisSpec='*.spec closed/*.spec'; export thisSpec
      echo "-- building following components: $thisSpec"
   else
      # verify chosen spec file
      if [ ! -f $SPECDIR/$thisSpec ]; then
         fatal_error "chosen spec file ($thisSpec) does not exist in spec dir ($SPECDIR)"
      fi
      echo "-- building following components: $thisSpec"
   fi
}

# rotate rpms dir
do_rotate_rpms() {
   echo '' | rsh $RHOST -l $RUSER "rm -rf $RPMSDIR.prev; mv $RPMSDIR $RPMSDIR.prev; mkdir -p $RPMSDIR"
}

# make dist
do_make_dist() {
   echo "-- making dist ..."
   /sgnome/tools/re-scripts/jds-build/make-jds-dist /jds/packages/PKGS /jds/dist nightly- > /dev/null 2>&1
   echo '' | rcp -r /jds/dist/nightly-/${OSarch_full}/* /jds/dist/nightly-/${OSarch_full}/.??* ${RUSER}@${RHOST}:$RPMSDIR
   echo '' | rsh $RHOST -l $RUSER "chmod a+x $RPMSDIR/install-jds"
   echo '' | rsh $RHOST -l $RUSER "mkdir -p $RPMSDIR/all_pkgs && cd $RPMSDIR/all_pkgs && ln -s ../*/*.tar.gz ."
   rm -rf /jds/dist/nightly-
}

# web reports
do_web_reports() {
   ALL_REPORTS=$WEBROOT/$WEBDIR/all_reports.html
   echo "-- creating main report in: $ALL_REPORTS"
   touch $ALL_REPORTS
   cp $ALL_REPORTS $ALL_REPORTS.old
   export ALL_REPORTS
   # update web page
   ( echo "<A HREF=$LOGDIR_BASE_URL/$LOGDIR.html>$DIR_DATE</A> $FAILED package(s) failed<BR>"; \
                                                           cat $ALL_REPORTS.old ) > $ALL_REPORTS
}

# send warnings, errors and summary in email
do_email() {
   grep -v '^INFO:' /tmp/build.log.$$ | \
    mailx -s "${PRODNAME} S${OSrel} ${OSarch_full} nightly build: $FAILED pkgs failed" $EMAIL_NOTIFICATION
}

# final cleanup
do_finally() {
   rm -f /tmp/build.log.$$
   echo '' | rsh $RHOST -l $RUSER "rm $LOCKFILE"
}

# let's do it
choose_build
prep_repository
do_uninst
do_clean_pkgs
do_log_dir
do_build
do_rotate_rpms
do_make_dist
do_web_reports
do_email
do_finally

exit 0
