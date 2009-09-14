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
# Author: moinakg@belenix.org
#

objs = taskq.o kernel.o
CFLAGS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -std=c99 -D__EXTENSIONS__ -fPIC -DPIC
LDFLAGS = -lthread -lumem
INC = 

# Uncomment this for debugging information in the files
DEBUG = -g

all: libtaskq.so.1

libtaskq.so.1: $(objs)
	@echo Linking
	@gcc -shared $(DEBUG) $(CFLAGS) $(LDFLAGS) $(objs) -o libtaskq.so.1

.c.o:
	@echo Compiling $<
	@gcc -c $< $(DEBUG) $(INC) $(CFLAGS)

clean:
	@rm -f *.o
	@rm -f libtaskq.so.1

install:
	@mkdir -p $(DESTDIR)/usr/lib
	@cp  btaskq.so.1 $(DESTDIR)/usr/lib
	@chmod 0755 $(DESTDIR)/usr/lib/libtaskq.so.1
	@ln -s $(DESTDIR)/usr/lib/libtaskq.so libtaskq.so.1
