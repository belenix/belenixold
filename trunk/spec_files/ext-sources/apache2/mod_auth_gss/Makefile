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
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
#ident	"@(#)Makefile	1.3	07/11/14 SMI"
#

include ../apache.build.env

top_srcdir   = ../$(APACHE_PREFORK_DIR)
top_builddir = ../$(APACHE_PREFORK_DIR)
srcdir       = .
builddir     = .
VPATH        = .

DESTDIR=$(ROOT)

static =

shared = mod_auth_gss.la

SHARED_TARGETS = $(shared)
INSTALL_TARGETS = install-modules-$(INSTALL_DSO)


$(builddir)/.deps: local-depend

include $(top_builddir)/build/rules.mk
include $(top_builddir)/build/config_vars.mk

all: mod_auth_gss.la install

SH_LIBS=-lgss

install-modules-yes: mod_auth_gss.la
	@$(MKINSTALLDIRS) $(DESTDIR)$(libexecdir)
	$(RM) $(DESTDIR)/$(libexecdir)/$(shared:.la=.so);
	$(top_srcdir)/build/instdso.sh SH_LIBTOOL='$(SH_LIBTOOL)' $(shared) $(DESTDIR)/$(libexecdir);

install-modules-no:

mod_auth_gss.la:	$(builddir)/.deps mod_auth_gss.c mod_auth_gss.slo 
	$(SH_LINK) -rpath $(libexecdir) -module -avoid-version mod_auth_gss.lo

clean:
	-rm -f .deps *.o *.so *.lo *.la
	-rm -rf .libs
