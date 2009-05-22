#
# spec file for package SFEqca
#
# includes module(s): qca
#
# 64Bit build commented for now since GStreamer is still 32Bit only.
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          qca
Name:                    SFEqca
Summary:                 Qt Cryptographic Architecture (QCA)
Version:                 4.2-svn20090520
License:                 LGPLv2
Source:                  http://www.belenix.org/binfiles/qca-%{version}.tar.bz2
URL:                     http://delta.affinix.com/qca/

SUNW_BaseDir:            /
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEpkcs11-helper
Requires:      SFEcyrus-sasl
Requires:      SUNWgnutls
Requires:      SUNWlibgcrypt
Requires:      SUNWopensslr
Requires:      SFEgnupg
BuildREquires: SFEcyrus-sasl
BuildRequires: SUNWgnutls-devel
BuildRequires: SFEpkcs11-helper-devel
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWlibgcrypt-devel


%description
Taking a hint from the similarly-named Java Cryptography Architecture,
QCA aims to provide a straightforward and cross-platform crypto API,
using Qt datatypes and conventions. QCA separates the API from the
implementation, using plugins known as Providers. The advantage of
this model is to allow applications to avoid linking to or explicitly
depending on any particular cryptographic library. This allows one to
easily change or upgrade crypto implementations without even needing
to recompile the application! QCA should work everywhere Qt does,
including Windows/Unix/MacOSX.


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp %{src_dir}-%{version} %{src_dir}-%{version}-64
%endif

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=%{_prefix}/gnu/bin/gcc
export CXX=%{_prefix}/gnu/bin/g++
export QTDIR=%{_prefix}
export QT_INCLUDES=%{_includedir}/qt4
OPATH=${PATH}
export QC_CERTSTORE_PATH=%{_sysconfdir}/certs/qca

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
export PATH="%{qt4_bin_path64}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
        -DBIN_INSTALL_DIR=%{_bindir}/%{_arch64}                         \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DSASL2_INCLUDE_DIR=%{_includedir}                              \
        -DSASL2_LIBRARIES=%{_prefix}/gnu/lib/%{_arch64}/libsasl2.so     \
        -DPKGCONFIG_INSTALL_PREFIX=%{_libdir}/%{_arch64}/pkgconfig      \
        -DOPENSSL_LIBRARIES=/lib/%{_arch64}/libssl.so                   \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
%endif

cd %{src_dir}-%{version}
export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++ %{xorg_lib_path} -L/lib -R/lib"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DBIN_INSTALL_DIR=%{_bindir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DSASL2_INCLUDE_DIR=%{_includedir}                              \
        -DSASL2_LIBRARIES=%{_prefix}/gnu/lib/libsasl2.so                \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-%{version}-64
export PATH="%{qt4_bin_path64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
cd ..
%endif

cd %{src_dir}-%{version}
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ..
export PATH="${OPATH}"

mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/qt4/mkspecs/features
mv ${RPM_BUILD_ROOT}%{_prefix}/mkspecs/features/* ${RPM_BUILD_ROOT}%{_datadir}/qt4/mkspecs/features
rm -rf ${RPM_BUILD_ROOT}%{_prefix}/mkspecs

if [ -d ${RPM_BUILD_ROOT}%{_prefix}/certs ]
then
	mkdir -p ${RPM_BUILD_ROOT}%{_sysconfdir}/certs/qca
        mv ${RPM_BUILD_ROOT}%{_prefix}/certs/* ${RPM_BUILD_ROOT}%{_sysconfdir}/certs/qca
        rm -rf ${RPM_BUILD_ROOT}%{_prefix}/certs
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_prefix}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/qcatool2

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/qcatool2.1

%dir %attr (0755, root, bin) %{_datadir}/qt4
%dir %attr (0755, root, bin) %{_datadir}/qt4/mkspecs
%dir %attr (0755, root, bin) %{_datadir}/qt4/mkspecs/features
%{_datadir}/qt4/mkspecs/features/crypto.prf

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/qt4
%dir %attr (0755, root, bin) %{_libdir}/qt4/plugins
%dir %attr (0755, root, bin) %{_libdir}/qt4/plugins/crypto
%{_libdir}/qt4/plugins/crypto/libqca*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/qt4
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/qt4/plugins
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/qt4/plugins/crypto
%{_libdir}/%{_arch64}/qt4/plugins/crypto/libqca*
%endif

%dir %attr (0755, root, sys) %{_sysconfdir}
%dir %attr (0755, root, sys) %{_sysconfdir}/certs
%dir %attr (0755, root, sys) %{_sysconfdir}/certs/qca
%{_sysconfdir}/certs/qca/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/qca2.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/qca2.pc
%endif

%changelog
* Fri May 22 2009 - moinakg@belenix.org
- Initial version.
