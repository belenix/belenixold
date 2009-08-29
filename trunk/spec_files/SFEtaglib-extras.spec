#
# spec file for package SFEtaglib-extras
#
# includes module(s): taglib-extras
#
#
%include Solaris.inc

Name:                    SFEtaglib-extras
Summary:                 Taglib support for other formats
Version:                 0.1.6
Group:                   Applications/Multimedia
License:                 LGPLv2
URL:                     http://websvn.kde.org/trunk/kdesupport/taglib-extras/
Source:                  http://www.kollide.net/~jefferai/taglib-extras-%{version}.tar.gz
Patch1:                  taglib-extras-01-wcscasecmp.diff

SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWzlib
Requires: SFEtaglib
Requires: SFEkdelibs4
%if %cc_is_gcc
Requires: SFEgccruntime
%else
Requires: SUNWlibC
%endif
BuildRequires: SFEtaglib-devel
BuildRequires: SFEkdelibs4-devel
BuildRequires: SFEcmake

%description
Taglib-extras delivers support for reading and editing the meta-data of 
audio formats not supported by taglib, including: asf, mp4v2, rmff, wav.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFEtaglib-devel
Requires: SFEkdelibs4-devel
Requires: SFEcmake

%prep
%setup -q -n taglib-extras-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

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

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

if [ "x`basename $CC`" = xgcc ]
then
	export LDFLAGS="%_ldflags -lc -lstdc++"
else
	export LDFLAGS="%_ldflags -lc -lCrun -lCstd"
fi

export PKG_CONFIG_PATH=%{_prefix}/lib/pkgconfig:%{_prefix}/gnu/lib/pkgconfig
export CMAKE_LIBRARY_PATH="%{xorg_lib}:%{gnu_lib}:%{_prefix}/lib:/lib"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_SKIP_RPATH:BOOL=YES                                     \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DWITH_KDE=1                                                    \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1
export PATH="${OPATH}"



%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT/%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Sat Aug 29 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial spec
