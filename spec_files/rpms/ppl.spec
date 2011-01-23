Name:    ppl
Version: 0.10.2
#Version: 0.11
Release: 2%{?dist}
Summary: The Parma Polyhedra Library: a library of numerical abstractions
Source:  ftp://gcc.gnu.org/pub/gcc/infrastructure/ppl-%{version}.tar.gz
#Source: http://www.cs.unipr.it/ppl/Download/ftp/releases/%{version}/ppl-%{version}.tar.bz2
Source1: ppl.hh
Source2: ppl_c.h
Source3: pwl.hh
Patch1:  ppl-01-CS.diff
Patch2:  ppl-02-defs.diff
Group:   Development/Libraries
License: GPLv3+
URL:     http://www.cs.unipr.it/ppl/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires: zlib
Requires: gmp
BuildRequires: gmp-devel
#Requires: libms
#Requires: libgcc
#BuildRequires: gcc

%description
The Parma Polyhedra Library (PPL) is a library for the manipulation of
(not necessarily closed) convex polyhedra and other numerical
abstractions.  The applications of convex polyhedra include program
analysis, optimized compilation, integer and combinatorial
optimization and statistical data-editing.  The Parma Polyhedra
Library comes with several user friendly interfaces, is fully dynamic
(available virtual memory is the only limitation to the dimension of
anything), written in accordance to all the applicable standards,
exception-safe, rather efficient, thoroughly documented, and free
software.  This package provides all what is necessary to run
applications using the PPL through its C and C++ interfaces.

%package devel
Summary:                 %{summary} - development files
Requires: %name

%description devel
The header files, Autoconf macro and minimal documentation for
developing applications using the Parma Polyhedra Library through
its C and C++ interfaces.

%package doc
Summary:                 %{summary} - documentation files
Requires: %name

%description doc
Documentation files for the Parma Polyhedra Library (PPL) library.

%prep
%setup -q -c -n %name-%version
cd ppl-%{version}
%patch1 -p1
%patch2 -p0

for f in `find . -type f | grep -v configure | xargs grep -w int8_t | cut -f1 -d":"`
do
	cp ${f} ${f}.orig
	cat ${f}.orig | gsed 's/uint8_t/UINT8_T/g
s/int8_t/signed char/g' > ${f}
done
cd ..

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I%{_includedir} -I%{_includedir}/gmp -fexceptions -DUINT8_T=uint8_t"

cd ppl-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags"
export PATH=/usr/gnu/bin:${PATH}

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --bindir=%{_bindir}              \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --with-pic                       \
            --enable-optimization=standard   \
%ifarch x86_64
            --enable-fpmath=sse2+387         \
%endif
            --enable-shared                  \
            --disable-static

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

cd ppl-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

normalized_arch=%{_arch}
%ifarch i686
normalized_arch=i386
%endif

mv %{buildroot}/%{_includedir}/ppl.hh %{buildroot}/%{_includedir}/ppl-${normalized_arch}.hh
ginstall -m644 %{SOURCE1} %{buildroot}/%{_includedir}/ppl.hh
mv %{buildroot}/%{_includedir}/ppl_c.h %{buildroot}/%{_includedir}/ppl_c-${normalized_arch}.h
ginstall -m644 %{SOURCE2} %{buildroot}/%{_includedir}/ppl_c.h
mv %{buildroot}/%{_includedir}/pwl.hh %{buildroot}/%{_includedir}/pwl-${normalized_arch}.hh
ginstall -m644 %{SOURCE3} %{buildroot}/%{_includedir}/pwl.hh
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ppl*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%files doc
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.hh
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Wed May 06 2009 - moinakg@belenix.org
- Initial spec file.
