#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEgts
Summary:             GNU Triangulated Surface Library
Version:             0.7.6
License:             LGPLv2+
Group:               Applications/Engineering
Source:              %{sf_download}/gts/gts-%{version}.tar.gz
URL:                 http://gts.sourceforge.net/index.html

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWglib2
Requires: SFEnetpbm
BuildRequires: SUNWglib2-devel
BuildRequires: SFEnetpbm-devel

%description
GTS provides a set of useful functions to deal with 3D surfaces meshed
with interconnected triangles including collision detection,
multiresolution models, constrained Delaunay triangulations and robust
set operations (union, intersection, differences).

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWglib2-devel
Requires: SFEnetpbm-devel

%prep
%setup -q -c -n %name-%version
cd gts-%version
# Fix broken permissions
chmod +x test/*/*.sh
cd ..

%ifarch amd64 sparcv9
cp -rp gts-%version gts-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd gts-%{version}-64

export CFLAGS="%optflags64"
export CXXFLAGS="%cxx_optflags64"
export LDFLAGS="%_ldflags64 %{gnu_lib_path64}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --disable-static \
            --disable-dependency-tracking \
            LIBS=-lm

gmake -j$CPUS

cd ..
%endif

cd gts-%{version}
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags %{gnu_lib_path}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --disable-static \
            --disable-dependency-tracking \
            LIBS=-lm

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd gts-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
mv -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/delaunay $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtsdelaunay 
#mv -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/happrox $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtshapprox
mv -f $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/transform $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/gtstransform
cd ..
%endif

cd gts-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
mv -f $RPM_BUILD_ROOT%{_bindir}/delaunay $RPM_BUILD_ROOT%{_bindir}/gtsdelaunay 
mv -f $RPM_BUILD_ROOT%{_bindir}/happrox $RPM_BUILD_ROOT%{_bindir}/gtshapprox
mv -f $RPM_BUILD_ROOT%{_bindir}/transform $RPM_BUILD_ROOT%{_bindir}/gtstransform
cd ..

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/stl2gts
%{_bindir}/gts2stl
%{_bindir}/gts2oogl
%{_bindir}/gtscompare
%{_bindir}/gtstemplate
%{_bindir}/gts2dxf
%{_bindir}/gtscheck
%{_bindir}/gtstransform
%{_bindir}/gtsdelaunay
%{_bindir}/gtshapprox
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/stl2gts
%{_bindir}/%{_arch64}/gts2stl
%{_bindir}/%{_arch64}/gts2oogl
%{_bindir}/%{_arch64}/gtscompare
%{_bindir}/%{_arch64}/gtstemplate
%{_bindir}/%{_arch64}/gts2dxf
%{_bindir}/%{_arch64}/gtscheck
%{_bindir}/%{_arch64}/gtstransform
%{_bindir}/%{_arch64}/gtsdelaunay
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gts-config
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/gts-config
%endif

%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%changelog
* Sat Oct 10 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
