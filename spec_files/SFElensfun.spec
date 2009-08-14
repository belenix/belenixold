#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFElensfun
Summary:             A library to rectify the defects introduced by your photographic equipment
Version:             0.2.3
License:             LGPLv3
Source:              http://download.berlios.de/lensfun/lensfun-%{version}.tar.bz2
URL:                 http://lensfun.berlios.de/
Patch1:              lensfun-01-posix.mak.diff

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWglib2
Requires: SUNWpng
Requires: SUNWPython26
Requires: SUNWzlib
BuildRequires: SFEdoxygen
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWpng-devel
BuildRequires: SUNWPython26-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SUNWglib2-devel
Requires: SUNWpng-devel
Requires: SUNWPython26-devel

%prep
%setup -q -c -n %name-%version
cd lensfun-%version
%patch1 -p1
cd ..

%ifarch amd64 sparcv9
cp -rp lensfun-%version lensfun-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd lensfun-%{version}-64

export CFLAGS="-m64"
export CXXFLAGS="-m64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --cflags="$CFLAGS" \
            --cxxflags="${CXXFLAGS}" \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir}/lensfun \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --target=.x86_64.generic

# set GCC.LDFLAGS to avoid stripping and useless -debuginfo
gmake AUTODEP=0 -j$CPUS lensfun manual V=1 GCC.LDFLAGS.release=""

cd ..
%endif

cd lensfun-%{version}
export CFLAGS=""
export CXXFLAGS=""
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --cflags="$CFLAGS" \
            --cxxflags="${CXXFLAGS}" \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir}/lensfun \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --target=..generic

# set GCC.LDFLAGS to avoid stripping and useless -debuginfo
gmake AUTODEP=0 -j$CPUS lensfun manual V=1 GCC.LDFLAGS.release=""

cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd lensfun-%{version}-64

gmake AUTODEP=0 INSTALL_PREFIX=$RPM_BUILD_ROOT install
cd ..
%endif

cd lensfun-%{version}
gmake AUTODEP=0 INSTALL_PREFIX=$RPM_BUILD_ROOT install
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/lensfun
%{_datadir}/lensfun/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/lensfun-%{version}
%{_docdir}/lensfun-%{version}/README
%{_docdir}/lensfun-%{version}/*.txt

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/lensfun-%{version}
%{_docdir}/lensfun-%{version}/manual

%changelog
* Fri Aug 14 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
