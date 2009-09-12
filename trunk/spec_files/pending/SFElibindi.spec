#
# spec file for package SFElibindi
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:			SFElibindi
License:		LGPLv2+ and GPLv2+
Group:			Development/Libraries
Version:		0.6
Summary:		Instrument Neutral Distributed Interface
Source:			%{sf_download}/indi/libindi0_%{version}.tar.gz
Patch1:                 libindi-01-suffix.diff
Patch2:                 libindi-02-cfitsio.diff

URL:			http://indi.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires:      SUNWzlib
Requires:      SFEcfitsio
Requires:      SFElibnova
Requires:      SFElibfli
BuildRequires: SUNWzlib
BuildRequires: SFEcmake
BuildRequires: SFElibnova-devel
BuildRequires: SFEcfitsio-devel
BuildRequires: SFElibfli-devel

%description
INDI is a distributed control protocol designed to operate
astronomical instrumentation. INDI is small, flexible, easy to parse,
and scalable. It supports common DCS functions such as remote control,
data acquisition, monitoring, and a lot more.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SUNWzlib
Requires: SFEcfitsio-devel

%prep
%setup -q -c -n %name-%version
cd libindi0-%{version}
%patch1 -p1
%patch2 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr libindi0-%{version} libindi0-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd libindi0-%{version}-64
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64} -lsocket -lnsl -lresolv -L$RPM_BUILD_ROOT%{_libdir}"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1 -j 2
cd ..
%endif

cd libindi0-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -L/lib -R/lib -lsocket -lnsl -lresolv -L$RPM_BUILD_ROOT%{_libdir}"

cmake   -DCMAKE_INSTALL_PREFIX=%{_prefix}                               \
        -DCMAKE_BUILD_TYPE=Release                                      \
        -DCMAKE_C_COMPILER:FILEPATH=${CC}                               \
        -DCMAKE_C_FLAGS:STRING="${CFLAGS}"                              \
        -DCMAKE_CXX_COMPILER:FILEPATH=${CXX}                            \
        -DCMAKE_CXX_FLAGS_RELEASE:STRING="${CXXFLAGS}"                  \
        -DBUILD_SHARED_LIBS=On                                          \
        -DCMAKE_VERBOSE_MAKEFILE=1 . > config.log 2>&1

make VERBOSE=1 -j 2

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd libindi0-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd libindi0-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

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
* Sun Jul 05 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Add dependency on SFEgccruntime for Gcc builds.
* Fri May 29 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Add patch for building with Gcc 4.4.
- Add lib paths to properly detect some libs.
* Tue Feb 10 2009 - moinakg@gmail.com
- Bump version to 1.3.3.
- Add 64Bit build.
* Tue Jan 22 2008 - moinak.ghosh@sun.com
- Initial spec.
