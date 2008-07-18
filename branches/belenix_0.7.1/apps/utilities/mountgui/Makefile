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
# Copyright 2008 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# Author: Moinak.Ghosh@Sun.COM
#

all: mounts

clean:

install:
	@mkdir -p $(DESTDIR)/usr/bin
	@cp mounts $(DESTDIR)/usr/bin
	@chmod 0755 $(DESTDIR)/usr/bin/mounts
	@mkdir -p $(DESTDIR)/usr/share/pixmaps
	@cp disk_mounts.png $(DESTDIR)/usr/share/pixmaps
	@mkdir -p $(DESTDIR)/usr/share/applications
	@cp hdd_mount.desktop $(DESTDIR)/usr/share/applications
