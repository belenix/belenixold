#
# spec file for package clutter
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# bugdb: http://bugzilla.openedhand.com
#
# Owner: bewitche
#

Name:         clutter
License:      LGPL
Group:        System/Libraries
Version:      0.8.8
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      clutter - a library for creating fast, visually rich and animated graphical user interfaces.
Source:	  http://www.clutter-project.org/sources/clutter/0.8/clutter-%{version}.tar.bz2
#owner:beiwtche date:2008-11-26 type:feature
Patch1:       clutter-01-remove-tests.diff
#owner:bewitche date:2009-04-14 type:feature
Patch2:       clutter-02-g11n-i18n-ui.diff

URL:          http://www.clutter-project.org/
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%description

%prep
%setup -q -n clutter-%version
%patch1 -p1
%patch2 -p1
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%{optflags} -I/usr/X11/include"
export CXXFLAGS="%{?cxx_optflags}"
export LDFLAGS="%{?_ldflags} -L/usr/X11/lib -R/usr/X11/lib -lX11"
./configure --prefix=%{_prefix}              \
            --libdir=%{_libdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --disable-static                 \
            --enable-gtk-doc			
make -j$CPUS 

%install
#rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT



%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*


%changelog
* Tue Apr 14 2009 - chris.wang@sun.com
- backup to 0.8.8 as 0.9 version is not competible with clutter-gtk
* Tue Apr 07 2009 - chris.wang@sun.com
- Bump to 0.9.2, revised patch 01 and removed upstreamed patch 02
* Mon Feb 23 2009 - chris.wang@sun.com
- Bump to 0.8.8 version
* Tue Jan 06 2009 - takao.fujiwara@sun.com
- Add patch g11n-i18n-ui.diff for I18n UI.
* Wed Nov 26 2008  chris.wang@sun.com
- add patch cairo-01-remove-tests.diff, we don't ship tests to our package
* Tue Jul 1  2008  chris.wang@sun.com 
- Initial build.



