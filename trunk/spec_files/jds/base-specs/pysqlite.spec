#
# spec file for package pysqlite
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%{?!pythonver:%define pythonver 2.4}

Name:                    pysqlite
Summary:                 Python DB-API 2.0 interface for the SQLite
%define                  major_version 2.4
Version:                 %{major_version}.1
Source:                  http://initd.org/pub/software/pysqlite/releases/%{major_version}/%{version}/pysqlite-%{version}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%prep
%setup -q -n pysqlite-%version

%build
python%{pythonver} setup.py build \
    --build-base=$RPM_BUILD_ROOT%{_prefix}

%install
rm -rf $RPM_BUILD_ROOT
python%{pythonver} setup.py install --prefix=%{_prefix} --root=$RPM_BUILD_ROOT

# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

rm -rf $RPM_BUILD_ROOT%{_prefix}/pysqlite2-doc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/lib/python%{pythonver}
%dir %attr(0755, root, bin) %{_prefix}/lib/python%{pythonver}/vendor-packages
%dir %attr(0755, root, bin) %{_prefix}/lib/python%{pythonver}/vendor-packages/pysqlite2
%{_prefix}/lib/python2.4/vendor-packages/pysqlite2/*

%changelog
* Thu Feb 12 2009 - brian.cameron@sun.com
- Split from SUNWpysqlite.spec file.
* Tue Nov 18 2008 - jedy.wang@sun.com
- Fix installation directory problem.
* Tue Sep 16 2008 - matt.keenn@sun.com
- Update copyright
* Tue Mar 11 2008 - damien.carbery@sun.com
- Change SUNWsqlite3-devel reference to SUNWsqlite3.
* Tue Feb 12 2008 - brian.cameron@sun.com
- Change SFEsqlite require to SUNWsqlite.
* Tue Feb 12 2008 - dermot.mccluskey@sun.com
- initial version
