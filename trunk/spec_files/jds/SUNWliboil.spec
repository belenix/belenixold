#
# spec file for package SUNWliboil
#
# includes module(s): liboil
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

%use liboil = liboil.spec

Name:                    SUNWliboil
Summary:                 GNOME structured file library
Version:                 %{liboil.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
BuildRequires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
%ifarch amd64 i386
BuildRequires: SUNWgcc
Requires: SUNWgccruntime
%endif

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%liboil.prep -d %name-%version

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

# Note, on x86 build with gcc since liboil contains GCC-style assembly
# code which won't compile with Sun Studio.  For better performance,
# we use GCC here.
#
%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
%ifarch i386
export CC=gcc
export CFLAGS="-O2 -march=i586 -Xlinker -i -fno-omit-frame-pointer -fPIC -DPIC"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%liboil.build -d %name-%version

%install
%liboil.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d liboil-%{liboil.version} AUTHORS README
%doc(bzip2) -d liboil-%{liboil.version} COPYING NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man1/*
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%dir %attr (0755, root, sys) %{_datadir}
%{_includedir}/*
%{_datadir}/gtk-doc/html/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Sep 15 2008 - christian.kelly@sun.com
- Remove /usr/share/doc from %files.
* Thu Mar 27 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Mon Mar 19 2007 - dougs@truemail.co.th
- Fixed -fno-omit-frame-pointer flag
* Thu Mar 15 2007 - damien.carbery@sun.com
- Add Requires SUNWgccruntime after check-deps.pl run.
* Mon Feb 12 2007 - brian.cameron@sun.com
- Fix building with gcc based on Laca's comments.
* Wed Jan 31 2007 - brian.cameron@sun.com
- Build with gcc so that on x86 we compile hardware acceleration GCC asm code.
* Wed Jun 14 2007 - brian.cameron@sun.com
- Add new bindir files included in 0.3.9.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 11 2006 - damien.carbery@sun.com
- Change build dependency on SUNWgnome-base-libs-share. That pkg is obsolete
  with files now in the base package.
* Thu Mar 23 2006 - shirley.woo@sun.com
- Updated Package Summary
* Fri Mar 17 2006 - shirley.woo@sun.com
- Updated Package Summary
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Oct 26 2005 - brian.cameron@sun.com
- Created.
