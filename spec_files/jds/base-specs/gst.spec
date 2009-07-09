#
# spec file for package gstreamer
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:         gstreamer
License:      LGPL v2, Public Domain
Group:        Libraries/Multimedia
Version:      0.10.22
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GStreamer streaming media framework runtime.
Source:       http://gstreamer.freedesktop.org/src/%{name}/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:      l10n-configure.sh
%endif

#owner:laca date:2005-08-11 type:bug bugster:6570425
Patch1:       gst-01-gettext.diff
#owner:yippi date:2009-01-20 type:bug bugzilla:568481 state:upstream
Patch2:       gst-02-makefile.diff
URL:          http://gstreamer.net/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:         /sbin/ldconfig

%define         glib2_version	2.0.1
%define         libxml2_version	2.4.0

Requires:       glib2 >= %{glib2_version}
Requires:       libxml2 >= %{libxml2_version}
Requires:       popt
BuildRequires:  glib2-devel >= %{glib2_version}
BuildRequires:  libxml2-devel >= %{libxml2_version}
BuildRequires:  flex
BuildRequires:  gtk-doc >= 0.7
BuildRequires:  gcc
BuildRequires:  zlib-devel
BuildRequires:  popt
BuildRequires:  pyxml

%description
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

%package devel
Summary:        Libraries/include files for GStreamer streaming media frame
Group:          Development/Libraries
Requires:       %{name} = %{version}
Requires:       glib2-devel >= %{glib2_version}
Requires:       libxml2-devel >= %{libxml2_version}

%description devel
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

This package contains the libraries and includes files necessary to develop
applications and plugins for GStreamer.

%package tools
Summary:        tools for GStreamer streaming media framework.
Group:          Libraries/Multimedia

%description tools
GStreamer is a streaming-media framework, based on graphs of filters which
operate on media data. Applications using this library can do anything
from real-time sound processing to playing videos, and just about anything
else media-related.  Its plugin-based architecture means that new data
types or processing capabilities can be added simply by installing new
plugins.

This package contains the basic command-line tools used for GStreamer, like
gst-launch.  It is split off to allow parallel-installability in the future.

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

glib-gettextize -f
libtoolize --copy --force
intltoolize --copy --force --automake
aclocal -I common/m4 $ACLOCAL_FLAGS

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

autoheader
autoconf
automake -a -c -f
./configure \
  --prefix=%{_prefix} \
  --sysconfdir=%{_sysconfdir} \
  --mandir=%{_mandir}   \
  %{gtk_doc_option}   \
  --disable-tests --disable-examples \
  --program-suffix="" --with-check=no

