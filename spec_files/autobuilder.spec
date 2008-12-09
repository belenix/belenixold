#
# Copyright (c) 2008 The BeleniX Team
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                autobuilder
Summary:             Utility to automate building OpenSolaris and XVM from source
Version:             0.2
Source1:             osol_builder
Source2:             osol_builder.py

SUNW_BaseDir:        /usr
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWipkg

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build
cd %{name}-%{version}-build

%build
cd %{name}-%{version}-build

%install
cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_bindir}
chmod a+x ${RPM_BUILD_ROOT}%{_bindir}/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%changelog
* Tue Dec 09 2008 - moinakg@belenix.org
- Initial spec.
