#
# spec file for package libexif-gtk
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=12272&atid=112272&aid=
#
Name:         libexif-gtk
License:      LGPL
Group:        Development/Libraries/C and C++
Version:      0.3.5
Release:      2
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GTK widgets for viewing EXIF information
Source:       http://umn.dl.sourceforge.net/libexif/%{name}-%{version}.tar.bz2
# date:2004-01-16 owner:mattman type:bug bugzilla:1616317
Patch1:       libexif-gtk-01-enable-deprecated.diff
# date:2004-06-02 owner:laca type:bug bugzilla:1616397 bugster:6570425
Patch2:       libexif-gtk-02-gettext.diff
# date:2004-06-02 owner:yippi type:bug bugzilla:1616320
Patch3:       libexif-gtk-03-solaris.diff
# date:2004-06-02 owner:yippi type:feature bugzilla:1643242
Patch4:       libexif-gtk-04-uninstalled-pc.diff
# date:2006-02-21 owner:dcarbery type:bug bugzilla:1394423
Patch5:       libexif-gtk-05-sf-bug-1394423.diff
URL:          http://sourceforge.net/projects/libexif
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
DocDir:       %{_defaultdocdir}/libexif-gtk
Autoreqprov:  on
Prereq:       /sbin/ldconfig


%define libexif_version 0.5.9
Requires:      libexif >= %{libexif_version}
Requires:      gtk2
BuildRequires: libexif >= %{libexif_version}
BuildRequires: gtk2-devel

%description
This library contains GTK widgets for viewing the EXIF informations within
JPEG images created by some types of digital cameras.

%prep 
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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

glib-gettextize -f
libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf
CFLAGS="$CFLAGS $RPM_OPT_FLAGS" 	\
	./configure 			\
		--prefix=%{_prefix} 	\
		--libdir=%{_libdir}	\
		--disable-static

# FIXME: hack: stop the build from looping
touch po/stamp-it

make -j $CPUS

%install
make DESTDIR=${RPM_BUILD_ROOT}/ install-strip
#clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la

#%check
make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/lib*so*
%{_libdir}/pkgconfig/*
%{_includedir}/*
%{_datadir}/locale/*

%changelog -n libexif-gtk
* Wed Apr 16 2008 - damien.carbery@sun.com
- Add 'make check' call after %install.

* Mon Mar 05 2006 - dermot.mccluskey@sun.com
- Correct license to LGPL, as per the source files

* Tue Feb 21 2006 - damien.carbery@sun.com
- Add patch, 05-sf-bug-1394423, to fix configure bug, already logged at sf.net.

* Mon Feb 13 2006 - damien.carbery@sun.com
- Add hack to fix infinite loop problem in po/Makefile.

* Wed Jun 15 2005 - laca@sun.com
- Add more libs to LDADD so that it builds with the new pkgconfig

* Wed Jun 15 2005 - matt.keenan@sun.com
- Bump to 0.3.5

* Wed Jul 13 2004 - niall.power@sun.com
- fix for rpm4 packaging

* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libexif-gtk-l10n-po-1.2.tar.bz2

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Thu Jun 17 2004 - hidetoshi.tajima@sun.com
- Run glib-gettextize and replace po/Makefile.in.in with standard
  ones found in %{_datadir}/glib-2.0/gettext/.

* Wed Jun 06 2004 - brian.cameron@sun.com
- Added needed patches for Solaris.

* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libexif-gtk-l10n-po-1.1.tar.bz2

* Mon Apr 12 2004 - brian.cameron@sun.com
- Add $ACLOCAL_FLAGS to aclocal call, making Solaris more happy.

* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar

* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libexif-gtk-l10n-po-1.0.tar.bz2

* Thu Mar 18 2004 - <matt.keenan@sun.com>
- Added URL Tag

* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added libexif-gtk-03-g11n-potfiles.diff

* Wed Feb 04 2004 - <matt.keenan@sun.com>
- l10n tarball, and patch

* Fri Jan 16 2004 - <matt.keenan@sun.com>
- Enable Deprecated patch

* Tue Oct 14 2003 - <matt.keenan@sun.com>
- Upgrade tarball to 0.3.3 for QS

* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la

* Wed Jul 16 2003 - matt.keenan@sun.com
- Initial version
