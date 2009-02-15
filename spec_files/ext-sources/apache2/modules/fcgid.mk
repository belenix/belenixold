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
# ident	"@(#)fcgid.mk	1.5	08/10/07 SMI"
#


FCGID_VER=mod_fcgid.2.2

fcgid: all-fcgid
	@echo "$@ built"

%-fcgid: %-fcgid-32 %-fcgid-64
	@echo "$@ built"

all-fcgid-%: $(FCGID_VER)-%/mod_fcgid.so
	@echo "$@ built"

clean-fcgid-%:
	rm -rf $(FCGID_VER)-$*

install-fcgid-%: all-fcgid-% sconf-install-fcgid
	(cd $(FCGID_VER)-$* ; env MACH64=$(MACH64) \
		$(SHELL) ../install-module.ksh93 -b $* -m fcgid)

#---------------------------------------
$(FCGID_VER)-%/Makefile: $(FCGID_VER).tgz tmp
	rm -rf $(FCGID_VER)-$*
	(cd tmp && \
		/usr/bin/gzip -dc ../$(FCGID_VER).tgz | \
			$(TAR) -xopf - && \
		mv -f $(FCGID_VER) ../$(FCGID_VER)-$* )

$(FCGID_VER)-%/mod_fcgid.so: $(FCGID_VER)-%/Makefile
	env "ROOT=$(ROOT)" "MACH64=$(MACH64)" "CC=$(CC)" \
		$(SHELL) ./apxs-fcgid.ksh93 -b $*


