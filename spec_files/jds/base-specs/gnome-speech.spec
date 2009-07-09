#
# spec file for package gnome-speech
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
Name:         gnome-speech
License:      LGPL v2
Group:        System/Libraries
Version:      0.4.25
Release:      201
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME text-to-speech engine
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/0.4/%{name}-%{version}.tar.bz2
# date:2008-08-15 owner:ww36193 type:bug
Patch1:       gnome-speech-01-espeak.diff
URL:          http://developer.gnome.org/projects/gap/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:	      /sbin/ldconfig

%define libbonobo_version 2.4.0
%define java_access_bridge_version 1.4.6
%define freetts_version 1.2.1

BuildRequires: jdk
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: java-access-bridge >= %{java_access_bridge_version}
BuildRequires: freetts >= %{freetts_version}
Requires:      jdk
Requires:      libbonobo >= %{libbonobo_version}
Requires:      freetts >= %{freetts_version}

%description
gnome-speech module is the GNOME text-to-speech engine.

%package devel
Summary:      GNOME text-to-speech engine
Group:        Development/System/Libraries
Autoreqprov:  on
Requires:     %name = %version
Requires:     libbonobo-devel >= %{libbonobo_version}

%description devel
gnome-speech module is the GNOME text-to-speech engine.

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

%if %option_with_java
%ifos solaris
export CFLAGS="-I/usr/jdk/jdk1.5.0/include -I/usr/jdk/jdk1.5.0/include/solaris $RPM_OPT_FLAGS"			\
export LDFLAGS="-Wl,-zcombreloc -Wl,-Bdirect"
%else
%define jdk_version 1.5.0_03
export PATH="/usr/java/jdk%{jdk_version}/bin:$PATH"
export CFLAGS="-I/usr/java/jdk%{jdk_version}/include -I/usr/java/jdk%{jdk_version}include/linux $RPM_OPT_FLAGS"			\
%endif
%define java_home_option
%else
%define java_home_option --with-java-home=/dont/find/me --without-freetts-dir
%endif

