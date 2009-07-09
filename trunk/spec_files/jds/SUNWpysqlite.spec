#
# spec file for package SUNWpysqlite
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#

%include Solaris.inc

%use pysqlite = pysqlite.spec
%define pythonver 2.4

Name:                    SUNWpysqlite
Summary:                 Python DB-API 2.0 interface for the SQLite
%define                  major_version 2.4
Version:                 %{major_version}.1
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SUNWPython
Requires:                SUNWsqlite3
BuildRequires:           SUNWPython-devel
BuildRequires:           SUNWsqlite3
BuildRequires:           SUNWpython-setuptools

%include default-depend.inc

%prep
rm -rf %name-%version
mkdir -p %name-%version
%pysqlite.prep -d %name-%version

%build
%pysqlite.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%pysqlite.install -d %name-%version

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) %{_prefix}/lib/python%{pythonver}
%dir %attr(0755, root, bin) %{_prefix}/lib/python%{pythonver}/vendor-packages
%dir %attr(0755, root, bin) %{_prefix}/lib/python%{pythonver}/vendor-packages/*
%{_prefix}/lib/python%{pythonver}/vendor-packages/pysqlite2/*
%doc -d %{pysqlite.name}-%{pysqlite.version} LICENSE PKG-INFO
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc

%changelog
* Thu Feb 12 2009 - brian.cameron@sun.com
- Now use pysqlite.spec file
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
