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

#
# This Makefile will create a file system package
# as a directory.
#
# To build new binaries and package issue:
# make
#
# To build only a package issue:
# make pkg
#
PKG=SUNWdistro-license
#possible ARCH values are i386, sparc, all
ARCH=i386

LIBS=devinfo

all: pkg

pkg:
	pkgmk -o -d ./ -a $(ARCH)
	chmod -R a+r $(PKG)
	chmod 555 $(PKG)

	@echo check current directory for .pkg files

clean: 
	chmod -R 777 SUNWdistro-license
	rm -r SUNWdistro-license
