#
# spec file for package evolution-webcal
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jedy
#
Name:         evolution-webcal
License:      GPL
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Webcal support for Evolution
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/evolution-webcal
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Prereq:       GConf

%define libgnomeui_version 2.4
%define libsoup_version 2.1.9
%define evolution_data_server_version 1.2.0

Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       evolution-data-server >= %{evolution_data_server_version}
Requires:       libsoup >= %{libsoup_version}

BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  libsoup-devel >= %{libsoup_version}
BuildRequires:  evolution-data-server-devel >= %{evolution_data_server_version}

%description
evolution-webcal provides support for adding online calendars to Evolution.

%prep
%setup -q

%build
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
./configure  --prefix=%{_prefix}		\
	     --libexecdir=%{_libexecdir}	\
	     --sysconfdir=%{_sysconfdir}

make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="evolution-webcal.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun

%files
%defattr (-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_libexecdir}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%config %{_sysconfdir}/gconf/schemas/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Mon Mar 06 2009 - jedy.wang@sun.com
- Bump to 2.25.91.
 
* Mon Feb 16 2009 - jedy.wang@sun.com
- Bump to 2.25.90.

* Wed Dec 03 2008 - jedy.wang@sun.com
- Bump to 2.24.0.

* Tue Sep 02 2008 - jedy.wang@sun.com
- Bump to 2.23.91.

* Mon Feb 25 2008 - damien.carbery@sun.com
- Bump to 2.21.92.

* Thu Jan 31 2008 - damien.carbery@sun.com
- Bump to 2.13.90.

* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.12.0.

* Wed Aug 29 2007 - damien.carbery@sun.com
- Add intltoolize call to update intltool scripts.

* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 2.11.91.

* Wed Mar 14 2007 - damien.carbery@sun.com
- Bump to 2.10.0.

* Tue Mar 06 2007 - damien.carbery@sun.com
- Bump to 2.9.92.

* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.9.91.

* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.9.5.

* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.8.0.

* Sun Jul 23 2006 - jeff.cai@sun.com
- Bump to 2.7.1.

* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.5.90.

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.3.91

* Mon Apr 26 2004 - glynn.foster@sun.com
- Initial spec file for evolution-webcal 1.0.3
