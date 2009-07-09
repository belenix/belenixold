#
# spec file for package gnome-audio
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
Name:			gnome-audio
License:		Creative Commons Attribution-Share Alike 2.0 Generic, Creative Commons Attribution 3.0 Unported
Group:			System/Libraries/GNOME
BuildArchitectures:	noarch
Version:		2.22.2
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Sounds for GNOME events.
Source:			http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.22/%{name}-%{version}.tar.bz2
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%description
If you use the GNOME desktop environment, you may want to install this package
of comlementary sounds.

%prep
%setup -q

%install
mkdir -p $RPM_BUILD_ROOT
make prefix=$RPM_BUILD_ROOT/%{_prefix} DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README
%{_datadir}/sounds/*.wav
%{_datadir}/sounds/panel/*.wav
%{_datadir}/sounds/gtk-events/*.wav


%changelog
* Wed Mar 26 2008 - brian.cameron@sun.com
- Bump to 2.22.1.

* Sun Mar 23 2008 - damien.carbery@sun.com
- Bump to 2.22.0. Add patch 01-destdir to fix #524032.

* Mon Feb 23 2004 Matt Keenan <matt.keenan@sun.com>
- Updated Distro

* Mon Oct 20 2003 Ghee Teo <ghee.teo@sun.com>
- Updated spec file, since there is no new release of this module in GNOME 2.4
  simply uprev release number.

* Thu Aug 06 2003 Niall Power <niall.power@sun.com>
- Initial spec file created.
