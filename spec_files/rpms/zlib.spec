Summary: The zlib compression and decompression library
Name: zlib
Version: 1.2.5
Release: 2%{?dist}
Group: System Environment/Libraries
Source: http://www.zlib.net/zlib-%{version}.tar.bz2
Patch1: zlib-1.2.5-gentoo.patch
URL: http://www.gzip.org/zlib/
License: zlib and Boost
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#BuildRequires: gnu-sed
#BuildRequires: automake, autoconf, libtool

%description
Zlib is a general-purpose, patent-free, lossless data compression
library which is used by many different programs.

%package devel
Summary: Header files and libraries for Zlib development
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
The zlib-devel package contains the header files and libraries needed
to develop programs that use the zlib compression and decompression
library.

%prep
%setup -q 
%patch1 -p1

%build
export CFLAGS="%optflags"
%if %build_64bit
%if %gcc_compiler
CFLAGS="$CFLAGS -O2 -msse2 -ftree-vectorize -flto -ftree-loop-linear -floop-interchange -floop-block"
%endif
%else
%if %gcc_compiler
CFLAGS="$CFLAGS -O2 -flto -ftree-loop-linear -floop-interchange -floop-block"
%endif
%endif

./configure --libdir=%{_libdir} --includedir=%{_includedir} --prefix=%{_prefix}
gmake

%install
rm -rf ${RPM_BUILD_ROOT}

make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_lib}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
mv $RPM_BUILD_ROOT%{_libdir}/libz.so* $RPM_BUILD_ROOT/%{_lib}/

reldir=$(echo %{_libdir} | gsed 's,/$,,;s,/[^/]\+,../,g')%{_lib}
(cd $RPM_BUILD_ROOT%{_libdir}/
 for f in `(cd $RPM_BUILD_ROOT/%{_lib}/; ls)`; do
   ln -s ${reldir}/${f}
 done)

# Remove the pkgconfig file for now. We need to revert this later once we
# have full system packages and fixed the crazy pkgconfig inclusion in
# gettext package in OpenIndiana.

rm -rf $RPM_BUILD_ROOT%{_libdir}/pkgconfig

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr (0655, root, bin)
%dir %attr(0755, root, bin) %{_lib}
%{_lib}/*
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*
#%dir %attr(0755, root, other) %{_pkgconfigdir}
#%{_pkgconfigdir}/*

%files devel
%defattr (0655, root, bin)
%dir %attr(0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/*
