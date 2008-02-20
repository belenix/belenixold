#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SUNWsolnm
Summary:             Solaris Naming enabler
Version:             5.11

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SUNWcsr

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cd %{name}-%{version}-build
echo "                               BeleniX 0.7 03/08" > release
echo "                           Innovating on OpenSolaris" >> release
echo "                            Assembled 20 March 2008" >> release


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
* Wed Feb 20 2008 - moinak.ghosh@sun.com
- Initial spec.
