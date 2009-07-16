#
# spec file for package SFEgsl
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:			SFEgsl
License:		GPLv3 and GFDL and BSD
Group:			Development/Libraries
Version:		1.12
Summary:		The GNU Scientific Library for numerical analysis
Source:			ftp://ftp.gnu.org/gnu/gsl/gsl-%{version}.tar.gz
Patch1:                 gsl-01-gsl-config.in.diff

URL:			http://www.gnu.org/software/gsl/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
SUNW_Copyright:         %{name}.copyright
Requires: SFEgccruntime
BuildRequires: SFEgcc

%description
The GNU Scientific Library (GSL) is a collection of routines for
numerical analysis, written in C.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SFEgcc

%package static
Summary:                 %{summary} - static libraries
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%setup -q -c -n %name-%version
cd gsl-%{version}
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr gsl-%{version} gsl-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd gsl-%{version}-64
export CFLAGS="%optflags64 -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64} -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir}/%{_arch64} \
    --libdir=%{_libdir}/%{_arch64} \
    --enable-shared \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} CFLAGS="$CFLAGS -fgnu89-inline"

make -j 2
cd ..
%endif

cd gsl-%{version}
export CFLAGS="%optflags -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L/lib -R/lib -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} CFLAGS="$CFLAGS -fgnu89-inline"

make -j 2

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd gsl-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd gsl-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir

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
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

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

%files static
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.a

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.a
%endif

%changelog
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
