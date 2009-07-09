#
# spec file for package SUNWpango
#
# includes module(s): pango
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
%define _sysconfdir /etc/%{_arch64}
%use pango_64 = pango.spec
%endif

%include base.inc

%use pango = pango.spec

Name:                    SUNWpango
Summary:                 GNOME core text and font handling libraries
Version:                 %{pango.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWpango-root
Requires: SUNWglib2
Requires: SUNWcairo
Requires: SUNWfreetype2
Requires: SUNWfontconfig
Requires: SUNWlibmsr
Requires: SUNWxwplt
Requires: SUNWxwrtl
Requires: SUNWxwxft
BuildRequires: SUNWglib2-devel
BuildRequires: SUNWcairo-devel
BuildRequires: SUNWxorg-headers
BuildRequires: SUNWlibm

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWpango

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%pango_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%pango.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
%pango_64.build -d %name-%version/%_arch64
%endif

%pango.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%pango_64.install -d %name-%version/%_arch64
%endif

%pango.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# on linux, these config files are created in %post
# that would be more complicated on Solaris, especially
# during jumpstart or live upgrade, so it's better to do
# it during the build
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}
$RPM_BUILD_ROOT%{_bindir}/pango-querymodules \
    $RPM_BUILD_ROOT%{_libdir}/pango/*/modules/*.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/pango/pango.modules

%ifarch amd64 sparcv9
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir}/%{_arch64}

$RPM_BUILD_ROOT%{_bindir}/%{_arch64}/pango-querymodules \
    $RPM_BUILD_ROOT%{_libdir}/%{_arch64}/pango/*/modules/*.so \
    | sed -e "s%%$RPM_BUILD_ROOT%%%%" \
    > $RPM_BUILD_ROOT%{_sysconfdir}/%{_arch64}/pango/pango.modules

rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/pango-view
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d  %{base_arch} pango-%{pango.version}/README
%doc -d  %{base_arch} pango-%{pango.version}/AUTHORS
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-0
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-2
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-4
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-6
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-8
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-10
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-12
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-14
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-16
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-18
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/ChangeLog.pre-1-20
%doc(bzip2) -d  %{base_arch} pango-%{pango.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/pango-querymodules
%{_bindir}/pango-view
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/pango/*/*/*.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_bindir}/%{_arch64}
%{_bindir}/%{_arch64}/pango-querymodules
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%{_libdir}/%{_arch64}/pango/*/*/*.so
%endif
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/pango-querymodules.1

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

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%config %{_sysconfdir}/pango
%ifarch amd64 sparcv9
%config %{_sysconfdir}/%{_arch64}/pango
%endif

%changelog
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)
