#
# spec file for package dogtail
#
# includes module(s): dogtail
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
%define pythonver 2.4

Name:         dogtail
License:      GPL
Group:        Development/Languages/Python
Version:      0.6.1
Release:      2
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GUI test tool and automation framework written in Python
Source:       http://people.redhat.com/zcerza/dogtail/releases/%{name}-%{version}.tar.gz
URL:          http://people.redhat.com/zcerza/dogtail/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  off
Prereq:       /sbin/ldconfig
Requires:      python >= %{pythonver}
Requires:      at-spi
Requires:      pyspi
Requires:      Pyrex
BuildRequires: python-devel >= %{pythonver}
BuildRequires: at-spi-devel
BuildRequires: pyspi

%description
dogtail is a GUI test tool and automation framework written in Python.
It uses Accessibility (a11y) technologies to communicate with desktop
applications. dogtail scripts are written in Python and executed like any
other Python program.

%prep
%setup -q

%build

%install
python setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}
%{_libdir}/python?.?/vendor-packages
%{_datadir}/doc
%{_datadir}/dogtail
%{_datadir}/icons
%{_datadir}/applications

%changelog
* Wed Mar 11 2009 - dave.lin@sun.com
- Took the ownership of this spec file.
* Mon Nov 17 2007 - jedy.wang@sun.com
- Fix installation directory bug.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Don't delete *.pyc files - they are needed.
* Thu Nov 09 2006 - damien.carbery@sun.com
- Bump 0.6.1. Remove upstream patch, 01-solaris.
* Sat Oct 07 2006 - brian.cameron@sun.com
- Bump 0.6.0.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 0.5.2.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 0.5.0.
* Mon Oct 31 2005 - laca@sun.com
- move from site-packages to vendor-packages
* Wed Oct 26 2005 - damien.carbery@sun.com
- Bump to 0.4.3.
* Thu Oct 20 2005 - damien.carbery@sun.com
- Delete .pyc files so they are not included in the package.
- Initial version.
