Summary: The zlib compression and decompression library
Name: zlib
Version: 1.2.3
Release: 1%{?dist}
Group: System Environment/Libraries
#Source: http://www.zlib.net/zlib-%{version}.tar.bz2
Source: http://prdownloads.sourceforge.net/libpng/zlib-1.2.3.tar.gz
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

%build
export CFLAGS="%optflags"

%if %build_64bit
%if %gcc_compiler
CFLAGS="$CFLAGS -O3 -msse2 -ftree-vectorize -flto -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -floop-parallelize-all -ftree-loop-distribution"
export LDSHARED="$CC -shared %_ldflags -flto"
%endif
%else
%if %gcc_compiler
CFLAGS="$CFLAGS -O3 -flto -ftree-loop-linear -floop-interchange -floop-strip-mine -floop-block -floop-parallelize-all -ftree-loop-distribution"
export LDSHARED="$CC -shared %_ldflags -flto"
%endif
%endif

bash ./configure --shared --libdir=%{buildroot}/%{_libdir} --includedir=%{buildroot}/%{_includedir} --prefix=%{buildroot}/%{_prefix}
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
%{_lib}/*
%{_libdir}/*
#%{_pkgconfigdir}/*

%files devel
%defattr (0655, root, bin)
%{_includedir}/*
%{_mandir}/*
