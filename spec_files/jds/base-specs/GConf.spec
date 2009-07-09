#
# spec file for package GConf
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: stephen
#
Name:         GConf
License:      LGPL
Group:        System/Libraries/GNOME
Provides:     GConf
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Configuration Framework
Source:       http://ftp.gnome.org/pub/GNOME/sources/GConf/2.26/GConf-%{version}.tar.bz2
%if %build_l10n
Source1:      l10n-configure.sh
%endif
#owner:stephen date:2004-08-02 type:bug bugster:5042863 bugzilla:100378
Patch1:       GConf-01-g11n-locale-alias.diff
#owner:laca date:2006-06-29 type:feature
Patch2:       GConf-02-GCONF_BACKEND_DIR.diff
#owner:yippi date:2008-10-09 type:bug bugzilla:555745
Patch3:       GConf-03-user-specific-dbus.diff
#owner:stephen date:2009-03-20 type:bug bugzilla:7402
Patch4:       GConf-04-no-defaults-service.diff
URL:	      http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define gtk2_version 2.4.0
%define libxml2_version 2.6.7
%define ORBit2_version 2.10.1
%define gtk_doc_version 1.1
%define popt_version 1.7

Requires: gtk2 >= %{gtk2_version}
Requires: libxml2 >= %{libxml2_version}
Requires: ORBit2 >= %{ORBit2_version}
Requires: popt >= %{popt_version}
BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libxml2-devel >= %{libxml2_version}
BuildRequires: ORBit2-devel >= %{ORBit2_version}
BuildRequires: popt-devel >= %{popt_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}

%description
GConf is the Configuration Framework for the GNOME Desktop.

%package devel
Summary:      GNOME Configuration Framework Development Libraries
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     libxml2-devel >= %{libxml2_version}
Requires:     ORBit2-devel >= %{ORBit2_version}
Requires:     gtk2-devel >= %{gtk2_version}

%description devel
GConf is the Configuration Framework for the GNOME Desktop.

%prep
%setup -q
%if %build_l10n
# Disable GNU extensions for ar CR 6730851
sh %SOURCE1 --disable-gnu-extensions
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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

export PKG_CONFIG_PATH=%{_libdir}/pkgconfig

%if %build_l10n
sh %SOURCE1 --enable-copyright
%endif

libtoolize --force
aclocal
autoheader
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure		                \
            --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --libexecdir=%{_libexecdir} \
	    --sysconfdir=%{_sysconfdir}	\
	    --libexecdir=%{_libexecdir}	\
	    %{gtk_doc_option}

# For some reason using -j $CPUS breaks the build on my machine with
# 2 processors, so just using make
#
make

