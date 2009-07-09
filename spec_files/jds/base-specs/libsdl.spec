#
# spec file for package libsdl
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
# bugdb: bugzilla.libsdl.org
#
Name:         libsdl
License:      LGPL
Group:        System/Libraries
Version:      1.2.13
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      libsdl - Simple DirectMedia Layer
Source:       http://www.libsdl.org/release/SDL-%{version}.tar.gz
# owner:dcarbery date:2008-01-17 type:bug bugzilla:542 state:upstream
Patch1:	      sdl-01-fixPATH.diff
URL:          http://www.libsdl.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%description
Simple DirectMedia Layer is a cross-platform multimedia library designed to
provide low level access to audio, keyboard, mouse, joystick, 3D hardware via
OpenGL, and 2D video framebuffer. It is used by MPEG playback software,
emulators, and many popular games.

%package devel
Summary: Headers for developing programs that will use libsdl
Group:      Development/Libraries
Requires:   %{name}

%description   devel
This package contains the headers that programmers will need to develop
applications which will use libsdl.

%prep
%setup -q -n SDL-%{version}
%patch1 -p1

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

export CFLAGS="%optflags -I/usr/X11/include"
export LDFLAGS="%_ldflags"
./configure \
	--prefix=%{_prefix} \
        --libdir=%{_libdir} \
        --bindir=%{_bindir} \
	--sysconfdir=%{_sysconfdir} \
        --with-esd-prefix=%{_prefix} \
	--mandir=%{_mandir}
make -j $CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT

# delete libtool .la files and static libs
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*la

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr (-, root, root)
%{_libdir}/*.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/*.so

%changelog
* Fri Mar 14 2008 - damien.carbery@sun.com
- Add -I/usr/X11/include to CFLAGS after update of SUNWwinc.
* Thu Jan 17 2008 - patrick.ale@gmail.com
- Add patch to restore path after sdl-config check
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 1.2.13.
* Fri Oct 12 2007 - dave.lin@sun.com
- Bump to 1.2.12 to fix bug CR6598379
* Wed Apr  4 2007 - laca@sun.com
- Create
