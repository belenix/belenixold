#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SFEpkgget
Summary:             Package repository client
Version:             5.11

SOURCE0:	     pkg-get
SOURCE1:	     pkg-get.conf
SOURCE2:	     admin
SOURCE3:	     makecontents.pl
SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:	     SUNWcsu

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cd %{name}-%{version}-build

%install

cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_prefix}/bin
cp %SOURCE0 ${RPM_BUILD_ROOT}%{_prefix}/bin
chmod a+x ${RPM_BUILD_ROOT}%{_prefix}/bin/*
mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}
cp %SOURCE1 ${RPM_BUILD_ROOT}%{_sysconfdir}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/pkg-get
cp %SOURCE2 ${RPM_BUILD_ROOT}%{_localstatedir}/pkg-get
cp %SOURCE3 ${RPM_BUILD_ROOT}%{_prefix}/bin

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_prefix}/bin
%{_prefix}/bin/*
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/*
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, bin) %{_localstatedir}/pkg-get
%{_localstatedir}/pkg-get/*

%changelog
* Sun Aug 17 2008 - moinakg@belenix.org
- Add capability to handle multiple repository sites transparently.
* Fri Aug 15 2008 - moinakg@belenix.org
- Initial spec.
