#
# Copyright (c) 2008 The BeleniX Team
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

Name:                SFEspkg
Summary:             spkg - Package and repository management toolkit
Version:             0.2
Source1:             spkg
Source2:             spkg_mod.py
Source3:             tsort.py
Source4:             spkg.conf
Source5:             admin
Source6:             repo_util
Source7:             genver
Source8:             http://downloads.sourceforge.net/cryptkit/ecc-0.9.tar.gz
Source9:             http://downloads.sourceforge.net/cryptkit/aes-1.1.tar.gz
Source10:            pkey-pkg.belenix.org
Source11:            pkey-belenix.v12.su

Patch1:              ecc-01.patch
Patch2:              aes-01.patch

SUNW_BaseDir:        /
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
Requires:            SFEaxel

%prep
rm -rf %{name}-%{version}-build
mkdir %{name}-%{version}-build
cd %{name}-%{version}-build
gunzip -c %{SOURCE8} | tar xf -
gunzip -c %{SOURCE9} | tar xf -
%patch1 -p0
%patch2 -p0

%build
cd %{name}-%{version}-build
cd ecc-0.9
python setup.py build_ext
cd ..

cd aes-1.1
python setup.py build_ext
cd ..

%install
cd %{name}-%{version}-build
rm -rf ${RPM_BUILD_ROOT}
mkdir ${RPM_BUILD_ROOT}

cd ecc-0.9
python setup.py install --prefix=${RPM_BUILD_ROOT}/usr
cd ..

cd aes-1.1
python setup.py install --prefix=${RPM_BUILD_ROOT}/usr
cd ..

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}/spkg/downloads
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages

cp %{SOURCE1} ${RPM_BUILD_ROOT}%{_bindir}
cp %{SOURCE6} ${RPM_BUILD_ROOT}%{_bindir}
cp %{SOURCE7} ${RPM_BUILD_ROOT}%{_bindir}
chmod a+x ${RPM_BUILD_ROOT}%{_bindir}/*
cp %{SOURCE2} ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages
cp %{SOURCE3} ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages
cp %{SOURCE4} ${RPM_BUILD_ROOT}%{_localstatedir}/spkg
cp %{SOURCE5} ${RPM_BUILD_ROOT}%{_localstatedir}/spkg
cp %{SOURCE10} ${RPM_BUILD_ROOT}%{_localstatedir}/spkg
cp %{SOURCE11} ${RPM_BUILD_ROOT}%{_localstatedir}/spkg

python -m compileall -l ${RPM_BUILD_ROOT}%{_libdir}/python2.4/site-packages

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_localstatedir}/spkg
%{_localstatedir}/spkg/admin
%{_localstatedir}/spkg/spkg.conf
%{_localstatedir}/spkg/pkey-*
%dir %attr (0755, root, bin) %{_localstatedir}/spkg/downloads
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/python2.4
%dir %attr (0755, root, bin) %{_libdir}/python2.4/site-packages
%{_libdir}/python2.4/site-packages/*

%changelog
* Thu Oct 30 2008 - moinakg@belenix.org
- Bump version for several changes.
- Re-whack version number normalization.
- Add slightly better common name handling in repo_util.
- Add package size to catalog file.
* Sun Oct 19 2008 - moinakg@belenix.org
- Add in Python crypto modules for ECC and AES support.
- Add current public keys for BeleniX package sites.
* Sat Sep 27 2008 - moinakg@belenix.org
- Move spkg.conf from /etc to allow preserving user configuration.
- Add dependency on axel, remove dependency on core package.
* Wed Sep 17 2008 - moinakg@belenix.org
- Add a couple of repository management tools.
* Sun Sep 07 2008 - moinakg@belenix.org
- Initial spec.
