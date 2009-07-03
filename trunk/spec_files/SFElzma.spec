#
# spec file for package SFElzma-utils
#
# includes module(s): lzma-utils
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc


Name:                    SFElzma
Summary:                 Utilities and libraries for the LZMA compression algo
Version:                 4.32.7
URL:                     http://tukaani.org/lzma/
Source:                  http://tukaani.org/lzma/lzma-%{version}.tar.gz
License:                 LGPLv2+

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          SFElzma.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibm

%description
LZMA provides very high compression ratio and fast decompression. The
core of the LZMA utils is Igor Pavlov's LZMA SDK containing the actual
LZMA encoder/decoder. LZMA utils add a few scripts which provide
gzip-like command line interface and a couple of other LZMA related
tools. 

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
cd lzma-%version
cd ..

%ifarch amd64 sparcv9
cp -rp lzma-%{version} lzma-%{version}-64
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
cd lzma-%{version}-64

export LDFLAGS="%_ldflags64 %{gnu_lib_path64} -lstdc++"
export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes         \
            --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make VERBOSE=1
cd ..
%endif

cd lzma-%{version}
export LDFLAGS="%_ldflags %{gnu_lib_path} -lstdc++"
export CFLAGS="%optflags ${LFS_CFLAGS}"
export CXXFLAGS="%cxx_optflags ${LFS_CFLAGS}"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes         \
            --disable-static

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

make VERBOSE=1
cd ..

%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"
export CONFIG_SHELL="/bin/bash"
export MAKESHELL="/bin/bash"

%ifarch amd64 sparcv9
cd lzma-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd lzma-%{version}
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

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Fri Jul 03 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
