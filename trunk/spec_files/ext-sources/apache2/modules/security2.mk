#
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
#
# ident	"@(#)security2.mk	1.6	08/10/07 SMI"
#


SECURITY2_VER= modsecurity-apache_2.1.5

security2: all-security2
	@echo "$@ built"

%-security2: %-security2-32 %-security2-64
	@echo "$@ built"

all-security2-%: $(SECURITY2_VER)-%/mod_security2.so
	@echo "$@ built"

clean-security2-%:
	rm -rf $(SECURITY2_VER)-$*

install-security2-%: all-security2-% sconf-install-security2
	(cd $(SECURITY2_VER)-$* ; env MACH64=$(MACH64) \
		$(SHELL) ../install-module.ksh93 -b $* -m security2)

#---------------------------------------
$(SECURITY2_VER)-%/Makefile: $(SECURITY2_VER).tar.gz tmp
	rm -rf $(SECURITY2_VER)-$*
	(cd tmp && \
		/usr/bin/gzip -dc ../$(SECURITY2_VER).tar.gz | \
			$(TAR) -xopf - && \
		mv -f $(SECURITY2_VER) ../$(SECURITY2_VER)-$* )
	find $(SECURITY2_VER)-$* -type d -exec chmod go+rx {} +

$(SECURITY2_VER)-%/mod_security2.so: $(SECURITY2_VER)-%/Makefile
	env "ROOT=$(ROOT)" "MACH64=$(MACH64)" "CC=$(CC)" \
		$(SHELL) ./apxs-security2.ksh93 -b $*


