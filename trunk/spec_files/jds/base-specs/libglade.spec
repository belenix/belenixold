#
# spec file for package libglade
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         libglade
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.6.4
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Library for loading GLADE interfaces at runtime
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.6/%{name}-%{version}.tar.bz2
URL:          http://www.daa.com.au/~james/gnome/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.5.0
%define libxml2_version 2.6.7
%define python_xml_version 2.3.3 

Requires: gtk2 >= %{gtk2_version}
Requires: libxml2 >= %{libxml2_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: python-xml >= %{python_xml_version}

%description
This library allows you to load glade interface files in a program at runtime.

%package devel
Summary:      Development library for loading GLADE interfaces at runtime
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     gtk2-devel >= %{gtk2_version}
Requires:     libxml2-devel >= %{libxml2_version}
Requires:     python-xml >= %{python_xml_version}

%description devel
This library allows you to load glade interface files in a program at runtime.

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


CONFLAGS="--prefix=%{_prefix}"
gtkdocize
libtoolize --force
aclocal $ACLOCAL_FLAGS -I ./m4
autoheader
automake -a -c -f
autoconf
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}		\
            --sysconfdir=%{_sysconfdir} \
            --libdir=%{_libdir}         \
            --bindir=%{_bindir}         \
            %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files 
%{_libdir}/lib*.so.*

%files devel
%defattr(-, root, root)
%{_bindir}
%{_libdir}/lib*.so
%{_includedir}/libglade-2.0/
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/libglade
%{_datadir}/xml/libglade
%{_mandir}/man3/*

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 2.6.4
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.6.3
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.6.2. Remove upstream patch, 01-gtk-tooltips.
* Tue Jul 24 2007 - damien.carbery@sun.com
- Add upstream patch, 01-gtk-tooltips, to fix build failure. Bugzilla: 455566.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.6.1.
* Thu Mar 15 2007 - laca@sun.com
- convert to new style of building multiple ISAs as per docs/multi-ISA.txt
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Thu Jul 20 2006 - damien.carbery@sun.com
- Bump to 2.6.0.
* Wed Aug 24 2005 - damien.carbery@sun.com
- Add _bindir to %files devel to pick up libglade-convert.
* Fri May 06 2005 - brian.cameron@sun.com
- Add "-I ./m4" to the ACLOCAL_FLAGS since it is needed to build
  on Solaris.
* Fri May 05 2005 - glynn.foster@sun.com
- Bump to 2.5.1
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Sat Oct 02 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Wed Jul 07 2004 - niall.power@sun.com
- Ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue Mar 16 2004 - <glynn.foster@sun.com>
- Bump to 2.3.6
* Wed Feb 25 2004 - <niall.power@sun.com>
- use the jds versions of the autotools
* Wed Feb 25 2004 - <laca@sun.com>
- autotoolize
* Wed Feb 18 2004 - <matt.keenan@sun.com>
- Bump to 2.3.2
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Bump to 2.3.1
* Mon Oct 6 2003 - <laszlo.kovacs@sun.com>
- upped some dep version numbers
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Tue May 13 2003 - matt.keenan@sun.com
- Initial Sun Spec File
