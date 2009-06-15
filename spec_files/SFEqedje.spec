#
# spec file for package SFEqedje
#
# includes module(s): qedje
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define src_dir          qedje-mainline
%define python_version   2.6
Name:                    SFEqedje
Summary:                 A library combining the benefits of Edje and Qt
Version:                 0.4.0
URL:                     http://code.openbossa.org/projects/
Source:                  http://code.openbossa.org/projects/qedje/repos/mainline/archive/0206ec8f2a802bf51455179933d8b7ab3e41a38b.tar.gz
License:                 GPLv3+

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
Requires:      SFEeet
Requires:      SFEqzion
Requires:      SUNWPython26
Requires:      SFEpython26-sip
Requires:      SFEpython26-pyqt4
BuildRequires: SFEeet-devel
BuildRequires: SFEqzion-devel
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SUNWPython26-devel
BuildRequires: SFEpython26-sip
BuildRequires: SFEpython26-pyqt4-devel


%description
The main purpose of the QEdje project is to build a bridge among components
that proved to have great value for open source developers: Edje and Qt. This
will extend the Qt toolkit with the flexibility of a declarative language, such
as Edje, and also enable Qt widgets to be embedded into Edje UI design.


%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEeet-devel
Requires: SFEqzion-devel
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SUNWPython26-devel
Requires: SFEpython26-sip
Requires: SFEpython26-pyqt4-devel


%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp %{src_dir} %{src_dir}-64
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
export CMAKE_INCLUDE_PATH="%{gnu_inc}:%{xorg_inc}"
OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-64
mkdir qedje-bld-64
cd qedje-bld-64

export CFLAGS="%optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags64 -I${QT_INCLUDES} -I%{gnu_inc}"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++ %{xorg_lib_path64}"
export PATH="%{qt4_bin_path64}:%{_bindir}/%{_arch64}:%{_prefix}/gnu/bin/%{_arch64}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/%{_arch64}/pkgconfig:%{_prefix}/gnu/lib/%{_arch64}/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib64}:%{gnu_lib64}:%{_prefix}/lib/%{_arch64}:/lib/%{_arch64}"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DBUILD_SHARED_LIBS=On                                          \
        -DPC_QZion_LDFLAGS="-L%{_libdir}/%{_arch64} -R%{_libdir}/%{_arch64} -lqzion" \
        -DCMAKE_VERBOSE_MAKEFILE=1 .. > config.log 2>&1

make VERBOSE=1
cd ../..
%endif

cd %{src_dir}
mkdir qedje-bld
cd qedje-bld

export CFLAGS="%optflags -I%{gnu_inc}"
export CXXFLAGS="%cxx_optflags -I%{gnu_inc}"
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++ %{xorg_lib_path}"
export PATH="%{qt4_bin_path}:${OPATH}"
export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DCMAKE_INCLUDE_PATH="%{gnu_inc}"				\
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 .. > config.log 2>&1

make VERBOSE=1
cd ../..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-64/qedje-bld-64
export PATH="%{qt4_bin_path64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_libdir}/*.so* ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}

mkdir -p ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_bindir}/qed* ${RPM_BUILD_ROOT}%{_bindir}/%{_arch64}
cd ../..
%endif

cd %{src_dir}/qedje-bld
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
cd ../..
export PATH="${OPATH}"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/qed*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/qed*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*.pc

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%changelog
* Mon Jun 15 2009 - moinakg@belenix(dot)org
- Initial version.
