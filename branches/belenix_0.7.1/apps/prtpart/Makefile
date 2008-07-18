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

objs = prtpart.o
CFLAGS = -D_LARGEFILE_SOURCE -D_FILE_OFFSET_BITS=64 -std=c99 -D__EXTENSIONS__
INC = 

# Uncomment this for debugging information in the files
DEBUG = -g

all: prtpart.bin prtpart

prtpart.bin: $(objs)
	@echo Linking
	@gcc $(DEBUG) $(CFLAGS) $(objs) -o prtpart.bin

prtpart:
	@cp prtpart.sh prtpart
	@chmod 0755 prtpart

.c.o:
	@echo Compiling $<
	@gcc -c $< $(DEBUG) $(INC) $(CFLAGS)

clean:
	@rm -f *.o
	@rm -f prtpart.bin
	@rm -f prtpart

install:
	@mkdir -p $(DESTDIR)/usr/bin
	@cp prtpart.bin $(DESTDIR)/usr/bin
	@cp prtpart $(DESTDIR)/usr/bin
	@chmod 0755 $(DESTDIR)/usr/bin/prtpart
	@chmod 0755 $(DESTDIR)/usr/bin/prtpart.bin
