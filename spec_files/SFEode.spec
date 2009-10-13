#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEode
Summary:             Open Dynamics engine
Version:             0.11.1
License:             BSD or LGPLv2+
Group:               System Environment/Libraries
Source:              %{sf_download}/opende/ode-%{version}.tar.gz
URL:                 http://www.ode.org

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWxorg-mesa
BuildRequires: SUNWxorg-headers

%description
ODE is an open source, high performance library for simulating
rigid body dynamics. It is fully featured, stable, mature and
platform independent with an easy to use C/C++ API. It has
advanced joint types and integrated collision detection with
friction. ODE is useful for simulating vehicles, objects in
virtual reality environments and virtual creatures. It is
currently used in many computer games, 3D authoring tools and
simulation tools.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWxorg-headers

%prep
%setup -q -c -n %name-%version
%ifarch amd64 sparcv9
cp -rp ode-%version ode-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd ode-%{version}-64

export CFLAGS="%optflags64 -ffast-math"
export CXXFLAGS="%cxx_optflags64 -ffast-math"
export LDFLAGS="%_ldflags64 %{xorg_lib_path64} -lX11 %{gnu_lib_path64}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --with-x \
            --with-drawstuff=X11 \
            --enable-shared \
            --disable-static

gmake -j$CPUS

cd ..
%endif

cd ode-%{version}
export CFLAGS="%optflags -ffast-math"
export CXXFLAGS="%cxx_optflags -ffast-math"
export LDFLAGS="%_ldflags %{xorg_lib_path} -lX11 %{gnu_lib_path}"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
            --with-x \
            --with-drawstuff=X11 \
            --enable-shared \
            --disable-static

gmake -j$CPUS
cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd ode-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd ode-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
cd ..

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
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/ode-config
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/ode-config
%endif

%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, bin) %{_includedir}/ode
%{_includedir}/ode/*
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
