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
# Author: moinakg@gmail.com
#

listcd_obj = listcd.o
listusb_obj = listusb_all.o
pagein_obj = pagein.o
checkcore_obj = checkcore.o
checklkcd_obj = checklkcd.o

CFLAGS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -std=c99 -D__EXTENSIONS__
LDFLAGS = -ldevinfo
INC = -I.

# Uncomment this for debugging information in the files
#DEBUG = -g

PKG=FSWlivecdtools
#possible ARCH values are i386, sparc, all
ARCH=i386

all: listcd listusb pagein checkcore checklkcd

listcd: $(listcd_obj)
	@echo Linking listcd
	@gcc $(DEBUG) $(CFLAGS) $(listcd_obj) $(LDFLAGS) -o listcd

listusb: $(listusb_obj)
	@echo Linking listusb
	@gcc $(DEBUG) $(CFLAGS) $(listusb_obj) $(LDFLAGS) -o listusb

pagein: $(pagein_obj)
	@echo Linking pagein
	@gcc $(DEBUG) $(CFLAGS) $(pagein_obj) -o pagein

checkcore: $(checkcore_obj)
	@echo Linking checkcore
	@gcc $(DEBUG) $(CFLAGS) $(checkcore_obj) -o checkcore

checklkcd: $(checklkcd_obj)
	@echo Linking checklkcd
	@gcc $(DEBUG) $(CFLAGS) $(checklkcd_obj) -o checklkcd

.c.o:
	@echo Compiling $<
	@gcc -c $< $(DEBUG) $(INC) $(CFLAGS)

clean:
	@rm -f *.o
	@rm -f listcd
	@rm -f listusb
	@rm -f pagein
	@rm -f checkcore
	@rm -f checklkcd
	@chmod -R 777 FSWlivecdtools
	@rm -rf FSWlivecdtools

install:
	@mkdir -p $(DESTDIR)/sbin
	@cp listcd $(DESTDIR)/sbin
	@cp listusb $(DESTDIR)/sbin
	@cp pagein $(DESTDIR)/sbin
	@cp checkcore $(DESTDIR)/sbin
	@cp checklkcd $(DESTDIR)/sbin
	@chmod 0755 $(DESTDIR)/sbin/listcd
	@chmod 0755 $(DESTDIR)/sbin/listusb
	@chmod 0755 $(DESTDIR)/sbin/pagein
	@chmod 0755 $(DESTDIR)/sbin/checkcore
	@chmod 0755 $(DESTDIR)/sbin/checklkcd

pkg: all
	pkgmk -o -d ./ -a $(ARCH)
	chmod -R a+r $(PKG)
	chmod 555 $(PKG)

	@echo check current directory for .pkg files
