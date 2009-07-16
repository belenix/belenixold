#
# spec file for package SFEcfitsio
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:			SFEcfitsio
License:		GPLv2+
Group:			Development/Libraries
Version:		3181
Summary:		Library for manipulating FITS data files
Source:			ftp://heasarc.gsfc.nasa.gov/software/fitsio/c/cfitsio3181.tar.gz
Patch1:                 cfitsio-01-Makefile.in.diff
Patch2:                 cfitsio-02-drvrfile.c.diff
Patch3:                 cfitsio-03-cfitsio.pc.in.diff

URL:			http://heasarc.gsfc.nasa.gov/docs/software/fitsio/fitsio.html
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
SUNW_BaseDir:		%{_prefix}
Requires: SFEgccruntime
BuildRequires: SFEgcc

%description
CFITSIO is a library of C and FORTRAN subroutines for reading and writing 
data files in FITS (Flexible Image Transport System) data format. CFITSIO 
simplifies the task of writing software that deals with FITS files by 
providing an easy to use set of high-level routines that insulate the 
programmer from the internal complexities of the FITS file format. At the 
same time, CFITSIO provides many advanced features that have made it the 
most widely used FITS file programming interface in the astronomical 
community.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
Requires:                SFEgcc

%prep
%setup -q -c -n %name-%version
cd cfitsio
%patch1 -p1
%patch2 -p1
%patch3 -p1
cd ..

%ifarch amd64 sparcv9
cp -pr cfitsio cfitsio-64
%endif

%build
%ifarch amd64 sparcv9
cd cfitsio-64
export CFLAGS="%optflags64 -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags64 -L/lib/%{_arch64} -R/lib/%{_arch64} -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --includedir=%{_includedir}/cfitsio \
    --libdir=%{_libdir}/%{_arch64} \
    --enable-shared \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-reentrant

make -j 2 shared 
cd ..
%endif

cd cfitsio
export CFLAGS="%optflags -D_LARGEFILE64_SOURCE -D_FILE_OFFSET_BITS=64"
export LD=/usr/ccs/bin/ld
export LDFLAGS="%_ldflags -L/lib -R/lib -L$RPM_BUILD_ROOT%{_libdir}"
./configure \
    --prefix=%{_prefix} \
    --includedir=%{_includedir}/cfitsio \
    --libdir=%{_libdir} \
    --enable-shared \
    --with-pic \
    --mandir=%{_mandir} \
    --infodir=%{_infodir} \
    --enable-reentrant
 
#%patch1 -p1

make -j 2 shared

%install
rm -rf $RPM_BUILD_ROOT
%ifarch amd64 sparcv9
cd cfitsio-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/lib*a
cd ..
%endif

cd cfitsio
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
* Thu Jul 16 2009 - moinakg(at)belenix<dot>org
- Initial spec.
