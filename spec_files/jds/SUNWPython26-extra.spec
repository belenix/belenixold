#
# spec file for package SUNWPython26-extra
#
# includes module(s): Pyrex, numpy
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc
%define pythonver 2.6
%use pyrex = Pyrex.spec
%use numpy = numpy.spec

Name:                    SUNWPython26-extra
Summary:                 Supplemental Python libraries and utilities
Version:                 2.6.1
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          SUNWPython-extra.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWPython26
Requires: SUNWlexpt
BuildRequires: SUNWsfwhea
BuildRequires: SUNWPython26-devel
BuildRequires: SUNWpython26-setuptools

%prep
rm -rf %name-%version
mkdir %name-%version
%pyrex.prep -d %name-%version
%numpy.prep -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
export PYTHON=/usr/bin/python2.6
%pyrex.install -d %name-%version
%numpy.install -d %name-%version

mv $RPM_BUILD_ROOT%{_bindir}/pyrexc $RPM_BUILD_ROOT%{_bindir}/pyrexc2.6

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*


%changelog
* Mon Feb  2 2009 - laca@sun.com
- create based on SUNWPython25-extra.spec
* Mon Nov 24 2008 - laca@sun.com
- created, based on SUNWPython-extra.spec
* Thu Oct 25 2007 - brian.cameron@sun.com
- Add numpy to add numerical processing extensions to Python.
* Thu Jul 27 2006 - laca@sun.com
- add elementtree
* Thu Oct 27 2005 - laca@sun.com
- add PyXML
- move pyspi to SUNWgnome-python-libs
- change permissions to root:bin
* Thu Oct 20 2005 - damien.carbery@sun.com
- Use %{default_pkg_version} instead of python version.
* Wed Oct 19 2005 - damien.carbery@sun.com
- Initial version.
