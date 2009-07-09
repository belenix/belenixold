#
# spec file for package poppler
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
# bugdb: bugzilla.freedesktop.org
#
Name:         poppler-data
License:      Adobe
Group:        System/Libraries
Version:      0.2.1
Release:      1 
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      PDF Rendering Library
Source:       http://poppler.freedesktop.org/%{name}-%{version}.tar.gz
URL:          http://poppler.freedesktop.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}/%{name}
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%description
poppler-data consists of encoding files for use with poppler.  These
files allow poppler to correctly render CJK and Cyrrilic properly.

%prep
%setup -q

%build

# Nothing to make

%install
make DESTDIR=$RPM_BUILD_ROOT install datadir=%{_datadir} 

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%{_datadir}/poppler/*

%changelog
* Wed Dec 19 2007 - brian.cameron@sun.com
- Bump to 0.2.0.

* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 0.1.1. Remove upstream patch 01-fixmake.

* Mon Sep 03 2007 - brian.cameron@sun.com
- Created
