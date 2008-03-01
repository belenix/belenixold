#!/bin/sh
#
# CDDL HEADER START
#
# The contents of this file are subject to the terms of the
# Common Development and Distribution License (the "License").
# You may not use this file except in compliance with the License.
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
# Copyright 2006 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# Author: Moinak.Ghosh@Sun.COM
#

NUMDISKS=0
LASTDISK=""
DISKLIST=""

dumpdisks() {
fmt=`echo "" | /usr/sbin/format`
flag=0
cnt=0
for item in $fmt
do
        if [ $flag -eq 1 ]; then
                flag=0
		NUMDISKS=`expr $NUMDISKS+1`
		LASTDISK="/dev/rdsk/${item}p0"
		DISKLIST="$DISKLIST\n/dev/rdsk/${item}p0"
		#echo "/dev/rdsk/${item}p0"
        fi
        if [ "$item" = "$cnt." ]; then flag=1; cnt=`expr $cnt + 1`; fi
done
}

if [ $# -eq 0 ]
then
	dumpdisks
	if [ $NUMDISKS -gt 1 ]
	then
		echo "Available disk devices:"
		echo $DISKLIST
		echo ""
		echo "Use /usr/bin/prtpart <disk device> to get partition details"
		echo "Use /usr/bin/prtpart -help for usage help"
		exit 0
	else
		exec /usr/bin/prtpart.bin $LASTDISK
	fi
fi

exec /usr/bin/prtpart.bin "$@"

