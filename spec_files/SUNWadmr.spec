#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWadmr
Summary:             System Admin root files - dependency package
Version:             5.11
Source:              sysidtool.xml

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWcsr

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cd %{name}-%{version}-build
echo "OS=OpenSolaris" >> INST_RELEASE
echo "VERSION=11" >> INST_RELEASE
echo "REV=0" >> INST_RELEASE


%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/system
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/sadm/softinfo

cp %{SOURCE} ${RPM_BUILD_ROOT}%{_localstatedir}/svc/manifest/system
cp INST_RELEASE ${RPM_BUILD_ROOT}%{_localstatedir}/sadm/softinfo

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%{_localstatedir}/*

%changelog
* Sun Mar 30 2008 - moinakg@gmail.com
- Initial spec.
