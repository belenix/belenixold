#
# spec file for package SFEid3lib
#
# includes module(s): id3lib
#
#
%include Solaris.inc

Name:                    SFEeigen
Summary:                 A C++ template library for linear algebra
Version:                 2.0.1
Source:                  http://download.tuxfamily.org/eigen/eigen-%{version}.tar.bz2
License:                 LGPL3

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          COPYING.LESSER
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEcmake
BuildRequires: SFEdoxygen
Requires: SUNWlibm

%prep
%if %cc_is_gcc
%else
error "This spec file requires /usr/gnu/bin/g++. Please set your environment variables."
%endif

%setup -q -c -n %name-%version
cd eigen-%version
cd ..

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

cd eigen-%{version}
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib -lstdc++"
export CFLAGS="-O3 -fno-omit-frame-pointer -fPIC -DPIC"
export CXXFLAGS="-O3 -fno-omit-frame-pointer -fPIC -DPIC"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=$(CC)                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"				\
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}				\
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"			\
        -DLIB_INSTALL_DIR=%{_libdir}                                    \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
doxygen
cd ..

%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

cd eigen-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p ${RPM_BUILD_ROOT}%{_datadir}/doc/eigen
cp -r html ${RPM_BUILD_ROOT}%{_datadir}/doc/eigen
cp COPYING COPYING.LESSER ${RPM_BUILD_ROOT}%{_datadir}/doc/eigen
cd ..



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/doc/eigen
%doc %{_datadir}/doc/eigen/*

%changelog
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Remove unused devel package definition.
* Mon May 04 2009 - moinakg@belenix.org
- Initial version.
