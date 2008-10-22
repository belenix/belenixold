#
# spec file for package SFEmrxvt
#
# includes module(s): Mrxvt
#
%include Solaris.inc

%define src_name	pysqlite
%define src_version	2.5.0a
%define pkg_release	1

SUNW_Pkg: %{src_name}
SUNW_ProdVers:	%{src_version}
SUNW_BaseDir:	%{_basedir}

Name:                    pysqlite
Summary:                 pysqlite - Python DB-API 2.0 interface for SQLite 3.x
Version:                 2.5.0
Source:                  http://oss.itsystementwicklung.de/download/pysqlite/2.5/2.5.0/pysqlite-%{src_version}.tar.gz
URL:                     http://oss.itsystementwicklung.de/trac/pysqlite/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%version

%build
python setup.py build_ext

%install
python setup.py install --prefix=${RPM_BUILD_ROOT}%{_prefix}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages
%{_libdir}/python2.4/site-packages/*
%dir %attr (0755, root, bin) %{_prefix}/pysqlite2-doc
%{_prefix}/pysqlite2-doc/*


%changelog
* Sun Oct 19 2008 - moinak.ghosh@sun.com
- Initial gnuchess spec file

