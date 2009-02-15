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
# ident	"@(#)dtrace.mk	1.4	08/08/18 SMI"
#


DTRACE_VER=mod_dtrace-0.3a

dtrace: all-dtrace
	@echo "$@ built"

%-dtrace: %-dtrace-32 %-dtrace-64
	@echo "$@ built"

all-dtrace-%: $(DTRACE_VER)-%/mod_dtrace.so
	@echo "$@ built"

clean-dtrace-%:
	rm -rf $(DTRACE_VER)-$*

install-dtrace-%: all-dtrace-% conf-install-dtrace
	(cd $(DTRACE_VER)-$* ; env MACH64=$(MACH64) \
		$(SHELL) ../install-module.ksh93 -b $* -m dtrace)

#---------------------------------------
$(DTRACE_VER)-%/native/Makefile: $(DTRACE_VER).tar.gz tmp
	rm -rf $(DTRACE_VER)-$*
	(cd tmp && \
		/usr/bin/gzip -dc ../$(DTRACE_VER).tar.gz | \
			$(TAR) -xopf - && \
		mv -f $(DTRACE_VER) ../$(DTRACE_VER)-$* )

$(DTRACE_VER)-%/mod_dtrace.so: $(DTRACE_VER)-%/native/Makefile
	env "ROOT=$(ROOT)" "MACH64=$(MACH64)" "LDFLAGS=$(LDFLAGS:%mapfile_noexstk=$(PWD)/$(DTRACE_VER)-$*/mapfile)" "CC=$(CC)" \
		$(SHELL) ./apxs-dtrace.ksh93 -b $*


