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
# Copyright 2006 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)init.sma	1.17	06/06/01 SMI"

case "$1" in
  start)
	svcadm enable -t svc:/application/management/sma:default
        ;;
  stop)
	svcadm disable -t svc:/application/management/sma:default
        ;;
  status)
	svcs svc:/application/management/sma:default
	;;
  restart)
	svcadm restart svc:/application/management/sma:default
	;;
  *)

        echo ""
	echo "\tUsage: $0 { start | stop | restart | status }"
	echo ""
        exit 1
esac

exit 0
