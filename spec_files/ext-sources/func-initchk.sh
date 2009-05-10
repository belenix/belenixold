#!/usr/bin/ksh

USER=$1
GROUP=$2
DATADIR=$3
LOGDIR=$4
PROFILE=$5
PASSWD=/etc/passwd
GROUPFILE=/etc/group

PROFILE=`echo "$PROFILE" | sed 's/\\\//g'`

if [ -z "$USER" -o -z "$GROUP" -o -z "$DATADIR" -o -z "$LOGDIR" -o -z "$PROFILE" ]
then
	echo "ERROR: All parameters are not specified"
	echo "Usage: $0 <username> <groupname> <datadir> <logdir> <profile>"
	exit 1
fi

#
# Initial processing.
#
# Check if the user exists, add it if not.
#
grep "^${USER}:" $PASSWD > /dev/null
if [ $? -ne 0 ]
then
	grep "^${GROUP}:" $GROUPFILE > /dev/null
	if [ $? -ne 0 ]
	then
		groupadd $GROUP
		[ $? -ne 0 ] && exit 1
	fi
	useradd -s /usr/bin/sh -d / -g $GROUP -P "$PROFILE" $USER
	[ $? -ne 0 ] && exit 1
else
	#
	# Get the current profile of the user
	#
	uprof=`cat /etc/user_attr | nawk -F "^${USER}:" 'BEGIN {FS=":"} {
	patt = "profiles=";
	pos = index($5, patt);
	if (pos > 0) {
		rem = substr($5, pos + length(patt));
		pos1 = index(rem, ";")
		if (pos1 > 0) {
			prof = substr(rem, 1, pos1-1)
		} else {
			prof = rem
		}
		print prof
	}}'`
	[ $? -ne 0 ] && exit 1

	#
	# If they are not the same as one in SMF then modify
	#
	if [ "$uprof" != "$PROFILE" ]
	then
		usermod -P "$PROFILE" $USER
		[ $? -ne 0 ] && exit 1
	fi
fi

#
# Ensure runtime dirs are owned by above user
#
/usr/bin/chown -f -R ${USER}:${GROUP} ${DATADIR}/*
/usr/bin/chown -f -R ${USER}:${GROUP} ${LOGDIR}/*

for auth in "func.module.write:::Allow Func Modules to change system parameters::"
do
	grep "$auth" /etc/security/auth_attr > /dev/null
        if [ $? -ne 0 ]
	then
		echo "$auth" >> /etc/security/auth_attr
	fi
done

for prof in "Func Admin:::Administrative Rights for Func modules:auths=func.*"
do
	grep "$prof" /etc/security/prof_attr > /dev/null
	if [ $? -ne 0 ]
	then
		echo "$prof" >> /etc/security/prof_attr
	fi
done
