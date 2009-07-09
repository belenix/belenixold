#
# spec file for package babl
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#
Name:         babl
License:      LGPL
Group:        Applications/Multimedia
Version:      0.0.22
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Babl is a dynamic, any to any, pixel format conversion library.
Source:	      ftp://ftp.gtk.org/pub/babl/0.0/%{name}-%{version}.tar.bz2
URL:          http://www.gegl.org/babl/

Patch1:       babl-01-solaris-build.diff
Patch2:       babl-02-inline-funcs.diff
%package devel
Summary:      %{summary} - development files
Group:        System/GUI/GNOME
Requires:     %name 

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
export CFLAGS="%{optflags}"
export CXXFLAGS="%{?cxx_optflags}"
export LDFLAGS="%{?_ldflags}"
aclocal
libtoolize --force
glib-gettextize --force
automake -a -c -f
autoconf
./configure --prefix=%{_prefix}			\
	    --libdir=%{_libdir}         \
            --sysconfdir=%{_sysconfdir}         \
	    --mandir=%{_mandir}                 \
	    --datadir=%{_datadir}               \
            --infodir=%{_datadir}/info
	    		
make -j$CPUS

%install
#rm -rf $RPM_BUILD_ROOT
#rm -rf $RPM_BUILD_ROOT%{_libdir}/*.la
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_libdir}/lib*.so*
%{_libdir}/babl-0.0/*.so*
%{_libdir}/pkgconfig/*

%files devel
%defattr (-, root, root)
%{_includedir}/babl-0.0/babl/*

%changelog
* Wed Nov 26 2008 - chris.wang@sun.com
- Initial create.
