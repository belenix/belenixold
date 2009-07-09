#
# spec file for package SUNWlibsdl
#
# includes module(s): libsdl
#
# Copyright 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: davelam
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use sdl_64 = libsdl.spec
%endif


%include base.inc
%use sdl = libsdl.spec

Name:        SUNWlibsdl
Summary:     %{sdl.summary}
Version:     %{sdl.version}
SUNW_BaseDir:%{_basedir}
SUNW_Copyright:%{name}.copyright
BuildRoot:   %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-audio-devel
Requires: SUNWgnome-audio

%package devel
Summary:      %{summary} - development files
SUNW_BaseDir: %{_basedir}
%include default-depend.inc

%prep
%ifnarch sparc
# Testing that the OpenGL headers and libs are installed.
# If this fails it means that the build machine is not properly configured
test -f /usr/X11/include/GL/glx.h || {
  echo "Missing OpenGL headers. Stopping."
  echo "As root, run: \"/lib/svc/method/ogl-select start\""
  false
  }
test -f /usr/X11/lib/modules/extensions/libglx.so  || {
  echo "Missing OpenGL libraries. Stopping."
  echo "As root, run: \"/lib/svc/method/ogl-select start\""
  false
  }
%endif

rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%sdl_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%sdl.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%sdl_64.build -d %name-%version/%_arch64
%endif

%sdl.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%sdl_64.install -d %name-%version/%_arch64
%endif

%sdl.install -d %name-%version/%base_arch

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%doc -d %{base_arch}/SDL-%{sdl.version} README CREDITS
%doc(bzip2) -d %{base_arch}/SDL-%{sdl.version} COPYING WhatsNew
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libSDL*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
 
%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/sdl-config
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/*
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif

%changelog
* Mon Feb 23 2009 - elaine.xiong@sun.com
- Remove SSE2 support to fix CR6808201.
* Thu Sep 19 2008 - dave.lin@sun.com
- Update the license file and add %doc lines to include licensing/copyright files
* Wed Apr  4 2007 - laca@sun.com
- Create
