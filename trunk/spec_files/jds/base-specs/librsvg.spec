#
# spec file for package librsvg
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         librsvg
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      1 
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Library for SVG support for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/librsvg/2.26/librsvg-%{version}.tar.bz2
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/librsvg
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libxml2_version 2.6.7
%define gtk2_version 2.4.0
%define freetype2_version 2.1.7
%define popt_version 1.7
%define libart_version 2.3.16

Requires:      libxml2 >= %{libxml2_version}
Requires:      gtk2 >= %{gtk2_version}
Requires:      freetype2 >= %{freetype2_version}
Requires:      popt >= %{popt_version}
Requires:      libart_lgpl >= %{libart_version}
Requires:      libpng

BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: freetype2-devel >= %{freetype2_version}
BuildRequires: popt >= %{popt_version}
BuildRequires: libart_lgpl-devel >= %{libart_version}
BuildRequires: libpng-devel

%description
librsvg provides SVG support for GNOME

%package devel
Summary:      Development Library for SVG support for GNOME
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     libxml2-devel >= %{libxml2_version}
Requires:     gtk2-devel >= %{gtk2_version}
Requires:     freetype2-devel >= %{freetype2_version}
Requires:     libart_lgpl-devel >= %{libart_version}

%description devel
librsvg provides SVG support for GNOME

%prep
%setup -q

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
            --libdir=%{_libdir}         \
            --bindir=%{_bindir}         \
	    --sysconfdir=%{_sysconfdir} \
	    --mandir=%{_mandir}		\
	    %{gtk_doc_option}           \
	    --with-html-dir=%{_datadir}/gtk-doc/html/librsvg
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.la
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/loaders/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
mkdir -p %{_sysconfdir}/gtk-2.0
gdk-pixbuf-query-loaders > %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders

%postun
/sbin/ldconfig
gdk-pixbuf-query-loaders > %{_sysconfdir}/gtk-2.0/gdk-pixbuf.loaders

%files
%defattr(-, root, root)
%{_libdir}/*.so.*
%{_libdir}/gtk-2.0/*/engines/libsvg.so
%{_libdir}/gtk-2.0/*/loaders/svg_loader.so
%{_bindir}
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_datadir}/pixmaps

%files devel
%defattr(-, root, root)
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc
%{_includedir}/librsvg-2
%{_datadir}/gtk-doc/html/librsvg

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.22.3.
- Remove librsvg-01-license.diff, fixed upstream.
* Thu Aug 21 2008 - laca@sun.com
- set env variable needed for 64-bit build
* Fri Jun 13 2008 - padraig.obriain@sun.com
- Add librsvg-01-license.diff to prevent gdk-pixbuf-query-loaders crash
* Wed Mar 05 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.22.1.
* Tue Jan 22 2008 - damien.carbery@sun.com
- Bump to 2.20.0.
* Fri Aug 31 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Tue Aug 21 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Jul 24 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Thu Jan 25 2007 - alvaro@sun.com
- librsvg-01-no-def-file.diff removed. It's no longer needed.
* Thu Jan 25 2007 - alvaro@sun.com
- librsvg-02-fixfunc.diff is no longer needed.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Fri Nov 03 2006 - dermot.mccluskey@sun.com
- Bump to 2.16.1.
* Thu Aug 31 2006 - dermot.mccluskey@sun.com
- Bump to 2.16.0.
* Fri Jul 28 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.90.
* Mon Jul 10 2006 - brian.cameron@sun.com
- Bump to 2.14.4.  Add patch to redefine __PRETTY_FUNCTION__ to
  __func__ so it compiles on Solaris.
* Mon Apr 03 2006 - damien.carbery@sun.com
- Bump to 2.14.3.
* Sun Mar 12 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.93.
* Wed Feb  8 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Add patch, 01-no-def-file, so as not to use .def file, to build on Solaris.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Mon Jan 09 2006 - damien.carbery@sun.com
- Remove patch, 01-rsvg-text-void-ret, as the code referenced is gone.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Aug 23 2005 - damien.carbery@sun.com
- Add mozilla build dependency so that mozilla/plugins build.
* Tue Jun 14 2005 - laca@sun.com
- added patch from HEAD for void functions returning values (breaks the build
  with Forte)
* Thu May 19 2005 - laszlo.kovacs@sun.com
- ported to 2.9.5
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add rsvg.1, librsvg-2.3 man pages
* Tue Aug 24 2004 - brian.cameron@sun.com
- Corrected --with-html-dir so it uses %{_datadir}.
* Tue Aug 24 2004 - laszlo.kovacs@sun.com
- removed /usr/share/doc from file list
* Wed Aug 18 2004 - brian.cameron@sun.com
- added patch 2 to fix gtk-doc building.  added --enable-gtk-doc.
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Feb 20 2004 - <matt.keenan@sun.com>
- Updated Distro
* Thu Feb 12 2004 - <niall.power@sun.com>
- added a -uninstalled.pc file patch.
- autotoolize the build stage
* Tue Dec 16 2003 - <glynn.foster@sun.com>
- Update to 2.5.0
* Fri Oct 10 2003 - <laca@sun.com>
- update to 2.4.0
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Tue May 13 2003 - glynn.foster@sun.com
- Initial Sun release
