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
# ident	"@(#)jk.mk	1.4	08/08/18 SMI"
#


JK_VER=tomcat-connectors-1.2.25-src

jk: all-jk
	@echo "$@ built"

%-jk: %-jk-32 %-jk-64
	@echo "$@ built"

all-jk-%: $(JK_VER)-%/mod_jk.so
	@echo "$@ built"

clean-jk-%:
	rm -rf $(JK_VER)-$*

install-jk-%: all-jk-% conf-install-jk conf-jk-worker
	(cd $(JK_VER)-$* ; env MACH64=$(MACH64) \
		$(SHELL) ../install-module.ksh93 -b $* -m jk)

conf-jk-worker:
	cat workers.properties > $(APACHE_CONFD)/workers.properties

#---------------------------------------
$(JK_VER)-%/native/Makefile: $(JK_VER).tar.gz tmp
	rm -rf $(JK_VER)-$*
	(cd tmp && \
		/usr/bin/gzip -dc ../$(JK_VER).tar.gz | \
			$(TAR) -xopf - && \
		mv -f $(JK_VER) ../$(JK_VER)-$* )

$(JK_VER)-%/mod_jk.so: $(JK_VER)-%/native/Makefile
	env "ROOT=$(ROOT)" "MACH64=$(MACH64)" "CC=$(CC)" \
		$(SHELL) ./apxs-jk.ksh93 -b $*


