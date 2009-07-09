#
# spec file for package SUNWlibglade
#
# includes module(s): libglade
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
%use libglade_64 = libglade.spec
%endif

%include base.inc

%use libglade = libglade.spec

Name:                    SUNWlibglade
Summary:                 GNOME library for loading GLADE interfaces at runtime
Version:                 %{libglade.version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgtk2
Requires: SUNWlxmlr
Requires: SUNWlxml
BuildRequires: SUNWgtk2-devel
BuildRequires: SUNWlxml-devel

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWlibglade
Requires: SUNWPython

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64

%libglade_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%{base_arch}
%libglade.prep -d %name-%version/%{base_arch}

cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED

%ifarch amd64 sparcv9
%libglade_64.build -d %name-%version/%_arch64
%endif

%libglade.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%libglade_64.install -d %name-%version/%_arch64
%endif

%libglade.install -d %name-%version/%{base_arch}

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%ifarch amd64 sparcv9
rm $RPM_BUILD_ROOT%{_bindir}/%{_arch64}/libglade-convert
rmdir $RPM_BUILD_ROOT%{_bindir}/%{_arch64}
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc -d  %{base_arch} libglade-%{libglade.version}/README
%doc -d  %{base_arch} libglade-%{libglade.version}/AUTHORS
%doc(bzip2) -d  %{base_arch} libglade-%{libglade.version}/ChangeLog
%doc(bzip2) -d  %{base_arch} libglade-%{libglade.version}/COPYING
%doc(bzip2) -d  %{base_arch} libglade-%{libglade.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/lib*.so*
%endif
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/xml

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_bindir}
%{_bindir}/libglade-convert
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

%changelog
* Tue Mar 31 2009 - dave.lin@sun.com
- initial version(split from SUNWgnome-base-libs)