# FIXME: hack: stop the build from looping
touch po/stamp-it

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/*/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig

%post tools
/sbin/ldconfig

%post devel
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS COPYING README TODO ABOUT-NLS
%{_libdir}/lib*.so.*
%{_libdir}/gstreamer-*/libgst*.so*
%{_datadir}/locale/*/LC_MESSAGES/*.mo

%files devel
%defattr(-, root, root)
%{_includedir}/*
%{_libdir}/lib*.so
%{_libdir}/pkgconfig
%{_datadir}/aclocal
%{_datadir}/gtk-doc
%{_mandir}/man3

%files tools
%{_bindir}/gst-*
%{_mandir}/man1/gst-*

%changelog
* Mon Jan 19 2009 - brian.cameron@sun.com
- Bump to 0.10.22.
* Sat Oct 04 2008 - christian.kelly@sun.com
- Bump to 0.10.21.
* Thu Jun 19 2008 - damien.carbery@sun.com
- Bump to 0.10.20.
* Mon Apr 07 2008 - damien.carbery@sun.com
- Bump to 0.10.19.
* Thu Mar 20 2008 - brian.cameron@sun.com
- Bump to 0.10.18.
* Mon Jan 30 2008 - jan.schmidt@sun.com
- Bump to 0.10.17 paper bag release.
* Mon Jan 28 2008 - brian.cameron@sun.com
- Bump to 0.10.16.
* Fri Nov 16 2007 - damien.carbery@sun.com
- Bump to 0.10.15.
* Fri Aug 03 2007 - damien.carbery@sun.com
- Bump to 0.10.14.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 0.10.13.
* Wed Mar 21 2007 - damien.carbery@sun.com
- Add --with-check=no to configure so as not to pick up SFEcheck package. Build
  breaks when it finds the package.
* Thu Mar 07 2007 - damien.carbery@sun.com
- Bump to 0.10.12.
* Sat Mar 04 2007 - damien.carbery@sun.com
- Add intltoolize call to expand MSGFMT_OPTS.
* Tue Feb 06 2006 - brian.cameron@sun.com
- Remove unneeded patch.
* Mon Dec 11 2006 - brian.cameron@sun.com
- Remove nofork patch since this is now fixed upstream.
* Thu Dec  7 2006 - brian.cameron@sun.com
- Bump to 0.10.11
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Oct 16 2006 - damien.carbery@sun.com
- Remove the '-f' from the 'rm *.la *.a' lines so that any changes to the
  module source will be seen as a build error and action can be taken.
* Mon Sep 11 2006 - brian.cameron@sun.com
- Bump to 0.10.9.
* Tue Aug 8 2006 - yandong.yao@sun.com
- Add l10n-configure.sh script for l10n pkgs
* Tue Jun 13 2006 - brian.cameron@sun.com
- Bump to 0.10.8.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 0.10.4.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Bump to 0.10.3.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Add hack to fix infinite loop problem in po/Makefile. 
* Sun Jan 22 2006 - damien.carbery@sun.com
- Add patch, 02-solaris-resolv, to add '-lresolv' so inet_aton function found.
* Mon Jan 09 2006 - brian.cameron@sun.com
- Bump to 0.10.1  The packaging will need some work if someone wants to build
  this for Linux.
* Tue Sep 20 2005 - brian.cameron@sun.com
- Bump to 0.8.11.
* Thu Sep 08 2005 - damien.carbery@sun.com
- Unbump back to 0.8.10 as 0.9.x is not in gnome2.12.
* Wed Sep 07 2005 - damien.carbery@sun.com
- Bump to 0.9.2. Update %files.
* Mon Jun 06 2005 - brian.cameron@sun.com
- Removed patch for modifying uninstalled-pc file since it
  is no longer needed.
* Wed May 11 2005 - brian.cameron@sun.com
- Updated to call automake, now needed.
* Wed Nov 17 2004 - matt.keenan@sun.com
- #6195855, install correct man page
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gst-*, libgst*
* Wed Sep 29 2004 - takao.fujiwara@sun.com
- Update gst-02-g11n-potfiles.diff
- Update gst-03-gettext.diff to fix 5068957
- Remove gst-04-g11n-potfiles.diff
* Mon Aug 30 2004 - takao.fujiwara@sun.com
- Add gst-04-g11n-potfiles.diff
* Sun Aug 29 2004 - laca@sun.com
- Now packaging gtk-docs.
* Tue Aug 23 2004 - brian.cameron@sun.com
- Now building gtk-docs.
* Fri Aug 20 2004 - brian.cameron@sun.com
- Fixed typo.
* Fri Aug 20 2004 - laszlo.kovacs@sun.com
- gst-xmlinspect man page packaged
* Mon Aug 09 2004 - brian.cameron@sun.com
- Corrected Linux packaging.  Corrected Release to 2 since
  this is the 2nd change after bumping the release last
  Thursday.
* Thu Jul 29 2004 - brian.cameron@sun.com
- Bumped revision of gstreamer to 0.8.4, making patches 4 and 5 go away
  since they were integrated into CVS head.
* Fri Jul 15 2004 - brian.cameron@sun.com
- Added patch to change the default scheduler to basicgthread which
  works better than opt for audio and opt doesn't work at all for
  video on Solaris.
* Mon Jul 12 2004 - niall.power@sun.com
- ported to rpm4, pkg'd some missing files
* Thu Jul 08 2004 - damien.donlon@sun.com
- Adding gst-l10n-po-1.2.tar.bz2 l10n content
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri May 14 2004 - brian.cameron@sun.com
- added patch 03 from CVS head to support aligned memory access,
  needed for Solaris.
* Wed May 12 2004 - ghee.teo@sun.com
- Updated to tarball 0.8.1 version as per Laca and yippi request.
* Mon May 10 2004 - laca@sun.com
- autotools-jdsize to fix Makefile problem
* Thu May 02 2004 - brian.cameron@sun.com
- Add glib-gettextize, aclocal, and autoconf calls
  so that gettext patches to configure.in/configure.ac
  get included.  Added patches mentioned above to
  appropriate spec files.
* Mon Apr 05 2004 - ghee.teo@sun.com
- changed majorminor version to 0.8
* Fri Apr 02 2004 - ghee.teo@sun.com
- Upgraded tarball to 0.8.0 which is released for 2.6
* Tue Mar 16 2004 - takao.fujiwara@sun.com
- Added gst-02-g11n-potfiles.diff
* Mon Mar 08 2004 - niall.power@sun.com
- add patch to fix gst-*-uninstslled.pc Cflags.
- disable docs build on Solaris for now (causes gthread error) 
* Fri Feb 13 2004 - matt.keenan@sun.com
- Bump to 0.7.4, update tools files
* Mon Jan 05 2004 - ghee.teo@sun.com
- Fixed the postinstall problem. Basically, gst has allowed for parallel
  installed and had decided to have program named by
  /usr/bin/gst-regsiter-<majorminor>
  since we do not have parallel installed on our distro, so configure with
  --program-suffix="" to remove the version number.
* Wed Dec 17 2003 - glynn.foster@sun.com
- bump to 0.7.2
* Fri Oct 10 2003 - ghee.teo@sun.com
- Removed the patch 01 which is already in 0.63 release of gstreamer
  updtaed spec file to build for Qs. and also include a patch from Bala
  as part of the fix to 4880305.
* Fri Oct 03 2003 - ghee.teo@sun.com
- Pulled out two patches from the 0.63 release that fixes a infinite loop
  and a crash, bugzilla 120741 and 104829.
* Wed Jul 23 2003 - ghee.teo@sun.com
- Added a patch to disable putbits which uses a potential patent ridden
  issue with mpeg
* Tue May 14 2003 - ghee.teo@sun.com
- initial release version for gstreamer
