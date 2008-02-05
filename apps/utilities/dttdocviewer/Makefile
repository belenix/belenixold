#
#    DTrace Toolkit Documentation Viewer
#
#    This application is free software; you can redistribute it and/or
#    modify it under the terms of the GNU Lesser General Public
#    License as published by the Free Software Foundation; either
#    version 2 of the License, or (at your option) any later version.
#
#    This application is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#    Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public
#    License along with this library; if not, write to the Free Software
#    Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
#
# Copyright 2007 Sun Microsystems, Inc.  All rights reserved.
# Use is subject to license terms.
#
# Author: Moinak Ghosh
#

PKG_CONFIG = /usr/bin/pkg-config
CC=/opt/SUNWspro/bin/cc
CFLAGS=-I/usr/include/gtk-2.0 -I/usr/lib/gtk-2.0/include -I/usr/include/atk-1.0 -I/usr/include/cairo -I/usr/include/pango-1.0 -I/usr/X11/include -I/usr/include/glib-2.0 -I/usr/lib/glib-2.0/include -I/usr/sfw/include -I/usr/sfw/include/freetype2 -I/usr/include/libpng12 -DPACKAGE_DATA_DIR=\"/usr/share\" -DPACKAGE=\"dttdocviewer\"
LDFLAGS=-R/usr/X11/lib -L/usr/X11/lib -lgtk-x11-2.0 -lgdk-x11-2.0 -lXi -lXext -lX11 -latk-1.0 -lgdk_pixbuf-2.0 -lm -lmlib -lpangocairo-1.0 -lfontconfig -lXrandr -lXcursor -lXcomposite -lXdamage -lpango-1.0 -lcairo -lXfixes -lgobject-2.0 -lgmodule-2.0 -lglib-2.0

COMPILE=    $(CC) $(CFLAGS) $(CPPFLAGS) -c
LINK=       $(CC) $(LDFLAGS)
PROG=       dttdocviewer
SOURCES=    support.c interface.c main.c callbacks.c
OBJECTS=    $(SOURCES:.c=.o)

all: $(SOURCES) $(PROG)

$(PROG): $(OBJECTS)
	$(LINK) $(LDFLAGS) support.o interface.o main.o callbacks.o -o $(PROG)

.c.o:
	$(COMPILE) $< -o $@


clean:
	rm -f *.o
	rm -f $(PROG)

install: all
	mkdir -p $(DESTDIR)/usr/bin
	cp -f $(PROG) $(DESTDIR)/usr/bin
	chmod a+rx $(DESTDIR)/usr/bin/$(PROG)

