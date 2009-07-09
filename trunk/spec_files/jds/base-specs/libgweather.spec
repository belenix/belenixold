#
# spec file for package libgweather
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include l10n.inc
Name:         libgweather
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Library to access weather information from online services
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgweather/2.26/%{name}-%{version}.tar.bz2
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on

%description
libgweather description.

%prep
%setup -q

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

#libtoolize --force
#intltoolize --force --copy --automake
aclocal $ACLOCAL_FLAGS
#autoheader
#automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"	\
./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libdir=%{_libdir}         \
        --bindir=%{_bindir}         \
	--libexecdir=%{_libexecdir} \
	--mandir=%{_mandir}         \
	--enable-all-translations-in-one-xml \
    --with-zoneinfo-dir=/usr/share/lib/zoneinfo \
	--localstatedir=/var/lib
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%clean
rm -rf $RPM_BUILD_ROOT


%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.92
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Wed Jan 29 2009 - matt.keenan@sun.com
- Bump to 2.25.5.
* Wed Jan 07 2009 - christian.kelly@sun.com
- Bump to 2.25.4.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - chrisian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 01 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
- Remove libgweather-01-uninstalled.diff and libgweather-02-zoneinfo-dir.diff
  fixed upstream, bugzilla:510125 and bugzilla:548440 bugster:6738588.
* Tue Aug 19 2008 - matt.keenan@sun.com
- Add configure option to correctly locate zoneinfo information, and log
  community bug #548440 to enable --with-zoneinfo-dir option
* Wed Aug 06 2008 - matt.keenan@sun.com
- Bump to 2.23.6.
* Wed Jul 22 2008 - damien.carbery@sun.com
- Bump to 2.23.5.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 2.23.2.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Wed Apr 16 2008 - damien.carbery@sun.com
- Bump to 2.22.1.2. Add --enable-all-translations-in-one-xml configure option
  to retain compatability with previous versions (and to actually build okay).
* Wed Apr 09 2008 - damien.carbery@sun.com
- Bump to 2.22.1.1.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Thu Feb 28 2008 - damien.carbery@sun.com
- Call aclocal to get patched intltool.m4.
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Initial Sun release.
