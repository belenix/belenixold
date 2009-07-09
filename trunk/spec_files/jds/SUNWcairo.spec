#
# spec file for package SUNWcairo
#
# includes module(s): cairo
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use cairo_64 = cairo.spec
%endif

%include base.inc

%use cairo = cairo.spec

Name:                    SUNWcairo
Summary:                 Vector graphics library
Version:                 %{cairo.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWglib2
Requires: SUNWpixman
Requires: SUNWfreetype2
Requires: SUNWfontconfig
Requires: SUNWpng
Requires: SUNWzlib
Requires: SUNWxwrtl
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWpng-devel

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWcairo

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%cairo_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%cairo.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%ifarch amd64 sparcv9
cd %{_builddir}/%name-%version/%{_arch64}/cairo-%{cairo.version}
cat > freetype-config <<EOF
#!/bin/sh
PKG_CONFIG_PATH=/usr/lib/%{_arch64}/pkgconfig
export PKG_CONFIG_PATH
OPT="\$1"
if [ "x\$OPT" = x--version ]; then
  OPT=--modversion
fi
exec /usr/bin/pkg-config \$OPT freetype2
EOF
chmod a+x freetype-config
%endif

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
%cairo_64.build -d %name-%version/%_arch64
%endif

%cairo.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%cairo_64.install -d %name-%version/%_arch64
%endif

%cairo.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc -d %{base_arch} cairo-%{cairo.version}/README
%doc -d %{base_arch} cairo-%{cairo.version}/AUTHORS
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.0
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.2
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.4
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/ChangeLog.pre-1.6
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/COPYING
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/COPYING-LGPL-2.1
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/COPYING-MPL-1.1
%doc(bzip2) -d %{base_arch} cairo-%{cairo.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %dir %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/gtk-doc

%changelog
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)
