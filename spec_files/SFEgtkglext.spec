#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%endif

%include base.inc

Name:                SFEgtkglext
Summary:             OpenGL Extension to GTK+
Version:             1.2.0
License:             LGPLv2+ or GPLv2+
Group:		     System Environment/Libraries
Source:              %{sf_download}/gtkglext/gtkglext-%{version}.tar.bz2
URL:                 http://gtkglext.sourceforge.net/

SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:      %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SUNWgtk2
Requires: SUNWxorg-mesa
Requires: FSWxorg-clientlibs
Requires: SUNWxorg-clientlibs
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWxorg-mesa
BuildRequires: FSWxorg-headers
BuildRequires: SUNWxorg-headers

%description
GtkGLExt is an OpenGL extension to GTK. It provides the GDK objects
which support OpenGL rendering in GTK, and GtkWidget API add-ons to
make GTK+ widgets OpenGL-capable.

%package devel
Summary:                 Development tools for GTK-based OpenGL applications
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name
Requires: SUNWgtk2-devel
Requires: SUNWxorg-mesa
Requires: FSWxorg-headers
Requires: SUNWxorg-headers

%prep
%setup -q -c -n %name-%version
cd gtkglext-%version
cd ..

%ifarch amd64 sparcv9
cp -rp gtkglext-%version gtkglext-%{version}-64
%endif


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

%ifarch amd64 sparcv9
cd gtkglext-%{version}-64

export CFLAGS="%optflags64"
export LDFLAGS="%_ldflags64"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir}/%{_arch64} \
            --libdir=%{_libdir}/%{_arch64} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
	    --enable-shared \
	    --disable-static

gmake -j$CPUS

cd ..
%endif

cd gtkglext-%{version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix} \
            --bindir=%{_bindir} \
            --libdir=%{_libdir} \
            --sysconfdir=%{_sysconfdir} \
            --includedir=%{_includedir} \
            --libexecdir=%{_libexecdir} \
	    --enable-shared \
	    --disable-static

gmake -j$CPUS

cd ..


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
cd gtkglext-%{version}-64

gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/*.la
cd ..
%endif

cd gtkglext-%{version}
gmake DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

mkdir -p $RPM_BUILD_ROOT%{_docdir}/gtkglext-%{version}
cp AUTHORS NEWS README COPYING* $RPM_BUILD_ROOT%{_docdir}/gtkglext-%{version}
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
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/gtkglext-1.0
%dir %attr (0755, root, bin) %{_libdir}/gtkglext-1.0/include
%{_libdir}/gtkglext-1.0/include/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%dir %attr(0755, root, bin) %{_datadir}/gtk-doc
%{_datadir}/gtk-doc/*

%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/gtkglext-1.0
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}/gtkglext-1.0/include
%{_libdir}/%{_arch64}/gtkglext-1.0/include/*
%endif

%defattr (-, root, other)
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/gtkglext-%{version}
%{_docdir}/gtkglext-%{version}/*

%changelog
* Fri Nov 06 2009 - Moinak Ghosh <moinakg<at>belenix(dot)org>
- Initial version.
