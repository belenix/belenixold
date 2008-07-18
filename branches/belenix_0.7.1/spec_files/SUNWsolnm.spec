#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWsolnm
Summary:             BeleniX Naming enabler
Version:             5.11

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWcsr

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cd %{name}-%{version}-build
echo "                              BeleniX 0.7.1 07/08" > release
echo "                         Based on OpenSolaris Build 93" >> release
echo "                           Innovating on OpenSolaris" >> release
echo "                             Assembled 18 July 2008" >> release


%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
cp release ${RPM_BUILD_ROOT}%{_sysconfdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*

%changelog
* Thu Jul 03 2008 - moinakg@gmail.com
- Updated release version and tentative dates.
* Wed Feb 20 2008 - moinak.ghosh@sun.com
- Initial spec.
