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
mcp_objs = mcp.o
CFLAGS = -D_FILE_OFFSET_BITS=64 -xc99=%all -D__EXTENSIONS__ -fPIC -DPIC -I.
LDFLAGS = -lthread -lumem 
INC = 
CC = /opt/SUNWspro/bin/cc
SHLIB_FLAGS = -G
MCP_LDFLAGS = -L. -R. -ltaskq

# Uncomment this for debugging information in the files
DEBUG = -g

all: libtaskq.so.1 mcp

libtaskq.so.1: $(objs)
	@echo Linking
	$(CC) $(SHLIB_FLAGS) $(DEBUG) $(CFLAGS) $(LDFLAGS) $(objs) -o libtaskq.so.1
	ln -sf libtaskq.so.1 libtaskq.so

.c.o:
	@echo Compiling $<
	$(CC) -c $< $(DEBUG) $(INC) $(CFLAGS)

mcp: libtaskq.so.1 $(mcp_objs)
	@echo Linking mcp
	$(CC) $(DEBUG) $(CFLAGS) $(MCP_LDFLAGS) $(mcp_objs) -o mcp

clean:
	@rm -f *.o
	@rm -f libtaskq.so.1
	@rm -f libtaskq.so
	@rm -f mcp

install:
	@mkdir -p $(DESTDIR)/usr/lib
	@cp libtaskq.so.1 $(DESTDIR)/usr/lib
	@chmod 0755 $(DESTDIR)/usr/lib/libtaskq.so.1
	@ln -s $(DESTDIR)/usr/lib/libtaskq.so libtaskq.so.1
	@cp libtaskq.h $(DESTDIR)/usr/include
	@cp libtaskq_defs.h $(DESTDIR)/usr/include
	@chmod 0444 $(DESTDIR)/usr/include/libtaskq*
