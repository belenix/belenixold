#
# spec file for package libbonoboui 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         libbonoboui 
License:      LGPL
Group:        System/Libraries/GNOME 
Version:      2.24.1
Release:      2
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Bonobo Base User Interface Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/libbonoboui/2.24/libbonoboui-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# owner:yippi date:2004-11-23 type:branding
# Needed to support /usr/share/gnome/gnome-2.0/ui for backwards compatibility.
Patch1:	      libbonoboui-01-solaris-backcompat.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libgnomecanvas_version 2.6.0
%define libglade_version 2.3.6
%define libbonobo_version 2.6.0
%define libgnome_version 2.6.0

Requires: libgnomecanvas >= %{libgnomecanvas_version}
Requires: libbonobo >= %{libbonobo_version}
Requires: libglade >= %{libglade_version}
Requires: libgnome >= %{libgnome_version}
BuildRequires: libgnomecanvas-devel >= %{libgnomecanvas_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: libgnome-devel >= %{libgnome_version}

%description
libbonoboui is one of the base user interface libraries for the GNOME Desktop, containing
convenient API for writing reusable components.

%package devel
Summary:      Bonobo Base User Interface Development Library
Group:        Development/Libraries/GNOME
Requires:     %name = %version-%release
Requires:     libbonobo-devel >= %{libbonobo_version}

%description devel
libbonoboui is one of the base user interface libraries for the GNOME Desktop, containing
convenient API for writing reusable components.

%prep
%setup -q
%patch1 -p1

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
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS"		\
./configure --prefix=%{_prefix}		\
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir} \
            %{gtk_doc_option}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.a
rm $RPM_BUILD_ROOT%{_libdir}/libglade/2.0/*.la
rm $RPM_BUILD_ROOT%{_datadir}/applications/*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%{_datadir}/locale/*/LC_MESSAGES/libbonoboui-2.0.mo
%{_libdir}/libbonoboui-2*so.*
%{_libdir}/libglade/2.0/libbonobo*so*

%files devel
%{_bindir}/test-moniker
%{_bindir}/bonobo-browser
%{_includedir}/libbonoboui-2.0/*.h
%{_includedir}/libbonoboui-2.0/bonobo/*.h
%{_libdir}/libbonoboui-2*so
%{_libdir}/bonobo-2.0/samples/*
%{_libdir}/bonobo/servers/*.server
%{_datadir}/gnome-2.0/ui/*.xml
%{_libdir}/pkgconfig/*.pc
%{_datadir}/gtk-doc/html/*
%{_mandir}/man3/*.gz

%changelog
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.24.1
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
* Wed Aug 06 2008 - damien.carbery@sun.com
- Bump to 2.23.5. Remove upstream patch, 02-gtk-deprecated.
* Thu Jul 10 2008 - damien.carbery@sun.com
- Add 02-gtk-deprecated to update files for the new gtk+ tarball.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.6.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 2.17.94.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Bump to 2.17.0.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Fri Sep 01 2006 - damien.carbery@sun.com
- Bump to 2.15.1.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.0.
* Wed Mar 15 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Specify --libexecdir in configure to have correct path in CanvDemo.server 
  file.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.1
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 2.13.0.
* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 2.10.1.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.10.0.
* Wed Jun 15 2005 - laca@sun.com
- Add more libs to LDADD so that it builds with the new pkgconfig
* Thu May 19 2005 - balamurali.viswanathan@wipro.com
- Added patch libbonoboui-05-nautilus-crash.diff to fix a nauitlus crash 
  Bug #6250742.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.8.1
* Thu Jan 13 2005 - alvaro.lopez@sun.com
- URL updated.
* Wed Nov 23 2004 - brian.cameron@sun.com
- Added patch 4 to support bonobo UI xml integration point that we
  used in GNOME 2.0.
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc
* Thu Aug 12 2004 - takao.fujiwara@sun.com
- Added libbonoboui-03-g11n-i18n-ui.diff to localize Evolution help menu. 
- Fixed 5078956.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libbonoboui-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- Ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 25 2004 - muktha.narayan@wipro.com
- Added patch libbonoboui-02-gmessage.diff to fix a crash 
  in ggv. Bug #5052487.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libbonoboui-l10n-po-1.1.tar.bz2
* Tue Apr 06 2004 - glynn.foster@sun.com
- Bump to 2.6.0, remove uninstalled pc patch, rename
  potfiles and remove broken g11n-ui patch.
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libbonoboui-l10n-po-1.0.tar.bz2
* Mon Mar 22 2004 - <takao.fujiwara@sun.com>
- Added libbonoboui-03-g11n-i18n-ui.diff to fix 4955030
* Wed Feb 11 2004 - <matt.keenan@sun.com>
- Bump to 2.5.2, add l10n-07 tarball, and manpage.
  Port 02-potfiles_in patch
* Fri Feb 06 2004 - <niall.power@sun.com>
- add ACLOCAL_FLAGS to aclocal invocation
* Tue Jan 13 2004 - <niall.power@sun.com> 2.5.1-1
- Update to 2.5.1
* Thu Oct 09 2003 - <markmc@sun.com> 2.4.0-1
- Update to 2.4.0
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Tue Aug 12 2003 - <markmc@sun.com> 2.2.4-1
- Upgrade to 2.2.4
* Fri Aug 01 2003 - <markmc@sun.com> 2.2.3-1
- Upgrade to 2.2.3
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Tue May 13 2003 - <Laszlo.Kovacs@Sun.COM>
- Create new spec file for libbonoboui
