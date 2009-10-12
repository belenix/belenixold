#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEsimage
Summary:             A library with image format loaders and front-ends to common import libraries.
Version:             1.6.1
License:             GPL
Source:              http://ftp.coin3d.org/coin/src/all/simage-%{version}.tar.gz
URL:                 http://www.coin3d.org

SUNW_BaseDir:        %{_basedir}
#SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWpng
Requires: SUNWjpg
Requires: SUNWTiff
Requires: SUNWogg-vorbis
Requires: SFElibsndfile
Requires: SUNWzlib
Requires: SFEqt3
BuildRequires: SUNWpng-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWTiff-devel
BuildRequires: SUNWogg-vorbis-devel
BuildRequires: SFElibsndfile-devel
BuildRequires: SFEqt3-devel
BuildRequires: SFEdoxygen
BuildRequires: SUNWxorg-headers

%description
This is ``simage'', a library with image format loaders and front-ends
to common import libraries. simage is meant for use with applications
which reads image files as textures.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SFEdoxygen
Requires: SUNWpng-devel
Requires: SUNWjpg-devel
Requires: SUNWxorg-headers
Requires: SUNWzlib
Requires: SUNWTiff-devel
Requires: SUNWogg-vorbis-devel
Requires: SFElibsndfile-devel
Requires: SFEqt3-devel

%prep
%setup -q -c -n %name-%version
cd simage-%version
cd ..

%ifarch amd64 sparcv9
cp -rp simage-%version simage-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd simage-%{version}-64
export CPPFLAGS="-I%{_includedir}/qt3"
export CFLAGS="%optflags64 -I%{_includedir}/qt3"
export CXXFLAGS="%cxx_optflags64 -I%{_includedir}/qt3"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"
export QTDIR=%{_prefix}

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --with-qt=true \
            --enable-qimage \
            --enable-threadsafe \
            --enable-html 

gmake -j$CPUS

cd ..
%endif

cd simage-%{version}
export CPPFLAGS="-I%{_includedir}/qt3"
export CFLAGS="%optflags -I%{_includedir}/qt3"
export CXXFLAGS="%cxx_optflags -I%{_includedir}/qt3"
export LDFLAGS="%_ldflags %{gnu_lib_path}"
export QTDIR=%{_prefix}

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --with-qt=true \
            --enable-qimage \
            --enable-threadsafe \
            --enable-html

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd simage-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd simage-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/Coin
%{_datadir}/Coin/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*.h
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*

%changelog
* Sun Oct 04 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
