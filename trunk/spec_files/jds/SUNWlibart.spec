#
# spec file for package SUNWlibart
#
# includes module(s): libart_lgpl
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include Solaris.inc
%include base.inc

%use libart_lgpl = libart_lgpl.spec

Name:                    SUNWlibart
Summary:                 GNOME library for high-performace 2D graphics
Version:                 %{libart_lgpl.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWlibmsr
BuildRequires: SUNWlibm

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWlibart

%prep
rm -rf %name-%version
mkdir %name-%version

mkdir %name-%version/%{base_arch}
%libart_lgpl.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%libart_lgpl.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%libart_lgpl.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d  %{base_arch} libart_lgpl-%{libart_lgpl.version}/README
%doc -d %{base_arch} libart_lgpl-%{libart_lgpl.version}/AUTHORS
%doc(bzip2) -d %{base_arch} libart_lgpl-%{libart_lgpl.version}/ChangeLog
%doc(bzip2) -d %{base_arch} libart_lgpl-%{libart_lgpl.version}/COPYING
%doc(bzip2) -d %{base_arch} libart_lgpl-%{libart_lgpl.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/libart2-config
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/libart2-config.1

%changelog
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)
