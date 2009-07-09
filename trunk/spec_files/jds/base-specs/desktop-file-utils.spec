#
# spec file for package desktop-file-utils
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
Name:			desktop-file-utils
License:		GPL
Group:			Development/Tools/Other 
Version:		0.15
Release:		1
Distribution:		Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		Desktop file utilities
Source:			http://www.freedesktop.org/software/desktop-file-utils/releases/%{name}-%{version}.tar.gz
URL:			http://www.gnome.org
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir: 		%{_defaultdocdir}/doc
Autoreqprov:		on

%define popt_version 1.6.4
%define glib2_version 2.2.1

Requires:      glib2 >= %{glib2_version}
BuildRequires: glib2-devel >= %{glib2_version}
BuildRequires: popt-devel >= %{popt_version}

%description
desktop-file-utils is a collection of command line tools for working with 
desktop files.

%prep
%setup -q

%build
./configure --prefix=%{_prefix}
make

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_prefix}/bin
%{_datadir}

%changelog
* Thu Mar 06 2008 - brian.cameron@sun.com
- Bump to 0.15
* Mon Dec 10 2007 - brian.cameron@sun.com
- Bump to 0.14.
* Wed Nov 29 2006 - damien.carbery@sun.com
- Bump to 0.12.
* Wed Jul 21 2006 - dermot.mccluskey@sun.com
- Bump to 0.11.
* Tue May 17 2005 - Laszlo Kovacs <laszlo.kovacs@sun.com>
- add %{_datadir} to %files
* Fri May 06 2005 - Glynn Foster <glynn.foster@sun.com>
- Bump to 0.10
* Tue Aug 12 2003 - Glynn Foster <glynn.foster@sun.com>
- Initial release
