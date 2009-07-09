#
# spec file for package libgtop 
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: niall
#
Name:         libgtop 
License:      GPL v2
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      libgtop System Information Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgtop/2.26/libgtop-%{version}.tar.bz2
URL:          http://www.gnome.org
# The G_GNUC_INTERNAL portions of the 01-solaris patch are in bugzilla 440678.
#owner:niall date:2006-11-15 type:feature
#This patch makes libgtop run on Solaris
Patch1:       libgtop-01-solaris.diff
#owner:bandy date:2009-03-24 type:bug bugzilla:548095 doo:3402
Patch2:       libgtop-02-link.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/dir
Autoreqprov:  on

%define glib2_version 2.4.0

Requires:	glib2 >= %{glib2_version}
BuildRequires:	glib2-devel >= %{glib2_version}
Requires:	libgnome
BuildRequires:	libgnome

%description
libgtop is a library that fetches information about the running system such as
cpu and memory usage, active processes etc.

On Linux systems, these information are taken directly from the /proc
filesystem while on other systems a server is used to read those
information from /dev/kmem or whatever.

%package devel
Summary:      libgtop System Information Development Library
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     glib2-devel >= %{glib2_version}

%description devel
libgtop is a library that fetches information about the running system such as
cpu and memory usage, active processes etc.

On Linux systems, these information are taken directly from the /proc
filesystem while on other systems a server is used to read those
information from /dev/kmem or whatever.

%prep
%setup -q
%patch1 -p1
%patch2 -p1

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

aclocal $ACLOCAL_FLAGS -I .
autoconf
CFLAG="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
#remove unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_prefix}/info

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/libgtop-2.0.mo
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/libgtop-2.0
%{_libdir}/pkgconfig/libgtop-2.0.pc
%{_libdir}/*.so

%changelog
* Mon Mar 24 2009 - andras.barna@gmail.com
- add libgtop-02-link.diff, fixes d.o.o#3402
* Mon Mar 23 2009 - niall.power@sun.com
- Take ownership of spec file + patches
* Mon Mar 02 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Tue Sep 09 2008 - patrick.ale@gmail.com
- Correct download URL

* Mon Jan 21 2007 - damien.carbery@sun.com
- Revert to 2.20.1 because of build issues and module owner choosing not to
  bump because of dependency issues with gnome-system-monitor.
* Thu Jan 17 2007 - damien.carbery@sun.com
- Bump to 2.21.5.
* Thu Jan 10 2007 - damien.carbery@sun.com
- Call aclocal and autoconf to pick up the modified intltool.m4.
* Tue Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.19.92.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4. Remove upstream patch, 02-pid_t-type.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Add patch, 02-pid_t-type, to fix #444815.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Mon May 19 2007 - hua.zhang@sun.com
- Bump to 2.19.2
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.14.8.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.14.7.
* Mon Jan 15 2007 - damien.carbery@sun.com
- Bump to 2.14.6.
* Tue Dec 05 2006 - damien.carbery@sun.com
- Bump to 2.14.5.
* Thu Nov 16 2006 - hua.zhang@sun.com
- add patch comments.
* Tue Sep 26 2006 - damien.carbery@sun.com
- Bump to 2.14.4.
* Wed Sep 06 2006 - damien.carbery@sun.com
- Bump to 2.14.3.
* Fri Jul 28 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Wed July 19 2006 - hua.zhang@sun.com
- add one patch so that libgtop can be installed at Solaris,
  also I fix some bugs 
* Fri Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Jan 24 2006 - damien.carbery@sun.com
- Bump to 2.13.3.
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.2
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 2.10.2
* Wed May 18 2005 - glynn.foster@sun.com
- Bump to 2.10.1
* Wed Sep 01 2004 - laszlo.kovacs@sun.com
- remove all info files
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libgtop-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libgtop-l10n-po-1.1.tar.bz2
* Thu Apr 08 2004 - <niall.power@sun.com>
- bump to 2.6.0
* Wed Feb 11 2004 - <matt.keenan@sun.com>
- Upped l10n to 0.7
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- Add dependency on libgnome
* Tue Dec 16 2003 - <glynn.foster@sun.com>
- Bump to 2.5.0 and merge patches.
* Tue Oct 14 2003 - <niall.power@sun.com>
- update to version 2.0.5, reset release
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Tue May 13 2003 - Laszlo.Kovacs@Sun.COM
- Initial Sun release
