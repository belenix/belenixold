#!/usr/bin/bash
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
# Copyright 2005 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# Author: Darren.Moffat@Sun.COM, Moinak.Ghosh@Sun.COM
#

PATH=/usr/foss/bin:/usr/bin:/usr/sbin

do_action()
{
	for service in $@ ; do
		current_state=$(svcs -H -o state $service)
		
		if [ "$current_state" = "offline" ]; then
			svcs -x -v 2>&1 > /tmp/svcs-x-zenity-$$
			zenity --width=500 --height=300 --text-info \
			    --title="svcs -v -x $service" \
			    --filename=/tmp/svcs-x-zenity-$$
			rm /tmp/svcs-x-zenity-$$
			continue;
		fi

		case $current_state in
		'disabled') allowed_actions="Start Enable Refresh Info";;
		'online') allowed_actions="Stop Disable Refresh Processes Details";;
		'maintenance') allowed_actions="Stop Disable Clear Refresh Info";;
		esac
		action=$(zenity --list --title="$service" --column "Perform Action"\
			--width=300 --height=300 $allowed_actions)
		[ -z "$action" ] && break

		
		if [ "$action" = "Processes" -o \
			"$action" = "Info" -o "$action" = "Details" ]
		then
			case $action in
			  'Processes') opt="-p";;
			  'Info') opt="-xv";;
			  'Details') opt="-l";;
			esac
			svcs $opt $service 2>&1 > /tmp/svcs-x-zenity-$$
			zenity --width=500 --height=400 --text-info \
				--title="svcs $opt $service" \
				--filename=/tmp/svcs-x-zenity-$$
			rm /tmp/svcs-x-zenity-$$
			continue
		fi

		oaction=$action
		case $action in
		  "Start") action="enable -st";;
		  "Stop") action="disable -st";;
		  "Refresh") action="refresh";;
		  "Disable") action="disable -s";;
		  "Enable") action="enable -s";;
		  "Clear") action="clear";;
		esac

		(
		print "Performing $oaction on $service"
		res=`svcadm $action $service 2>&1`
		if [ $? -ne 0 ]
		then
			zenity --error --error-text "$res"
		fi
		print "100"
		) | zenity --progress --auto-close --pulsate \
			--title="$serv" --percentage=0
	done
}


if [ "$1" = "-h" ]; then
	echo "Usage: `basename $0` [-a] [FMRI | pattern]..."
	echo "       -a\tlist all services"
	exit 0
fi

while true ; do
	services=$(svcs -a -H -o fmri,stime,state,nstate -s fmri -s state \
		-S nstate $@ |sed s/-$/X/g)
	err=$?
	[ $err != 0 ] && exit $err

	service=$(zenity --list --title="Services" \
		--width=600 --height=500 \
		--column=FMRI --column=STIME --column=STATE --column NSTATE\
		$services)
	[ ! $? -eq 0 ] && break;

	if [ -z "$service" ]
	then
		zenity --error --error-text "Please select one or more services"
	fi

	do_action `echo $service | sed 's/|/ /g'`
done
