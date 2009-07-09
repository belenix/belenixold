#
# spec file for package libgail-gnome
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         libgail-gnome
License:      LGPL
Group:        System/Libraries/GNOME
Version:      1.20.1
Release:      42
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Accessibility implementation for GTK+ and GNOME libraries
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgail-gnome/1.20/%{name}-%{version}.tar.bz2
URL:          http://developer.gnome.org/projects/gap
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libgnomeui_version 2.6.0
%define gtk2_version 2.4.0
%define gnome_panel_version 2.6.0
%define atk_version 1.7.0
%define at_spi_version 1.5.1
%define at_spi_release 1

BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gnome-panel-devel >= %{gnome_panel_version}
BuildRequires: atk-devel >= %{atk_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: at-spi-devel >= %{at_spi_version}-%{at_spi_release}
Requires:      atk >= %{atk_version}
Requires:      gtk2 >= %{gtk2_version}
Requires:      gnome-panel >= %{gnome_panel_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      at-spi >= %{at_spi_version}


%description
GAIL implements the abstract interfaces found in ATK for GTK+ and GNOME 
libraries, enabling accessibility technologies such as at-spi to access those 
GUIs. libgail-gnome contains the GNOME portions of GAIL.

%prep
%setup -q 


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

./configure --prefix=%{_prefix}

make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm $RPM_BUILD_ROOT%{_libdir}/gtk-2.0/modules/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post 
/sbin/ldconfig

%postun 
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_libdir}/gtk-2.0/*/*.so
%{_libdir}/pkgconfig

%changelog
* Sat Sep 27 2008 - christian.kelly@sun.com
- Bump to 1.21.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 1.20.0.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Bump to 1.19.5.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 1.18.0.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 1.1.3.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 1.1.2.
* Thu Aug 11 2005 - brian.cameron@sun.com
- Remove --enable-gtk-doc from configure since this library has no gtk-docs.
* Tue Apr 19 2005 - <bill.haneman@sun.com>
- Bump to 1.1.1, for bugfix #6240069.
* Tue Aug 24 2004 - laszlo.kovacs@sun.com
- removed devel package, this pacakge does not install any docs
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.  added devel package for gtk-docs.
* Tue Aug 03 2004 - <bill.haneman@sun.com>
- Bump to 1.1.0
* Mon Jul 26 2004 - <padraig.obriain@sun.com>
- Bump to 1.0.5
* Wed Jul 07 2004 - niall.power@sun.com
- port to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Thu Mar 25 2004 - <damien.carbery@sun.com>
- Add gnome-panel-devel as a dependency.
* Tue Mar 23 2004 - <padraig.obriain@sun.com>
- Bump to 1.0.3
* Fri Feb 27 2004 - <laca@sun.com>
- add pkgconfig file
* Wed Feb 18 2004 - Matt.Keenan@sun.com
- Update distro
* Fri Oct 10 2003 - Laszlo.Kovacs@sun.com
- moving up version numbers of deps
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Wed May 14 2003 - ghee.teo@sun.com
- initial release version for libgail-gnome