libtoolize -f
aclocal $ACLOCAL_FLAGS
automake
autoconf
./configure --prefix=%{_prefix}			\
            --sysconfdir=%{_sysconfdir}		\
            --mandir=%{_mandir}			\
            --with-freetts-dir=%{_datadir}/lib/freetts \
            %java_home_option
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/orbit-2.0/*.la
rm -f $RPM_BUILD_ROOT%{_bindir}/theta-synthesis-driver
rm -f $RPM_BUILD_ROOT%{_libdir}/bonobo/servers/GNOME_Speech_SynthesisDriver_Theta.server

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/festival-synthesis-driver
%{_bindir}/freetts-synthesis-driver
%{_bindir}/test-speech
%{_libdir}/bonobo/servers/*
%{_libdir}/orbit-2.0/*.so
%{_libdir}/*.so*
%{_datadir}/jar/*.jar
%{_datadir}/gnome-speech
%{_datadir}/idl/gnome-speech-1.0/*

%files devel
%defattr(-,root,root)
%{_includedir}/gnome-speech-1.0/*
%{_libdir}/pkgconfig/*.pc

%changelog
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 0.4.25
* Fri Feb 06 2009 - li.yuan@sun.com
- Bump to 0.4.23. Run libtoolize before aclocal.
* Wed Nov 05 2008 - li.yuan@sun.com
- Change copyright information.
* Mon Aug 18 2008 - william.walker@sun.com
- Handle the fallout of porting eSpeak to SunStudio.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 0.4.21.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 0.4.20.
* Fri Apr 18 2008 - damien.carbery@sun.com
- Bump to 0.4.19.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 0.4.18.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 0.4.17.
* Fri Sep 28 2007 - laca@sun.com
- disable java stuff if the --without-java option is used
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 0.4.16.
* Mon Jul 09 2007 - damien.carbery@sun.com
- Bump to 0.4.15.
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 0.4.14.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 0.4.13.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 0.4.12.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 0.4.11.
* Tue Feb 27 2007 - damien.carbery@sun.com
- Bump to 0.4.10.
* Mon Feb 12 2007 - damien.carbery@sun.com
- Bump to 0.4.9.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 0.4.8.
* Thu Dec 14 2006 - damien.carbery@sun.com
- Bump to 0.4.7.
* Mon Nov 06 2006 - damien.carbery@sun.com
- Bump to 0.4.6.
* Tue Aug 29 2006 - damien.carbery@sun.com
- Bump to 0.4.5.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 0.4.4.
* Mon Aug 07 2006 - damien.carbery@sun.com
- Update to 0.4.3
* Mon Jul 24 2006 - damien.carbery@sun.com
- Update to 0.4.2
* Wed Jul 12 2006 - william.walker@sun.com
- Update to 0.4.1
* Wed Jun 14 2006 - william.walker@sun.com
- Add patch for festival core dump (see bugzilla bug 341405)
* Thu Feb 23 2006 - william.walker@sun.com
- Bump to 0.3.10
* Mon Nov 14 2005 - william.walker@sun.com
- Bump to 0.3.9
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 0.3.8
* Tue Aug 23 2005 - damien.carbery@sun.com
- Add variable to make updating JDK version easier.
* Tue May 10 2005 - bill.haneman@sun.com
- Upgrade to gnome-speech 0.3.7; completes fix for bug #6216633.
- Remove unnecessary patch 1 which is now in the tarball.
- Remove Theta drivers if they happen to have been built.
* Mon May 09 2005 - dermot.mccluskey@sun.com
- New jdk (1.5.0_03)
* Mon Feb 28 2005 - william.walker@sun.com
- Upgrade to FreeTTS 1.2.1, fix for bug #6228329.
* Fri Oct 08 2004 - bill.haneman@sun.com
- Added patch gnome-speech-01-freetts-perf.diff, part of fix for bug
  #5087408.
* Mon Sep 20 2004 - dermotm.mccluskey@sun.com
- new path for JDK 1.5.0
* Mon Aug 30 2004 - bill.haneman@sun.com
- Removed patch (it's in CVS now), and bumped to 0.3.5.
* Wed Aug 18 2004 - brian.cameron@sun.com
- removed --disable-gtk-doc since this isn't an option this module's
  configure takes.
* Thu Jul 22 2004 - bill.haneman@sun.com
- Add patch to fix CLASSPATH in freetts-synthesis-driver script.
  (Please remove patch when upgrading to gnome-speech-0.3.4)
* Thu Jul 22 2004 - damien.carbery@sun.com
- Remove source1 tarball. Incorrectly overwrites source with old files.
* Mon Jul 12 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Thu Jun 10 2004 - bill.haneman@sun.com
- Upgrade to version 0.3.3, depend on FreeTTS 1.2 beta.
* Tue Jun 01 2004 - damien.carbery@sun.com
- Correct JDK path in CFLAGS for Solaris.
* Sun May 30 2004 - dermot.mccluskey
- new JDK
* Mon May 03 2004 - dermot.mccluskey@sun.com
- moved Java to 1.5.0
* Thu Apr 15 2004 - damien.carbery@sun.com
- Move bin and jar files from devel to root rpm.
* Mon Mar 15 2004 - damien.carbery@sun.com
- Add JDK path to CFLAGS and PATH for Linux.
* Thu Mar 11 2004 - damien.carbery@sun.com
- Bump ver to 1.3.2. Reset release. Add --with-freetts-dir configure switch.
- Add files created for freetts support.
* Tue Mar 02 2004 - damien.carbery@sun.com
- Correct line for .so files - was omitting libgnomespeech.so.
* Tue Feb 24 2004 - damien.carbery@sun.com
- Created new spec file for gnome-speech
