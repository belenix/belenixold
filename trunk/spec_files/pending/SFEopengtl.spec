#
# spec file for package SFEopengtl
#
# includes module(s): opengtl
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

%define python_version   2.6
Name:                    SFEopengtl
Summary:                 The Graphics Transformation Languages
Version:                 0.9.9
URL:                     http://openctl.org/
Source:                  http://www.opengtl.org/download/OpenGTL-%{version}.tar.bz2
%define src_dir          OpenGTL-%{version}

License:                 GPLv3+
SUNW_BaseDir:            %{_basedir}
#SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SFEqt4
BuildRequires: SFEqt4-devel
BuildRequires: SFEcmake
BuildRequires: SUNWgnome-common-devel


%description
The Graphics Transformation Languages is a set of library for using
and integrating transformation algorithms (such as filter or color
conversion) in graphics applications. The goal is to provide the
tools, languages and libraries to create generic transformation for
graphics. Those transformations could then be used by different
programs (Krita, The Gimp, CinePaint, gegl...).

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEqt4-devel
Requires: SFEcmake
Requires: SUNWgnome-common-devel

%prep
%setup -q -c -n %name-%version
cd %{src_dir}
#%patch1 -p1
cd ..

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
export JAVA_HOME=%{_prefix}/java
OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-64
mkdir opengtl-bld-64
cd opengtl-bld-64

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
        -DLIB_INSTALL_DIR=%{_libdir}/%{_arch64}                         \
        -DCMAKE_VERBOSE_MAKEFILE=1 .. > config.log 2>&1

make VERBOSE=1
cd ../..
%endif

cd %{src_dir}
mkdir opengtl-bld
cd opengtl-bld

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
        -DCMAKE_VERBOSE_MAKEFILE=1 .. > config.log 2>&1

make VERBOSE=1
cd ../..
export PATH="${OPATH}"


%install
rm -rf $RPM_BUILD_ROOT

OPATH=${PATH}

%ifarch amd64 sparcv9
cd %{src_dir}-64/opengtl-bld-64
export PATH="%{qt4_bin_path64}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.a
#mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages \
#   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages
#mkdir ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/qzion/64
#mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/qzion/*.so \
#   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/qzion/64

mkdir -p ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_libdir}/*.so* ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
mv ${RPM_BUILD_ROOT}%{_libdir}/pkgconfig ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}
cd ../..
%endif

cd %{src_dir}/opengtl-bld
export PATH="%{qt4_bin_path}:${OPATH}"

make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.a
#mv ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages/qzion/* \
#   ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/vendor-packages/qzion
#rm -r ${RPM_BUILD_ROOT}%{_libdir}/python%{python_version}/site-packages
cd ../..
export PATH="${OPATH}"


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%dir %attr (0755, root, sys) %{_datadir}
#%dir %attr (0755, root, bin) %{_datadir}/sip
#%dir %attr (0755, root, bin) %{_datadir}/sip/qzion
#%{_datadir}/sip/qzion/*

#%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}
#%dir %attr (0755, root, bin) %{_libdir}/python%{python_version}/vendor-packages
#%{_libdir}/python%{python_version}/vendor-packages/*

%ifarch amd64 sparcv9
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
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version.
