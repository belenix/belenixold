Name:           xz
Summary:        Utilities for the LZMA compression algo and XZ container format
Version:        5.0.0
%define tarball_version  5.0.0
URL:            http://tukaani.org/xz/
Source:         http://tukaani.org/xz/xz-%{tarball_version}.tar.gz
License:        LGPLv2+
Release:        1%{?dist}
Group:          Applications/File
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
Requires:       %{name}-libs = %{version}-%{release}

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils were written for POSIX-like systems
(GNU/Linux, *BSDs, etc.), but also work on some not-so-POSIX systems
like Windows. XZ Utils are the successor to LZMA Utils. 

%package        libs
Summary:        Libraries for decoding LZMA compression
Group:          System Environment/Libraries
License:        LGPLv2+
%if %gcc_compiler
Requires:       libstdc++
Requires:       libgcc
%endif

%description    libs
Libraries for decoding files compressed with LZMA or XZ utils.

%package devel
Summary:                 Development files for the LZMA compression algo
Requires: %{name}-libs = %{version}-%{release}

%description devel
Development header files and documentation for the XZ utils and library package.

%if %build_l10n
%package    l10n
Version:    %{version}
Group:      System Environment/Libraries
License:    GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Summary:    %{summary} - l10n files
Requires:   %{name}
%endif

%prep
%if %gcc_compiler
%else
error "This spec file requires /usr/bin/g++. Please set your environment variables."
%endif
%bsetup

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=/usr/bin/gcc
export CXX=/usr/bin/gcc
export LFS_CFLAGS=`/usr/bin/getconf LFS_CFLAGS`

cd xz-%{tarball_version}
export LDFLAGS="%_ldflags -lstdc++"
export CFLAGS="%optflags ${LFS_CFLAGS} -fno-strict-aliasing"
export CXXFLAGS="%cxx_optflags ${LFS_CFLAGS} -fno-strict-aliasing"

%if %{build_64bit}
CFLAGS="${CFLAGS} -msse2 -ftree-vectorize -flto -ftree-loop-linear -floop-parallelize-all -floop-block"
%else
CFLAGS="${CFLAGS} -flto -ftree-loop-linear -floop-parallelize-all -floop-block"
%endif

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}         \
            --libdir=%{_libdir}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --docdir=%{_docdir}/xz \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes         \
            --disable-static

/usr/gnu/bin/sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
/usr/gnu/bin/sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make VERBOSE=1
cd ..

%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

cd xz-%{tarball_version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}/*
%{_mandir}/*

%files libs
%defattr (-, root, bin)
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}/*
%{_pkgconfigdir}/*
%dir %{_docdir}/xz

%defattr (-, root, other)
%{_docdir}/xz/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%{_localedir}/*
%endif

%changelog
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- Major update to new XZ version needed for KDE4.
* Fri Jul 03 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