%install
make install DESTDIR=$RPM_BUILD_ROOT MKDIR_P="mkdir -p"

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/GConf/2/*.la
rm $RPM_BUILD_ROOT%{_libdir}/GConf/2/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/GConf
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/GConf/2/*.so*
%{_libdir}/libgconf-2*so.*
%{_sysconfdir}/gconf
%{_mandir}/man1/*
%dir %{_sysconfdir}/gconf/gconf.xml.defaults
%dir %{_sysconfdir}/gconf/gconf.xml.mandatory

%files devel
%defattr(-, root, root)
%{_includedir}/gconf/2/gconf/*.h
%{_libdir}/libgconf-2*.so
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/*.m4
%{_datadir}/gtk-doc/*
%{_datadir}/sgml/*
%{_mandir}/man3/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.0.
* Fri Oct 10 2008 - darren.kenny@sun.com
- Add patch GConf-04-user-specific-dbus so D-Bus is restarted without
  DBUS_SESSION_BUS_ADDRESS set if the effective user id looking to connect is
  not the same as the owner of the bus. Fix for bug#2980
* Fri Sep 26 2008 - brian.cameron@sun.com
- Bump to 2.24.0.  Remove upstream patch GConf-04-nopolkit.diff.
* Tue Aug 05 2008 - takao.fujiwara@sun.com
- Add l10n-configure.sh to fix 6730851 ar SEGV
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.1.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 22 2008 - damien.carbery@sun.com
- Bump to 2.21.2. Remove upstream patch 04-glib-pc.
* Thu Jan 10 2008 - damien.carbery@sun.com
- Add patch 04-glib-pc to fix gconf-2.0.pc file type: s/glib/glib-2.0/.
* Wed Jan 09 2008 - damien.carbery@sun.com
- Bump to 2.21.1. Remove upstream patch, 02-daemon-hanged-solaris, rename
  remainder.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Fri Sep 28 2007 - laca@sun.com
- convert to new style multi-ISA build
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Jul 02 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Wed Mar 15 2007 - dougs@truemail.co.th
- Removed adding ccdir to PATH
* Tue Mar 06 2007 - damien.carbery@sun.com
- Add aclocal call and set MKDIR_P in %install to resolve autoconf version
  mismatch.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.18.0.1.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.18.0. Remove upstream patches, 05-gconftool-makefile-install and
  06-use-fdwalk.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Tue Oct 17 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Mon Sep 25 2006 - padraig.obriain@sun.com
- add patch use-fdwalk to speed up clsoing of fds. (bug 6366879)
* Tue Jul  4 2006 - laca@sun.com
- add patch gconftool-makefile-install.diff which makes --makefile-install-rule
  continue if a schemas file fails.
* Thu Jun 29 2006 - laca@sun.com
- add patch GCONF_BACKEND_DIR.diff that makes the backend dir relocatable
  via env variable
* Sat Mar 18 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 2.13.5.
* Fri Jan  6 2006 - laca@sun.com
- set 64-bit sysconfdir to /etc, since those files are not arch specific
* Wed Nov 30 2005 - damien.carbery@sun.com
- Remove upstream patch, 04-markup-tree-incremental-reads.diff.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.1.
* Thu Oct 20 2005 - laca@sun.com
- add Lorenzo's incremental read patch; already in HEAD
* Wed Sep 14 2005 - brian.cameron@sunc.om
- Bump to 2.12.0.
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.90.
* Wed Jun 15 2005 - laca@sun.com
- add patch pkgconfig.diff that add gconf-2.0 to the pkgconfig deps
- run autoconf
* Wed May 11 2005 - brian.cameron@sun.com
- Remove building with multiple processors, since that is breaking
  the build on Solaris.
* Fri May 06 2005 - glynn.foster@wipro.com
- Bump to 2.10.0
* Tue Feb 15 2005 - arvind.samptur@wipro.com
- Add patch to fix such that defaults don't get
  installed for all locales since we always
  fallback to C locale values
* Fri Oct 29 2004 - laca@sun.com
- use $CC64 for the 64-bit build if defined
* Sat Oct  2 2004 - Joseph.Townsend@Sun.COM
- Create 64bit libraries for Solaris
* Fri Sep 24 2004 - yuriy.kuznetsov@sun.com
- Added GConf-06-g11n-potfiles.diff 
* Mon Aug 30 2004 - takao.fujiwara@sun.com
- updated GConf-02-g11n-potfiles.diff
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Wed Aug 11 2004 - ghee.teo@sun.com
- Removed GConf-05-use-global-lock.diff as it is backwards incomptaible in a 
  heterogeneous environment. While the goal of the project is to allow 
  concurrent login which has in effect achieved by not having any lock at all.
* Thu Aug 02 2004 - hidetoshi.tajima@sun.com
- create GConf-06-g11n-locale-alias.diff to fix bug #5042863,
  the orignal patch is from the bugzilla.gnome.org #100378
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to GConf-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - stephen.browne@sun.com
- ported to rpm4/suse91
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 11 2004 - Ghee.Teo@Sun.Com
- Create a patch GConf-05-use-global-lock.diff as we want to use orbit ip
  to resolve to a single gconf daemon per user.
* Thu Jun 03 2004 - Ghee.Teo@Sun.Com
- Added GConf-04-daemon-hanged-solaris.diff as the signal handler
  is calling non-reentrant code as gconf_log(). SO removed the calls
  to these signals, though much of these messages are not that important.
* Wed May 19 2004 - Cyrille.Moureaux@Sun.COM
- added GConf-03-apoc-path-update.diff.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to GConf-l10n-po-1.1.tar.bz2
* Thu Apr 06 2004 - matt.keenan@sun.com
- Updtaed to 2.6.1 tarball.
* Fri Apr 02 2004 - ghee.teo@sun.com
- Updtaed to 2.6.0 tarball.
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to GConf-l10n-po-1.0.tar.bz2
* Fri Mar 19 2004 - glynn.foster@sun.com
- Bump to 2.5.90 and merge the potfile patches.
* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added GConf-03-g11n-potfiles.diff
* Wed Feb 11 2004 - <matt.keenan@sun.com>
- Bump to 2.5.1, l10n to 0.7, port 02-fix-potfiles patch
* Mon Dec 15 2003 - <glynn.foster@sun.com>
- Add back the man page stuff, and the backend 
  notification patch
* Mon Oct 06 2003 - <markmc@sun.com> 2.4.0.1-1
- Update to 2.4.0.1-1.
- Remove dump/load and local locks patches.
* Tue Aug 19 2003 - <niall.power@sun.com>
- add GConf-02-sanity-check.diff patch, fixes 4908212
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Fri Aug 01 2003 - <markmc@sun.com> 2.2.1-1
- Upgrade to 2.2.1
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Fri May 30 2003 - <markmc@sun.com>
- Make sure gconf.xml.mandatory gets created
* Fri May 30 2003 - <markmc@sun.com>
- Add patches required by gnome-panel-2.3.1
- Install .la files
* Thu May 07 2003 - <Niall.Power@Sun.COM>
- Create new spec file for GConf
