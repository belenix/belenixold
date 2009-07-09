#
# spec file for package drivel
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner:ydzhang
#

Name:           drivel
License:        GPL v2
Group:          Development/Utilities
Version:        2.0.3
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://dropline.net/past-projects/drivel-blog-editor/
Summary:        Drivel is a GNOME client for editing blog
Source:         http://prdownloads.sourceforge.net/%{name}/%{name}-%{version}.tar.bz2
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: gtk2-devel

%description
Drivel - Blog Editor

%prep
%setup -q

%build
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir} CFLAGS="-D__NetBSD__ -D__EXTENSIONS__"

make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog NEWS README COPYING.LIB
%{_bindir}/*
%{_libdir}/lib*.so.*
%{_libdir}/bonobo/servers/GNOME_RemoteDesktop.server

%changelog
* Wed Feb 11 2009 - david.zhang@sun.com
- Initial version
