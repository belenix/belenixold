#
# spec file for package libexif
#
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
Name:         libexif
URL:          http://libexif.sourceforge.net
License:      LGPL
Group:        Development/Libraries/C and C++
Summary:      An EXIF tag parsing library for digital cameras
Version:      0.6.17
Release:      1
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Source0:      http://kent.dl.sourceforge.net/sourceforge/libexif/%{name}-%{version}.tar.bz2
Source1:      l10n-configure.sh
URL:          http://libexif.sourceforge.net/

%description
This library is used to parse EXIF information from JPEGs created by
digital cameras.

%prep 
%setup -q

bash -x %SOURCE1 --enable-sun-linguas

%build
libtoolize --force
aclocal -I m4m $ACLOCAL_FLAGS 
autoconf
CFLAGS="$CFLAGS $RPM_OPT_FLAGS" 	\
	./configure 			\
		--prefix=%{_prefix}	\
		--libdir=%{_libdir}	\
		--disable-static

cat po/Makefile | sed 's|@MKINSTALLDIRS@|\$(top_srcdir)/mkinstalldirs|' > po/Makefile.new
cp po/Makefile.new po/Makefile

make

%install
# we don't have doxygen and the Makefile incorrectly deals with this
touch doc/install-apidocs
touch doc/install-apidocs-internals
make DESTDIR=${RPM_BUILD_ROOT} install

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root)
%doc README AUTHORS INSTALL ChangeLog COPYING 
%{_libdir}/lib*
%{_libdir}/pkgconfig/*
%{_includedir}/libexif/*
%{_datadir}/share/locale/*/LC_MESSAGES/libexif*.mo

%changelog -n libexif
* Wed Jan 07 2009 - christian.kelly@sun.com
- Remove patches/libexif-01-security.diff.
* Tue Dec 09 2008 - dave.lin@sun.com
- Bump to 0.6.17.
* Fri Jan 18 2007 - padraig.obriain@sun.com
- Add patch 01-security for bugster 6652301
* Mon Nov 05 2007 - brian.cameron@sun.com
- Bump to 0.6.16
* Mon Dec 11 2006 - laca@sun.com
- delete patch no-docs.diff, it's not really necessary, instead add two
  touch commands in %install
* Tue May 02 2006 - damien.carbery@sun.com
- Remove unneeded intltoolize call.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 0.6.13.
- Add patch, 01-no-docs, to skip building docs; update aclocal dir.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Add hack to fix infinite loop problem in po/Makefile.
* Wed Jan 04 2006 - damien.carbery@sun.com
- Remove unneeded patch. Failed to build even after rework.
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 0.6.12. Add m4 dir to aclocal call for needed macro.
* Wed Aug 06 2003 - meissner@suse.de
- Upgreaded to upstream 0.5.12:
- fixed endless loops and crashes on invalid exif data.
- translation updates.
* Mon Jul 21 2003 - meissner@suse.de
- Upgraded to upstream 0.5.10.
* Tue May 13 2003 - meissner@suse.de
- Upgraded to current CVS 0.5.9 (just some bugfixes).
- Package translations too.
* Wed Jan 08 2003 - meissner@suse.de
- Upgraded to upstream 0.5.9.
* Mon Dec 02 2002 - meissner@suse.de
- Upgraded to upstream 0.5.7.
* Mon Nov 18 2002 - meissner@suse.de
- Upgraded to 0.5.6 in preparation of gphoto2-2.1.1.
* Wed Jul 24 2002 - meissner@suse.de
- Upgraded to 0.5.3. Do not include static libraries.
* Mon Feb 11 2002 - meissner@suse.de
- make sure we do not include -I/usr/include into the cflags got from pkgconfig
  or we confuse gcc 3 -Wall -Werror
* Mon Feb 04 2002 - meissner@suse.de
- JPEG/EXIF tag parsing library for use by gphoto / gtkam
  (EXIF tags store EXtended InFormation of images taking by digital cameras)
