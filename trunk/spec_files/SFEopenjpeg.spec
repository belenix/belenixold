#
# spec file for package SFEopenjpeg
#
# includes module(s): openjpeg
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          OpenJPEG
Name:                    SFEopenjpeg
Summary:                 An open-source JPEG 2000 codec written in C language.
Version:                 v1_3
License:                 BSD
Source:                  http://www.openjpeg.org/openjpeg_%{version}.tar.gz
URL:                     http://www.openjpeg.org/

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen

%description
OpenJPEG is an open-source JPEG 2000 codec written in C language. It has been
developed in order to promote the use of JPEG 2000, the new still-image
compression standard from the Joint Photographic Experts Group (JPEG).

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -c -n %name-%version

%ifarch amd64 sparcv9
cp -rp %{src_dir}_%{version} %{src_dir}_%{version}-64
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
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/gcc

%ifarch amd64 sparcv9
cd %{src_dir}_%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
        -DBIN_INSTALL_DIR=%{_bindir}/%{_arch64}                         \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
%endif

cd %{src_dir}_%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DBIN_INSTALL_DIR=%{_bindir}                                    \
        -DINCLUDE_INSTALL_DIR=%{_includedir}                            \
        -DBUILD_SHARED_LIBS=On                                          \
        -DBUILD_DOCUMENTATION=On                                        \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{src_dir}_%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a

#
# LIB and BIN install dirs are not honoured by openjpeg cmake files.
#
mkdir -p ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_bindir}/frames_to_mj2 ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_bindir}/mj2_to_frames ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_bindir}/wrap_j2k_in_mj2 ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_bindir}/extract_j2k_from_mj2 ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_libdir}/*.so* ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
cd ..
%endif

cd %{src_dir}_%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
rm -rf ${RPM_BUILD_ROOT}/openjpeg
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/frames_to_mj2
%{_bindir}/mj2_to_frames
%{_bindir}/wrap_j2k_in_mj2
%{_bindir}/extract_j2k_from_mj2
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/frames_to_mj2
%{_bindir}/%{_arch64}/mj2_to_frames
%{_bindir}/%{_arch64}/wrap_j2k_in_mj2
%{_bindir}/%{_arch64}/extract_j2k_from_mj2
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Avoid stripping of binaries.
* Sun Apr 17 2009 - moinakg@belenix.org
- Fix minor specfile bug.
* Sat May 16 2009 - moinakg@belenix.org
- Pull in from SFE repo.
* Tue Apr 28 2009 - moinakg@belenix.org
- Add 64Bit build.
- Add patch to fix iomanip include for Gcc4.
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFEopenjpeg
- changed to root:bin to follow other JDS pkgs.
- added dependencies
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
