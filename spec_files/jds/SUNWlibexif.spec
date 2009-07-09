#
# spec file for package SUNWlibexif
#
# includes module(s): libexif
#
# Copyright (c) 2004 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: laca
#
%include Solaris.inc

%use libexif = libexif.spec

Name:                    SUNWlibexif
Summary:                 EXIF tag parsing library for digital cameras
Version:                 11.%{libexif.version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
BuildRequires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-common-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc

%prep
rm -rf %name-%version
mkdir %name-%version
%libexif.prep -d %name-%version

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%libexif.build -d %name-%version

%install
%libexif.install -d %name-%version

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.la
rm -rf $RPM_BUILD_ROOT%{_datadir}

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Dec 11 2006 - laca@sun.com
- delete some unnecessary env variables
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 11 2006 - damien.carbery@sun.com
- Change build dependency on SUNWgnome-base-libs-share. That pkg is obsolete
  with files now in the base package.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Jan 04 2006 - damien.carbery@sun.com
- Add BuildRequires to avoid build failure.
* Tue Oct 04 2005 - damien.carbery@sun.com
- Add better summary (libexif -> EXIF tag parsing lib for digital cameras).
* Fri Sep 09 2005 - <laca@sun.com>
- remove unpackaged files
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Jul 05 2004 - damien.carbery@sun.com
- Add BuildRequires: SUNWgnome-base-libs-share
* Sat Jun 26 2004 - shirley.woo@sun.com
- Changed install location to /usr/...
* Fri Mar 31 2004 - brian.cameron@sun.com
- Created,
