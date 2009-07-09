#
# spec file for package apoc-adapter-gconf
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         apoc-adapter-gconf
License:      BCL
Group:        System/GUI/GNOME 
Version:      1.1.0
Release:      1
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Summary:      Apoc GConf Adapter
Source:       apoc-adapter-gconf-%{version}.tar.bz2
URL:          http://www.sun.com
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Autoreqprov:  on

Requires:      GConf
Requires:      apoc
Prereq:        sed
Prereq:        coreutils
Prereq:        /sbin/ldconfig
BuildRequires: GConf-devel

%define pathfile    %{_sysconfdir}/gconf/2/path

%description
Part of the Apoc framework providing through GConf central configuration 
settings.

%prep
%setup -q -n apoc-adapter-gconf-%{version}

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

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}	--sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/GConf/2/*.la
rm $RPM_BUILD_ROOT%{_libdir}/GConf/2/*.a

# Ensures a clean build root before building a package a second time.
%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{pathfile} ]; then
    sed -e s/^#apoc:/apoc:/g %{pathfile} > /tmp/apocpath.$$
    if [ $? -eq 0 ]; then
        mv /tmp/apocpath.$$ %{pathfile}
    fi
fi
/sbin/ldconfig

%preun
if [ $1 -eq 0 ] && [ -f %{pathfile} ]; then
    sed -e s/^apoc:/#apoc:/g %{pathfile} > /tmp/apocpath.$$
    if [ $? -eq 0 ]; then
        mv /tmp/apocpath.$$ %{pathfile}
    fi
fi

%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/GConf/2/libgconfbackend-apoc.so
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_sysconfdir}/gconf/2/*

%changelog
* Thu Jun 29 2006 - Cyrille.Moureaux@Sun.COM
- Moved to new tarball adapted for use with Gnome 2.14 (5028119).

* Tue Mar 14 2006 - Cyrille.Moureaux@Sun.COM
- Added apoc-adapter-gconf-02-placeholders.diff to handle replacements in APOC
  data (6397519).

* Thu Oct 14 2004 - Cyrille.Moureaux@Sun.COM
- Added apoc-adapter-gconf-02-shutdown-protect.diff to fix potential
  conflicts during shutdown (6179077).
- Set l10n tarball to proper version number.

* Wed Sep 15 2004 - ciaran.mcdermott@sun.com
- added apoc-adapter-gconf--01-g11n-alllinguas.diff to include cs, hu.

* Wed Jul 07 2004 - stephen.browne@sun.com
- ported to rpm4/SuSE9.1

* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds

* Fri Jun 11 2004 - Cyrille.Moureaux@Sun.COM
- Updated version number.
* Wed May 19 2004 - Cyrille.Moureaux@Sun.COM
- Removed patch file for GConf path and modified post/preun to 
  modify the path delivered by GConf instead.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to apoc-adapter-gconf-l10n-po-1.1.tar.bz2

* Mon Apr 19 2004 - Cyrille.Moureaux@Sun.COM
- Update version number and remove patch (which *was* required until now).
* Thu Apr 01 2004 - damien.carbery@sun.com
- Comment out failing patch. Damien Donlon told me it is no longer required.
  Leaving in spec file and patch file in CVS in case I misheard him.
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding apoc-adapter-gconf-l10n-po-1.0.tar.bz2 l10n content

