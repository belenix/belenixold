#ident	"@(#)fix-config_vars.sed	1.6	08/09/15 SMI"	
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

# apply changes to installed object $ROOT/usr/apache2/2.2/build$ISA/config_vars.mk

/^AP_LIBS =/c\
AP_LIBS = /usr/share/src/apache2/srclib/pcre/libpcre.la /usr/share/src/apache2/srclib/apr-util/libaprutil-1.la /usr/share/src/apache2/srclib/apr-util/xml/expat/lib/libexpat.la /usr/share/src/apache2/srclib/apr/libapr-1.la -lsendfile -lrt -lm -lsocket -lnsl -lresolv

/^abs_srcdir =/c\
abs_srcdir = /usr/share/src/apache2

/^CC =/c\
CC = /opt/SUNWspro/bin/cc

/^CPP =/c\
CPP = /opt/SUNWspro/bin/cc -E

/^CXX =/c\
CXX = /opt/SUNWspro/bin/CC

/^EXTRA_LDFLAGS =/c\
EXTRA_LDFLAGS = -L/usr/share/src/apache2/srclib/apr-util/xml/expat/lib

/^EXTRA_INCLUDES =/c\
EXTRA_INCLUDES = -I/usr/share/src/apache2/srclib/apr/include -I/usr/share/src/apache2/srclib/apr-util/include -I/usr/share/src/apache2/srclib/apr-util/xml/expat/lib -I. -I$(top_srcdir)/os/$(OS_DIR) -I$(top_srcdir)/server/mpm/$(MPM_SUBDIR_NAME) -I$(top_srcdir)/modules/http -I$(top_srcdir)/modules/filters -I$(top_srcdir)/modules/proxy -I$(top_srcdir)/include -I$(top_srcdir)/modules/dav/main

/^APR_INCLUDEDIR =/c\
APR_INCLUDEDIR = /usr/share/src/apache2/srclib/apr/include

/^APU_INCLUDEDIR =/c\
APU_INCLUDEDIR = /usr/share/src/apache2/srclib/apr-util/include

/^MKDEP =/c\
MKDEP = /opt/SUNWspro/bin/cc -xM
