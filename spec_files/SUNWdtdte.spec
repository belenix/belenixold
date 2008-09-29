#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWdtdte
Summary:             desktop-login-dummy - Solaris Desktop Login dummy package to meet OpenOffice dependencies
Version:             5.11

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cd %{name}-%{version}-build
echo "Solaris Desktop Login dummy package" > README.SUNWdtdte

%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/sadm/softinfo

cp README.SUNWdtdte ${RPM_BUILD_ROOT}%{_localstatedir}/sadm/softinfo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*

%changelog
* Sun Sep 28 2008 - moinakg@gmail.com
- Initial spec.
