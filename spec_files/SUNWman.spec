#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWman
Summary:             Solaris manual pages
Version:             5.11.1
%define tarball_version 20081210
Source:              http://dlc.sun.com/osol/man/downloads/current/man-sunosman-%{tarball_version}.tar.bz2

URL:                 http://dlc.sun.com/osol/devpro/downloads/current/
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

cd %{name}-%{version}-build
bunzip2 -c %{SOURCE} | tar xpf -

%build
cd %{name}-%{version}-build

%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}

tar cpf - * | (cd ${RPM_BUILD_ROOT}%{_datadir}; tar xpf - )

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/man
%{_datadir}/man/*

%changelog
* Mon Feb 19 2008 - moinak.ghosh@sun.com
- Initial spec.
