#
# spec file for package libgphoto2
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=8874&atid=108874&aid=
#
Name:         libgphoto2
License:      LGPL
Group:        Library/Hardware/Other
Version:      2.4.5
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Digital camera library
Source:       http://superb-west.dl.sourceforge.net/sourceforge/gphoto/libgphoto2-%{version}.tar.bz2
Source1:      usermap.gphoto
Source2:      usbcam
# date:2004-04-08 type:bug owner:laca bugster:6570425
Patch1:       libgphoto2-01-gettext.diff
# date:2007-04-17 type:branding owner:jerrytan
Patch2:       libgphoto2-02-nousb.diff
# date:2008-08-01 type:branding owner:mattman
Patch3:       libgphoto2-03-man.diff
URL:          http://www.gphoto.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
DocDir:       %{_defaultdocdir}/libgphoto2
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Requires:     hotplug

%description
gPhoto (GNU Photo) is a set of libraries for previewing, retrieving, and capturing images from a range of supported digital camerason to your local harddrive.

(It does not support digital cameras based on the USB storage protocol,
those can be mounted by Linux directly.)

As of this time gPhoto supports around 200 cameras, listed on:

 http://www.gphoto.org/cameras.html

or by running

 gphoto2 --list-cameras

%prep
%setup -q
%ifos solaris
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1

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
#%{?suse_update_config:%{suse_update_config -f . libgphoto2_port}}
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS -I ./m4m -I ./auto-m4 
automake -a -f
autoconf
cd libgphoto2_port
%ifos solaris
glib-gettextize -f
%endif
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS -I ./m4 -I ./auto-m4
automake -a -f
autoconf
cd ..
%define libusb_option "--with-libusb=/usr/sfw"

PATH="/usr/X11R6/bin:$PATH" CFLAGS="$RPM_OPT_FLAGS -fPIC" ./configure	\
  --prefix=%{_prefix} 	\
  --mandir=%{_mandir} 	\
  --bindir=%{_bindir} 	\
  --libdir=%{_libdir} 	\
  --includedir=%{_includedir} \
  --with-doc-dir=%{_defaultdocdir}/%{name} \
  --disable-static %{libusb_option}
make -j $CPUS INTLLIBS=

%install
export LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
make DESTDIR=$RPM_BUILD_ROOT install
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/usb/
cp %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/usb/usbcam.usermap
install -c -m 755 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/hotplug/usb/usbcam

rm $RPM_BUILD_ROOT%{_libdir}/libgphoto2/*/*.la
rm $RPM_BUILD_ROOT%{_libdir}/libgphoto2_port/*/*.la

