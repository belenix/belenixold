#
# spec file for package pyxml
#
# includes module(s): pyxml
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%{!?pythonver:%define pythonver 2.4}

Name:         pyxml
License:      CNRI Python License
Group:        Development/Languages/Python
Version:      0.8.4
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Python XML module
Source:       http://internap.dl.sourceforge.net/sourceforge/pyxml/PyXML-0.8.4.tar.gz
URL:          http://pyxml.sourceforge.net/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  off
Prereq:       /sbin/ldconfig
Requires:     python >= %{pythonver}
Requires:     expat
BuildRequires: python-devel >= %{pythonver}
BuildRequires: expat

%description
A collection of tools useful for writing basic XML applications in Python,
along with documentation and sample code.
Features include (but are not limited to) SAX, DOM, the xmlproc validating
parser, an Expat interface.

%prep
%setup -q -n PyXML-%{version}

%install
python%{pythonver} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_bindir}
%{_libdir}/python?.?/vendor-packages

%changelog
* Mon Nov 24 2008 - laca@sun.com
- use %{pythonver} macro to select with version of Python to build which
* Mon Nov 17 2007 - jedy.wang@sun.com
- Fix installation directory bug.
* Thu Nov 01 2007 - brian.cameron@sun.com
- Fix Source URL.
* Thu Oct 27 2005 - laca@sun.com
- initial version
