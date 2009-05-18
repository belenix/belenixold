#
# spec file for package SFEautomoc
#
# includes module(s): Automoc
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define maj_ver          1.0
%define min_ver          0.9.88
%define tarball_dir      automoc-%{maj_ver}~version-%{min_ver}
Name:                    SFEautomoc
Summary:                 Automatic moc for Qt 4 packages
Version:                 %{maj_ver}_%{min_ver}
URL:                     http://packages.debian.org/sid/automoc
Source:                  http://ftp.de.debian.org/debian/pool/main/a/automoc/automoc_%{maj_ver}~version-%{min_ver}.orig.tar.gz

License:                 GPL2
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
Requires:                SFEqt4
BuildRequires:           SFEqt4-devel
BuildRequires:           SFEcmake

%include default-depend.inc

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp %{tarball_dir} %{tarball_dir}-64
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
cd %{tarball_dir}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++"

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
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..
%endif

cd %{tarball_dir}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++"

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
        -DBUILD_DOCUMENTATION=On                                        \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
cd ..

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd %{tarball_dir}-64
make install DESTDIR=${RPM_BUILD_ROOT}

#
# Automoc build does not honour BINDIR
#
mkdir ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_bindir}/automoc4 ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
cd ..
%endif

cd %{tarball_dir}
make install DESTDIR=${RPM_BUILD_ROOT}
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/automoc4
%{_libdir}/automoc4/Automoc4Version.cmake
%{_libdir}/automoc4/automoc4.files.in
%{_libdir}/automoc4/Automoc4Config.cmake

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/automoc4

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/automoc4
%endif

%changelog
* Sun Apr 17 2009 - moinakg@belenix.org
- Initial version.