# Clean up unpackaged files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Note I filed bug 1906579 regarding the fact that Solaris does not support
# udev.  I suggest that a # configure option be added to disable installing
# these udev files.
rm -rf $RPM_BUILD_ROOT%{_libdir}/udev
rm -f $RPM_BUILD_ROOT%{_libdir}/libgphoto2/print-camera-list

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_includedir}/gphoto2
%dir %{_defaultdocdir}/%{name}
%{_defaultdocdir}/%{name}/*
%{_datadir}/libgphoto2
%{_bindir}/gphoto2-config
%{_bindir}/gphoto2-port-config
%{_libdir}/libgphoto2.*so*
%{_libdir}/libgphoto2/*/*.so
%{_libdir}/libgphoto2_port.*
%{_libdir}/libgphoto2_port/*/*.so
%{_libdir}/libgphoto2/print-usb-usermap
%{_libdir}/pkgconfig/libgphoto2.pc
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_mandir}/man3/
%{_sysconfdir}/hotplug/usb/*

%changelog -n libgphoto2
* Fri Apr 03 2009 - brian.cameron@sun.com
- Bump to 2.4.5.
* Wed Jan 21 2009 - brian.cameron@sun.com
- Bump to 2.4.4.
* Tue Oct 21 2008 - brian.cameron@sun.com
- Bump to 2.4.3.  Remove upstream patch libgphoto2-03-packed.diff.  Add new
  patch libgphoto2-04-smal.diff to address compile issue.
* Fri Aug 01 2008 - matt.keenan@sun.com
- Add Attributes man page patches
* Mon Jul 21 2008 - brian.cameron@sun.com
- Bump to 2.4.2.  Added new patch libgphoto2-03-packed.diff to address
  SourceForge Tracker bug id #2023814.
* Sat Mar 29 2008 - brian.cameron@sun.com
- Bump to 2.4.1.
* Mon Mar 03 2007 - matt.keenan@sun.com
- Remove udev files as udev not supported on solaris
* Wed Nov 28 2007 - brian.cameron@sun.com
- Bump to 2.4.0, remove upstream patches and add new needed patches.
* Mon Aug 13 2007 - brian.cameron@sun.com
- Bump back to 2.3.1, since 2.4.0 depends on libltdl which is not
  yet in Nevada (it is a part of libtool).  Will bump back to 2.4.0 once
  libtool is in Nevada.
* Tue Jul 31 2007 - brian.cameron@sun.com
- Bump to 2.4.0.  Now sierra driver builds!  Remove upstream patches
  and add new patches to fix new issues.
* Fri Mar 30 2007 - laca@sun.com
- add patch iconv-UCS-2.diff, fixes 6536628
* Tue Feb 13 2007 - brian.cameron@sun.com
- Bump to 2.3.1.
* Tue Dec 19 2006 - brian.cameron@sunc.om
- Bump to 2.3.0.  This fixes problem with libgphoto needing deprecated
  dbus interface.  Add new drivers and a patch to fix compile issue with
  the new mars driver (we were not building this before).  Still can't
  compile sierra driver with our compiler.  Fix patches to work with
  latest build.  Fix uninstalled pc file so that the version number is
  not hardcoded.  Instead install pc.in file and build with the correct
  version.
* Mon Oct 16 2006 - damien.carbery@sun.com
- Remove the '-f' from the 'rm *.la *.a' lines so that any changes to the
  module source will be seen as a build error and action can be taken.
* Mon Jul 24 2006 irene.huang@sun.com
- Add patch libgphoto2-05-dummy.diff
* Web Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 2.2.1.
* Thu May 11 2006 - laca@sun.com
- add patch pragma-pack.diff
* Thu Mar  9 2006 - damien.carbery@sun.com
- Add patch, 03-solaris-mntent, to port mntent code to Solaris.
* Wed Jan 25 2006 - Brian.Cameron@sun.com
- Set LIBUSB_LIBS and LIBUSB_CFLAGS which makes the libgphoto2_port configure
  happier.  For some reason just calling with --with-libusb isn't enough.  The
  build still fails when compiling libgphoto2_port/disk.c because Solaris does
  not have mntent.h, but this gets the build farther along.  
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.1.99.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.1.6.
* Wed Feb 09 2005 - alvaro.lopez@sun.com
- Version updated to 2.1.5
- Patches 2 and 4 are not longer needed:
  libgphoto2-02-fix-konica.diff, libgphoto2-04-pc.diff
- Renamed path 5 as patch 2: libgphoto2-05-g11n-potfiles.diff ->
  libgphoto2-02-g11n-potfiles.diff
* Fri Nov 12 2004 - laca@sun.com
- added --bindir=%{_bindir} so it can be redirected on Solaris
* Wed Sep 15 2004 - yuriy.kuznetsov@sun.com
- Added libgphoto2-05-g11n-potfiles.diff
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libgphoto2-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri May 28 2004 - brian.cameron@sun.com
- Added patch 04, so that gtkam can build on Solaris.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libgphoto2-l10n-po-1.1.tar.bz2
* Thu Apr 15 2004 - brian.cameron@sun.com
- Only apply patch01 on Solaris since it is causing problems for
  Linux.
* Wed Apr 14 2004 - brian.cameron@sun.com
- Add glib-gettextize -f when running configure in the
  libgphoto2_port directory. 
* Thu Apr 08 2004 - brian.cameron@sun.com
- Avoid building sierra driver on Solaris, since it doesn't
  build with Forte.  Add needed 02 patch.
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libgphoto2-l10n-po-1.0.tar.bz2
* Wed Feb 04 2004 - <matt.keenan@sun.com>
- New Tarball 2.1.4, added l10n tarball
- Remove patch: libgphoto2-01-potfiles-in.diff
* Tue Oct 14 2003 - <matt.keenan@sun.com>
- New Tarball 2.1.2 for QS
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Wed Jul 23 2003 - michael.twomey@sun.com
- Fixing POTFILES.in
* Wed Jul 16 2003 - matt.keenan@sun.com
- Initial Spec File
