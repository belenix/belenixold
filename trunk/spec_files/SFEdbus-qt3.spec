#
# spec file for package SUNWdbus-bindings
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

#%ifarch amd64 sparcv9
#%include arch64.inc
#%use libdbus_qt_64   = libdbus-1-qt3.spec
#%define _libdir %{_basedir}/lib
#%endif

%include base.inc
%use libdbus_qt   = libdbus-1-qt3.spec
%use dbus_qt   = dbus-qt3.spec

Name:                    SFEdbus-qt3
Summary:                 Qt3 binding for DBUS
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	SUNWdbus
Requires:	SUNWgnome-base-libs
Requires:	SUNWlxml
Requires:       SUNWlexpt
Requires:       SFEqt3
BuildRequires:	SUNWdbus-devel
BuildRequires:	SUNWgnome-base-libs-devel
BuildRequires:	SUNWlxml
BuildRequires:  SUNWsfwhea
BuildRequires:  SFEqt3-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:       SUNWgnome-base-libs
Requires:       SFEqt3-devel

%prep
rm -rf %name-%version
mkdir %name-%version

#%ifarch amd64 sparcv9
#mkdir %name-%version/%_arch64
#%libdbus_qt_64.prep -d %name-%version/%_arch64
#%endif

mkdir %name-%version/%{base_arch}
%libdbus_qt.prep -d %name-%version/%{base_arch}
%dbus_qt.prep -d %name-%version/%{base_arch}

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED
%if %cc_is_gcc
export EXTRA_CFLAGS="-I/usr/sfw/include"
export EXTRA_CXXFLAGS="-I/usr/sfw/include"
%else
export EXTRA_CFLAGS="-xc99 -D_REENTRANT -I/usr/sfw/include -D__EXTENSIONS__"
export EXTRA_CXXFLAGS="-xc99 -D_REENTRANT -I/usr/sfw/include -D__EXTENSIONS__"
%endif
# Put /usr/ccs/lib first in the PATH so that cpp is picked up from there
# note: I didn't put /usr/lib in the PATH because there's too much other
# stuff in there
#
export PATH=/usr/ccs/lib:$PATH

#%ifarch amd64 sparcv9
#export CFLAGS="%optflags64 $EXTRA_CFLAGS"
#export CXXFLAGS="%optflags64 $EXTRA_CXXFLAGS"
#export LDFLAGS="%_ldflags64 -L/usr/sfw/lib/%{_arch64} -R/usr/sfw/lib/%{_arch64} -lexpat"
#export PKG_CONFIG_PATH=../libdbus-1-qt3-%{libdbus_qt.version}:/usr/lib/%{_arch64}/pkgconfig
#%libdbus_qt_64.build -d %name-%version/%_arch64
#%endif

export CFLAGS="%optflags $EXTRA_CFLAGS"
export CXXFLAGS="%optflags $EXTRA_CXXFLAGS"
export PKG_CONFIG_PATH=../libdbus-1-qt3-%{libdbus_qt.version}
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lexpat"
export PYTHON=%{_bindir}/python
%libdbus_qt.build -d %name-%version/%{base_arch}
%dbus_qt.build -d %name-%version/%{base_arch}

%install
rm -rf $RPM_BUILD_ROOT
#%ifarch amd64 sparcv9
#%libdbus_qt_64.install -d %name-%version/%_arch64
#%endif

%libdbus_qt.install -d %name-%version/%{base_arch}
%dbus_qt.install -d %name-%version/%{base_arch}

%clean
rm -rf $RPM_BUILD_ROOT

%if %(test -f /usr/sadm/install/scripts/i.manifest && echo 0 || echo 1)
%iclass manifest -f i.manifest
%endif

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/dbus-1
#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%{_libdir}/%{_arch64}/lib*.so*
#%endif

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
#%ifarch amd64 sparcv9
#%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
#%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
#%{_libdir}/%{_arch64}/pkgconfig/*.pc
#%endif

%changelog
* Sun Mar 23 2008 - moinakg@gmail.com
- Initial spec. Needed by Compiz.
