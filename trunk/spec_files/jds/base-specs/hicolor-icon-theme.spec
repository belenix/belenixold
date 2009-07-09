#
# spec file for package hicolor-icon-theme
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: calumb
#
Name:         		hicolor-icon-theme
License:      		GPL
Group:        		System/GUI/GNOME
BuildArchitectures:	noarch
Version:      		0.10
Release:      		40
Distribution: 		Java Desktop System
Vendor:       		Sun Microsystems, Inc.
Summary:      		GNOME Hi Color Icon Theme
Source:       		http://icon-theme.freedesktop.org/releases/%{name}-%{version}.tar.gz
URL:          		http://icon-theme.freedesktop.org/wiki/HicolorTheme
BuildRoot:    		%{_tmppath}/%{name}-%{version}-build
Docdir:	      		%{_defaultdocdir}/doc
Autoreqprov:  		on

%description
Hi Color Icon Theme for the GNOME Desktop

%prep
%setup -q


%build
aclocal $ACLOCAL_FLAGS
autoconf
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
    --prefix=%{_prefix} \
    --sysconfdir=%{_sysconfdir}

%install
make -i install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_datadir}/icons/hicolor

%changelog
* Wed Oct 31 2007 - damien.carbery@sun.com
- Bump to 0.10.
* Mon Jan 16 2006 - damien.carbery@sun.com
- Correct URL source (s/bz2/gz/).
* Fri Dec 02 2005 - damien.carbery@sun.com
- Add URL for Source.
* Thu May 06 2004 - <matt.keenan@sun.com>
- Bump to 0.5
* Tue Feb 24 2004 - <matt.keenan@sun.com>
- Bump to 0.4, configure and install rules
* Mon Feb 16 2004 - <niall.power@sun.com>
- replace tar jxf with the setup macro
- replace /usr with %{_prefix}
* Tue Feb 10 2004 - <matt.keenan@sun.com>
- Initial verison for cinnabar
