#ident	"@(#)httpdconf.sed	1.9	08/02/14 SMI"	
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
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.

/^# Do NOT simply/i\
# Solaris Quick Configuration Information\
#\
# 1. Set ServerName if necessary (default is 127.0.0.1)\
# 2. Set ServerAdmin to a valid email address\
#\
#
/^ServerAdmin/c\
ServerAdmin you@yourhost.com
/^#ServerName/c\
ServerName 127.0.0.1
/^ServerName/c\
ServerName 127.0.0.1
/^User/c\
User webservd
/^Group/c\
Group webservd
/^LoadModule /d

$a\
\
<IfModule prefork.c>\
    ListenBacklog 8192\
    ServerLimit 2048\
    MaxClients 2048\
</IfModule>

