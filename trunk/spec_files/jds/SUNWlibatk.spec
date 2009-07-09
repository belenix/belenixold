#
# spec file for package SUNWlibatk
#
# includes module(s): atk
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: liyuan
#
%include Solaris.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use atk_64 = atk.spec
%endif

%include base.inc

%use atk = atk.spec

Name:                    SUNWlibatk
Summary:                 GNOME accesibility toolkit libraries
Version:                 %{atk.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWglib2
BuildRequires: SUNWglib2-devel

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWlibatk

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n content
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%atk_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%atk.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
%atk_64.build -d %name-%version/%_arch64
%endif

%atk.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%atk_64.install -d %name-%version/%_arch64
%endif

%atk.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

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
%dir %attr (0755, root, sys) %{_datadir}

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
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %dir %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)
