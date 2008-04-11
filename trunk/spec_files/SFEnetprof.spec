#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SFEnetprof
Summary:             Network Profiles Utility
Version:             1.0
Source:              netprof
Source1:             Static

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWcsr

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cp %{SOURCE} . 
cp %{SOURCE1} . 


%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}/%{_basedir}/bin
mkdir -p ${RPM_BUILD_ROOT}/%{_sysconfdir}/netprof

cp %{SOURCE} ${RPM_BUILD_ROOT}/%{_basedir}/bin
cp %{SOURCE1} ${RPM_BUILD_ROOT}/%{_sysconfdir}/netprof
chmod a+x ${RPM_BUILD_ROOT}/%{_basedir}/bin/*

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_basedir}/bin
%{_basedir}/bin/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Fri Apr 11 2008 - moinakg@gmail.com
- Initial spec.
