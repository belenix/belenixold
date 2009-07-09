#
# spec file for package gphoto2
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=8874&atid=108874&aid=
#
Name:         gphoto2
License:      GPL
Group:        Hardware/Other
Version:      2.4.5
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Digital camera utility
Source:       http://kent.dl.sourceforge.net/sourceforge/gphoto/gphoto2-%{version}.tar.bz2
# date:2005-09-30 type:bug owner:dcarbery bugster:6570425
Patch1:       gphoto2-01-gettext.diff
# date:2008-08-01 type:branding owner:mattman
Patch2:       gphoto2-02-man.diff
URL:          http://www.gphoto.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
DocDir:       %{_defaultdocdir}/gphoto2
Autoreqprov:  on

%define libgphoto2_version 2.1.2

Requires:      libgphoto2 >= %{libgphoto2_version}
BuildRequires: libgphoto2 >= %{libgphoto2_version}

%description
gPhoto (GNU Photo) is a commandline tool for previewing, retrieving, and
capturing images from a range of supported digital camerason to your
local harddrive.

(It does not support digital cameras based on the USB storage protocol,
those can be mounted by Linux directly.)

As of this time gPhoto supports around 200 cameras, listed on:

 http://www.gphoto.org/cameras.html

or by running

 gphoto2 --list-cameras

%prep
%setup -q -n gphoto2-%{version}
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

%ifos solaris
glib-gettextize -f
%endif
libtoolize --copy --force
aclocal-1.9 $ACLOCAL_FLAGS -I ./m4m -I ./auto-m4
autoheader
automake-1.9 -a -f
autoconf
PATH="/usr/X11R6/bin:$PATH" CFLAGS="$RPM_OPT_FLAGS" ./configure	\
  --prefix=%{_prefix} 			\
  --mandir=%{_mandir} 			\
  --bindir=%{_bindir} 			\
  --libdir=%{_libdir} 			\
  --includedir=%{_includedir}           \
  --with-cdk-prefix={_prefix}		\
  --with-libintl-prefix=/usr		\
  --with-doc-dir=%{_defaultdocdir}/%{name}
make -j $CPUS INTLLIBS=

%install
make  DESTDIR=$RPM_BUILD_ROOT install

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && [ -d $RPM_BUILD_ROOT ] && rm -rf $RPM_BUILD_ROOT;

%files
%defattr(-,root,root)
%{_bindir}/gphoto2
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_mandir}/man1/*

%changelog 
* Fri Apr 03 2009 - brian.cameron@sun.com
- Bump to 2.4.5.
* Wed Jan 21 2009 - brian.cameron@sun.com
- Bump to 2.4.4.
* Tue Oct 21 2008 - brian.cameron@sun.com
- Bump to 2.4.3.
* Fri Aug 01 2008 - matt.keenan@sun.com
- Add man page attributes patch
* Mon Jul 21 2008 - brian.cameron@sun.com
- Bump to 2.4.2.
* Sat Mar 29 2008 - brian.cameron@sun.com
- Bump to 2.4.1.
* Wed Nov 28 2007 - brian.cameron@sun.com
- Bump to 2.4.0 and add back patch gphoto2-02-fixbuild.diff
* Mon Aug 13 2007 - brian.cameron@sun.com
- Bump back to 2.3.1, since 2.4.0 depends on libltdl which is not
  yet in Nevada (it is a part of libtool).  Will bump back to 2.4.0 once
  libtool is in Nevada.
* Tue Jul 31 2007 - brian.cameron@sun.com
- Bump to 2.4.0.
* Mon Apr  2 2007 - laca@sun.com
- force using automake 1.9
* Tue Feb 13 2007 - brian.cameron@sun.com
- Bump to 2.3.1
* Tue Dec 19 2006 - brian.cameron@sun.com
- Bump to 2.3.0.
* Mon Jul 24 2006 - irene.huang@sun.com
- add option --with-libintl-prefix=/usr
* Web Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 2.2.0.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.1.99.
* Tue Sep 20 2005 - laca@sun.com
- update patches forte-configure and forte-fixes and merge them into one
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.1.6.
* Wed Jun 08 2005 - glynn.foster@sun.com
- Bump to 2.1.5
* Fri Nov 12 2004 - laca@sun.com
- Added --bindir=%{_bindir} so it can be redirected on Solaris
* Thu Oct 07 2004 - ciaran.mcdermott@sun.com
- Backing out Patch4,only applies in linux
- and not in Solaris for unknown reason.
* Thu Oct 07 2004 - ciaran.mcdermott@sun.com
- Recreated gphoto2-04-g11n-alllinguas.diff
* Mon Sep 20 2004 - dermot.mccluskey@sun.com
- Removed patch 04
* Thu Sep 16 2004 - ciaran.mcdermott@sun.com
- Added gphoto2-04-g11n-alllinguas.diff to add hu lingua.
* Tue Aug 24 2004 - laszlo.kovacs@sun.com
- fix man pge installation
* Fri Aug 20 2004 - laszlo.kovacs@sun.com
- added man page to pkg list
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gphoto2-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gphoto2-l10n-po-1.1.tar.bz2
* Tue May 04 2004 - laca@sun.com
- grrr... don't rm -rf $RPM_BUILD_ROOT in %install, do it in %clean
* Mon May 03 2004 - dermot.mccluskey@sun.com
- fixed %install cleanup error
* Wed Apr 14 2004 - brian.cameron@sun.com
- Added $ACLOCAL_FLAGS to aclocal call, needed for Solaris.
* Wed Apr 07 2004 - brian.cameron@sun.com
- Removed -n from %changelog.  It breaks Solaris and Laca recommended
  removing it.
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gphoto2-l10n-po-1.0.tar.bz2
* Wed Feb 04 2004 - matt.keenan@sun.com
- Ported Patch 01 from QS
* Wed Feb 04 2004 - matt.keenan@sun.com
- New tarball 2.1.4 for Cinnabar
* Tue Oct 14 2003 - matt.keenan@sun.com
- New Tarball 2.1.2 for QS
* Wed Jul 16 2003 - matt.keenan@sun.com
- Initial version
