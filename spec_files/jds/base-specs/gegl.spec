#
# spec file for package gegl
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#
Name:         gegl
License:      LGPL
Group:        Applications/Multimedia
Version:      0.0.22
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GEGL (Generic Graphics Library) is a graph based image processing framework.
Source:	      ftp://ftp.gimp.org/pub/gegl/0.0/%{name}-%{version}.tar.bz2
URL:          http://www.gegl.org/
Patch1:	      gegl-01-build.diff
Patch2:       gegl-02-make.diff
#date:2009-01-06 owner:fujiwara type:feature bugster:6790365 bugzilla:566743
Patch3:       gegl-03-g11n-textdomain.diff
#date:2009-01-16 owner:bewitche type:bug bugster:6793543 bugzilla:568389
Patch4:       gegl-04-fprintf-null.diff
#date:2009-02-24 owner:bewitche type:bug bugster:6802192 bugzilla:573073
Patch5:       gegl-05-info-null.diff
%package devel
Summary:      %{summary} - development files
Group:        System/GUI/GNOME
Requires:     %name 

%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1

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
export CFLAGS="%{optflags} -features=extensions"
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

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/lib*.so*
%{_libdir}/pkgconfig/*
%{_libdir}/gimp
%{_datadir}/pixmaps/*
%{_datadir}/applications/*

%files devel
%defattr (-, root, root)
%{_includedir}/*
%{_datadir}/gtk-doc

%changelog
* The Feb 26 2009- chris.wang@sun.com
- Add patch gegl-05-info-null to fix bug 6802192
* Tue Jan 20 2009 - chris.wang@sun.com
- bump to 0.22, add patch fprintf_null
* Tue Jan 06 2009 - takao.fujiwara@sun.com
- Add patch g11n-textdomain.diff
* Wed Nov 26 2008 - chris.wang@sun.com
- Initial create.
