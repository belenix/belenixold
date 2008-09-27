#
# Copyright (c) 2008 The BeleniX Team
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SFEspkg
Summary:             spkg - Advanced SVR4 package and repository management
Version:             0.1
Source1:             spkg
Source2:             spkg_mod.py
Source3:             tsort.py
Source4:             spkg.conf
Source5:             admin
Source6:             repo_util
Source7:             genver

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SFEaxel

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build

%build
cd %{name}-%{version}-build

%install
cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/spkg/downloads
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}
cp %{SOURCE6} ${RPM_BUILD_ROOT}%{_bindir}
cp %{SOURCE7} ${RPM_BUILD_ROOT}%{_bindir}
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_localstatedir}/spkg
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_localstatedir}/spkg

python -m compileall -l ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, sys) %{_bindir}
%{_bindir}/*

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_localstatedir}/spkg
%{_localstatedir}/spkg/admin
%{_localstatedir}/spkg/spkg.conf
%dir %attr (0755, root, bin) %{_localstatedir}/spkg/downloads
%dir %attr (0755, root, sys) %{_libdir}
%dir %attr (0755, root, sys) %{_libdir}/python2.4
%dir %attr (0755, root, sys) %{_libdir}/python2.4/site-packages
%{_libdir}/python2.4/site-packages/*

%changelog
* Sat Sep 27 2008 - moinakg@belenix.org
- Move spkg.conf from /etc to allow preserving user configuration.
- Add dependency on axel, remove dependency on core package.
* Wed Sep 17 2008 - moinakg@belenix.org
- Add a couple of repository management tools.
* Sun Sep 07 2008 - moinakg@belenix.org
- Initial spec.
