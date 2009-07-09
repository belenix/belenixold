#
# spec file for package dmz-cursor
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#

Name:			Vanilla-DMZ
License:		MIT
Group:			System/GUI/GNOME
BuildArchitectures:     noarch
Version:		0.4
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		DMZ cursor themes also known as DMZ-White
Source:                 http://jimmac.musichall.cz/zip/vanilla-dmz-%{version}.tar.bz2
URL:			http://jimmac.musichall.cz/themes.php?skin=7
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on


%description
This package contains the DMZ cursor themes, which are derived from the Industrial theme developed for the Ximian GNOME desktop.

%prep
%setup -n %{name}
rm COPYING

%install
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/icons/DMZ-White
cp -rp * $RPM_BUILD_ROOT/%{_datadir}/icons/DMZ-White
rm  $RPM_BUILD_ROOT/%{_datadir}/icons/DMZ-White/index.theme


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, other)
%{_datadir}/icons/DMZ-White/*

%changelog
* Thu Jul 24 2008 - ghee.teo@sun.com
- Created Spec for dmz-cursor.spec 
