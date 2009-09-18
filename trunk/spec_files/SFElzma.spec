#
# spec file for package SFExz
#
# includes module(s): xz-utils
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFElzma
Summary:                 Utilities and libraries for the LZMA compression algo and XZ container format
Version:                 5.0
%define tarball_version  4.999.9beta
URL:                     http://tukaani.org/xz/
Source:                  http://tukaani.org/xz/xz-%{tarball_version}.tar.gz
License:                 LGPLv2+

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          SFExz.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibm

%description
XZ Utils is free general-purpose data compression software with high
compression ratio. XZ Utils were written for POSIX-like systems
(GNU/Linux, *BSDs, etc.), but also work on some not-so-POSIX systems
like Windows. XZ Utils are the successor to LZMA Utils. 

%package devel
Summary:                 Development files for the LZMA compression algo
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%if %cc_is_gcc
%else
error "This spec file requires /usr/gnu/bin/g++. Please set your environment variables."
%endif

%setup -q -c -n %name-%version
cd xz-%tarball_version
cd ..

%ifarch amd64 sparcv9
cp -rp xz-%{tarball_version} xz-%{tarball_version}-64
%endif

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"
export GCC="yes"
export CC=/usr/gnu/bin/gcc
export CXX=/usr/gnu/bin/gcc
export LFS_CFLAGS=`/usr/bin/getconf LFS_CFLAGS`

%ifarch amd64 sparcv9
cd xz-%{tarball_version}-64

export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++"
export CFLAGS="%optflags64 -fno-strict-aliasing"
export CXXFLAGS="%cxx_optflags64 -fno-strict-aliasing"

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes         \
            --disable-assembler         \
            --disable-static

/usr/gnu/bin/sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
/usr/gnu/bin/sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make VERBOSE=1
cd ..
%endif

cd xz-%{tarball_version}
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++"
export CFLAGS="%optflags ${LFS_CFLAGS} -fno-strict-aliasing"
export CXXFLAGS="%cxx_optflags ${LFS_CFLAGS} -fno-strict-aliasing"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
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

%ifarch amd64 sparcv9
cd xz-%{tarball_version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd xz-%{tarball_version}
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la
cd ..


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/*.so*
%endif

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/xz
%{_docdir}/xz/*

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
* Fri Sep 18 2009 - moinakg(at)belenix<dot>org
- Major update to new XZ version needed for KDE4.
* Fri Jul 03 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
