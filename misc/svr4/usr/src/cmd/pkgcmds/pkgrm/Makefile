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
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# ident	"@(#)Makefile	1.33	07/11/06 SMI"
#
PROG=		pkgrm

OBJECTS=	main.o quit.o presvr4.o check.o
SRCS=		$(OBJECTS:.o=.c)

include ../../Makefile.cmd
TEXT_DOMAIN= SUNW_PKG_CMDS
#
# for messaging catalog files
#
POFILE= pkgrm.po
POFILES= $(SRCS:%.c=%.po)

LOCAL=		.
GENERAL=	../hdrs
LIBPKGDIR=  $(SRC)/lib/libpkg
LIBGENDIR=  $(SRC)/lib/libgendb
LIBINSTDIR= $(SRC)/lib/libinst

CPPFLAGS=	-I$(LOCAL) -I$(GENERAL) -I$(LIBPKGDIR) -I$(LIBGENDIR) \
		-I$(SFWINCDIR) $(CPPFLAGS.master) \
		-I$(ROOTINCADMIN) \
		-DTEXT_DOMAIN=\"${TEXT_DOMAIN}\"

GENLIBS=     -L$(SFWLIBDIR) -R$(SFWLIBRDIR) -L$(ROOTADMINLIB)
LIBINST=    $(LIBINSTDIR)/libinst.a
LAZYLIB=	-z lazyload -lzonecfg -lcontract -z nolazyload
LIBSSO=     -ladm -lnsl -lsocket -lelf -lwanboot -lssl -lcrypto -lmd5 -lscf
LIBPKGSO=   -lpkg
LIBSPMI		= -lspmizones -lspmicommon
LIBPKGAR=   $(SRC)/lib/libpkg/objs/$(ARCH)/libpkg.a
LDLIBSSO=   $(LDLIBS.cmd) $(LIBINST) $(GENLIBS) $(LIBPKGSO) $(LIBSSO) $(LIBSPMI) $(LAZYLIB)
LDLIBSAR=   $(LDLIBS.cmd) $(LIBINST) $(GENLIBS) $(LIBPKGAR) $(LIBSSO) $(LIBSPMI) $(LAZYLIB)
LDFLAGS	    += -R$(ROOTADMINLIB:$(ROOT)%=%)

FILEMODE=	0555
OWNER=		root
GROUP=		sys

.KEEP_STATE:

all: 		$(PROG) 

dynamic:    $(OBJECTS) $(LIBINST)
	$(LINK.c) -o $(PROG) $(OBJECTS) $(LDLIBSSO)
	$(POST_PROCESS $(PROG))

static: $(OBJECTS) $(LIBINST)
	$(LINK.c) -o $(PROG) $(OBJECTS) $(LDLIBSAR)
	$(POST_PROCESS $(PROG))

$(PROG):    $(OBJECTS) $(LIBINST)
	$(LINK.c) -o $(PROG) $(OBJECTS) $(LDLIBSSO)
	$(POST_PROCESS)

catalog:        $(POFILE)

$(POFILE):      $(POFILES)
	$(RM) $@
	cat $(POFILES)  > $@

install:	all $(ROOTUSRSBINPROG)

lint:		lint_SRCS

clean:
	$(RM) $(OBJECTS)

include ../../Makefile.targ
