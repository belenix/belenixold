#
# spec file for package SFElibarchive
#
# includes module(s): libarchive
#
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                    SFElibarchive
Summary:                 A library for handling streaming archive formats
Version:                 2.7.1
License:                 BSD
URL:                     http://code.google.com/p/libarchive/
Source:                  http://libarchive.googlecode.com/files/libarchive-%{version}.tar.gz
Patch1:                  libarchive-01-write_disk.c.diff
Patch2:                  libarchive-02-tar-write.c.diff
Patch3:                  libarchive-03-size_max.diff

SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:      SUNWzlib
Requires:      SUNWbzip
Requires:      SFEsharutils
Requires:      SFElzma
Requires:      SFEe2fsprogs
BuildRequires: SFElzma-devel
BuildRequires: SFEe2fsprogs-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SFElzma-devel
Requires: SFEe2fsprogs-devel

%prep
%if %cc_is_gcc
%else
error "This spec file requires /usr/gnu/bin/g++. Please set your environment variables."
%endif

%setup -q -c -n %name-%version
cd libarchive-%version
%patch1 -p1
%patch2 -p1
%patch3 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp libarchive-%{version} libarchive-%{version}-64
%endif

%build
#
# Need to force some shell info to point to bash because the scripts
# are for bash.
#
export SHELL="/bin/bash"
export LFS_CFLAGS=`/usr/bin/getconf LFS_CFLAGS`

%ifarch amd64 sparcv9
cd libarchive-%{version}-64

export LDFLAGS="%_ldflags64"
export CFLAGS="%optflags64 -D_POSIX_PTHREAD_SEMANTICS"

./configure --prefix=%{_prefix}         \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes         \
            --disable-static

make VERBOSE=1
cd ..
%endif

cd libarchive-%{version}
export LDFLAGS="%_ldflags"
export CFLAGS="%optflags -D_POSIX_PTHREAD_SEMANTICS ${LFS_CFLAGS}"

./configure --prefix=%{_prefix}         \
            --mandir=%{_mandir}         \
            --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared=yes         \
            --disable-static

make VERBOSE=1
cd ..

%install
rm -rf $RPM_BUILD_ROOT

export SHELL="/bin/bash"

%ifarch amd64 sparcv9
cd libarchive-%{version}-64
make install DESTDIR=$RPM_BUILD_ROOT
rm -f ${RPM_BUILD_ROOT}%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd libarchive-%{version}
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
* Sat Sep 12 2009 - moinakg(at)belenix<dot>org
- Bump version, add new patch.
* Fri Jul 03 2009 - Moinak Ghosh <moinakg@belenix(dot)org>
- Initial version
