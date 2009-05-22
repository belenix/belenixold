#
# spec file for package SFEpkcs11-helper
#
# includes module(s): pkcs11-helper
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFEpkcs11-helper
Summary:                 pkcs11-helper is a library for using PKCS#11 providers
Version:                 1.07
URL:                     http://www.opensc-project.org/pkcs11-helper/
Source:                  http://www.opensc-project.org/files/pkcs11-helper/pkcs11-helper-%{version}.tar.bz2

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
License:                 GPLv2,BSD
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEgccruntime
BuildRequires: SFEgcc

%description
pkcs11-helper is a library that simplifies the interaction with
PKCS#11 providers for end-user applications using a simple API
and optional OpenSSL engine. 

%package devel
Summary:                 Development files for the pkcs11-helper package.
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEgcc

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp pkcs11-helper-%{version} pkcs11-helper-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd pkcs11-helper-%{version}-64
export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64}"
export PKCS11_TEST_PROVIDER="/usr/lib/%{_arch64}/libpkcs11.so"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}/%{_arch64}              \
            --libdir=%{_libdir}/%{_arch64}              \
            --libexecdir=%{_libexecdir}/%{_arch64}      \
            --sysconfdir=%{_sysconfdir}      \
            --infodir=%{_infodir}            \
            --enable-shared		     \
	    --disable-static                 \
            --enable-threading               \
            --enable-token                   \
            --enable-data                    \
            --enable-certificate             \
            --enable-slotevent               \
            --enable-openssl                 \
            --with-crypto-engine-openssl     \
            --with-crypto-engine-gnutls      \
            --with-test-provider=${PCKS11_TEST_PROVIDER} \
            --with-pic

make
cd ..
%endif

cd pkcs11-helper-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/lib -R/lib"
export PKCS11_TEST_PROVIDER="/usr/lib/libpkcs11.so"

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --infodir=%{_infodir}            \
            --enable-shared                  \
            --disable-static                 \
            --enable-threading               \
            --enable-token                   \
            --enable-data                    \
            --enable-certificate             \
            --enable-slotevent               \
            --enable-openssl                 \
            --with-crypto-engine-openssl     \
            --with-crypto-engine-gnutls      \
            --with-test-provider=${PCKS11_TEST_PROVIDER} \
            --with-pic

make
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd pkcs11-helper-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/lib*.la

cat ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/pkgconfig/libpkcs11-helper-1.pc | sed '{
    s@-R/lib -L/lib@-R/lib/%{_arch64} -L/lib/%{_arch64}@
    s@-lgnutls@-L\${libdir} -R\${libdir} -lgnutls@
}' > libpkcs11-helper-1.pc.new
mv libpkcs11-helper-1.pc.new ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/pkgconfig/libpkcs11-helper-1.pc

cd ..
%endif

cd pkcs11-helper-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.a
rm -f ${RPM_BUILD_ROOT}%{_libdir}/lib*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%dir %attr (0755,root,sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man8
%{_mandir}/man8/*
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Fri May 22 2009 - moinakg@belenix.org
- Initial version
