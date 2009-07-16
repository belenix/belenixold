#
# spec file for package SFEcln
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:			SFEcln
License:		GPLv2+
Group:			System Environment/Libraries
Version:		1.3.0
Summary:		Class Library for Numbers
Source:			http://www.ginac.de/CLN/cln-%{version}.tar.bz2

URL:			http://www.ginac.de/CLN/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires:      SFEgmp
BuildRequires: SFEgmp-devel
BuildRequires: SUNWtexi

%description
A collection of C++ math classes and functions, which are designed for
memory and speed efficiency, and enable type safety and algebraic
syntax.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires: SFEgmp-devel
Requires: SUNWtexi

%prep
%setup -q -c -n %name-%version
cd cln-%{version}
cd ..

%ifarch amd64 sparcv9
cp -pr cln-%{version} cln-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd cln-%{version}-64
export CFLAGS="%optflags64 -I%{_includedir}/%{_arch64} -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im"
export CXXFLAGS="%cxx_optflags64 -I%{_includedir}/%{_arch64} -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im"
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64}"
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir}/%{_arch64} \
    --libdir=%{_libdir}/%{_arch64} \
    --includedir=%{_includedir}/%{_arch64} \
    --enable-shared \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

make -j 2
cd ..
%endif

cd cln-%{version}
export CFLAGS="%optflags -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im"
export CXXFLAGS="%cxx_optflags -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im"
export LDFLAGS="%_ldflags -L/lib -R/lib"

./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

make -j 2

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd cln-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd cln-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

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
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
