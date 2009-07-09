#
# spec file for package nimbus
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
Name:         nimbus
Summary:      Engine for GTK2 Nimbus Theme
# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
Version:      0.1.2
%define tarball_version %{version}
Release:      1
License:      LGPL
Distribution: Java Desktop System
Vendor:	      Sun Microsystems, Inc.
Group:        System/GUI/GNOME
Source:       http://dlc.sun.com/osol/jds/downloads/extras/nimbus/%{name}-%{tarball_version}.tar.bz2
Source1:      nimbus-media-play-rtl.png
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
URL:          http://www.sun.com/software/javadesktopsystem/
#owner:erwannc date:2006-09-20  type:branding
Patch1:	      nimbus-01-icon-name-mapping-hack.diff
## %SOURCE1 .png file needs to be upstreamed when the %patch2 
## rtl-icons.diff is upstreamed.
#owner:fujiwara date:2009-04-10 type:bug bugster:6675046
Patch2:       nimbus-02-rtl-icons.diff

%define gtk2_version 2.4.0
%define intltool_version 0.30
BuildRequires: gtk2 >= %{gtk2_version}
BuildRequires: intltool >= %{intltool_version}

%description
This package contains the Nimbus theme engine for GTK2

%prep
%setup -q -n %name-%tarball_version
cp %SOURCE1 gtk-engine/gtk-2.0/media-play-rtl.png
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

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
automake -a -c -f
autoconf
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./autogen.sh --prefix=%{_prefix}  \
	     --libdir=%{_libdir}  \
	     --sysconfdir=%{_sysconfdir} 
make -j $CPUS
cd -

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/*/engines/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_libdir}/gtk-2.0/*/engines/*.so
%{_datadir}/themes/*
%{_datadir}/icons/*
%{_datadir}/locale/*
%{_datadir}/pixmaps/*

%changelog
* Fri Apr 10 2009 - takao.fujiwara@sun.com
- Add patch nimbus-02-rtl-icons.diff CR 6675046
- Add media-play-rtl.png in ext-sources.
* Thu Aug 14 2008 - erwann@sun.com
- bumped to 0.0.17
* Fri May 18 2007 - laca@sun.com
- set CFLAGS/LDFLAGS and configure options such that we can use this spec
  file for the 64-bit build too
* Fri Jul 21 2006 - damien.carbery@sun.com
- Add patch to comment out the redefine of an enum.
* Mon May 12 2006 Erwann Chenede - <erwann.chenede@sun.com>
- initial implementation of the spec file
