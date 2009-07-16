#
# spec file for package SFElibnova
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc
%define gcc4_extra_opts -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -ftree-loop-distribution -fivopts -ftree-loop-im

Name:			SFElibnova
License:		LGPLv2+
Group:			Development/Libraries
Version:		0.13.0
Summary:		Libnova is a general purpose astronomy & astrodynamics library
Source:			%{sf_download}/libnova/libnova-%{version}.tar.gz

URL:			http://libnova.sourceforge.net/
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}

%description
Libnova is a general purpose, double precision, celestial mechanics, 
astrometry and astrodynamics library.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%prep
%if %cc_is_gcc
%else
	%error "This spec file needs to be built with Gcc"
%endif
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -pr libnova-%{version} libnova-%{version}-64
%endif

%build
%ifarch amd64 sparcv9
cd libnova-%{version}-64
export CFLAGS="%optflags64 %gcc4_extra_opts"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64} -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --bindir=%{_bindir}/%{_arch64} \
    --libdir=%{_libdir}/%{_arch64} \
    --enable-shared \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

for mk in `find . -name Makefile`
do
	cp ${mk} ${mk}.orig
	cat ${mk}.orig | sed 's#CFLAGS = -Wall#%optflags64 -Wall %gcc4_extra_opts#' > ${mk}
done

make -j 2
cd ..
%endif

cd libnova-%{version}
export CFLAGS="%optflags %gcc4_extra_opts"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L/lib -R/lib -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --libdir=%{_libdir} \
    --enable-shared \
    --disable-static \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir}

for mk in `find . -name Makefile`
do
	cp ${mk} ${mk}.orig
	cat ${mk}.orig | sed 's#CFLAGS = -Wall#%optflags -Wall %gcc4_extra_opts#' > ${mk}
done

make -j 2

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd libnova-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd libnova-%{version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
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

%changelog
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
