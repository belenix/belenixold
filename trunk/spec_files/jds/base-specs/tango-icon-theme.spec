#
# spec file for package tango-icon-theme
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
# bugdb: bugs.freedesktop.org
#
Name:         		tango-icon-theme
License:      		GPL
Group:        		System/GUI/GNOME
BuildArchitectures:	noarch
Version:      		0.8.90
Release:      		1
Distribution: 		Java Desktop System
Vendor:       		Sun Microsystems, Inc.
Summary:      		tango icon theme
Source:       		http://tango.freedesktop.org/releases/%name-%version.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
#owner:dcarbery date:2006-01-06 type:bug bugzilla:9837
Patch1:                 tango-icon-theme-01-pkgconfig_ver.diff
URL:          		http://tango.freedesktop.org/
BuildRoot:    		%{_tmppath}/%{name}-%{version}-build
Docdir:	      		%{_defaultdocdir}/doc
Autoreqprov:  		on

BuildRequires:		intltool
BuildRequires:		glib2
BuildRequires:		automake >= 1.9
BuildRequires:          icon-naming-utils

%description
The aim of the tango project is providing a standard set of
icons for the Linux desktop.

%prep
%setup -q
%patch1 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%{_datadir}/icons/tango
%{_libdir}/pkgconfig/tango-icon-theme.pc

%changelog
* Thu mar 26 2009 - brian.cameron@sun.com
- Bump to 0.8.90.
* Wed Nov 12 2008 - takao.fujiwara@sun.com
- Removed glib-gettextize to avoid a build error with intltool 0.40.5.
* Tue Aug 28 2007 - damien.carbery@sun.com
- Bump to 0.8.1.
* Tue Mar 06 2006 - brian.cameron@sun.com
- Bump to 0.8.0.
* Thu Feb 01 2007 - damien.carbery@sun.com
- Add patch metadata after pushing patch to bugzilla.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 0.7.2.
* Tue Feb 21 2006 - damien.carbery@sun.com
- Bump to 0.7.0.
* Thu Feb  9 2006 - damien.carbery@sun.com
- Bump to 0.6.7.
* Sat Jan 21 2006 - damien.carbery@sun.com
- Call intltoolize and glib-gettextize.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 0.6.5.
* Fri Jan 06 2006 - damien.carbery@sun.com
- Add patch to downgrade pkg-config ver and remove hard-coding of dir to
  icon-name-mapping (so it builds in the SUNWgnome-themes super-package).
* Wed Dec 21 2005 - damien.carbery@sun.com
- Bump to 0.6.3.
 Wed Oct 26 2005 - damien.carbery@sun.com
- Bump to 0.3.2.1.
* Sat Oct 15 2005 - laca@sun.com
- created

