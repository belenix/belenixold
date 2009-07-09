#
# spec file for package avahi
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
Name:         avahi
License:      Other
Group:        System/Libraries
Version:      0.6.23
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      System which facilitates service discovery on a local network.
Source:       http://www.avahi.org/download/%{name}-%{version}.tar.gz
Source1:      l10n-configure.sh
# date:2007-06-12 owner:padraig type:feature
Patch1:       avahi-01-config-bonjour.diff
# date:2007-06-12 owner:padraig type:feature
Patch2:       avahi-02-browse-service.diff
# date:2007-06-12 owner:padraig type:feature
Patch3:       avahi-03-entry.diff
# date:2007-06-12 owner:padraig type:feature
Patch4:       avahi-04-internal.diff
# date:2007-06-12 owner:padraig type:feature
Patch5:       avahi-05-resolve-service.diff
# date:2007-06-12 owner:padraig type:feature
Patch6:       avahi-06-server.diff
# date:2007-06-12 owner:padraig type:feature
Patch7:       avahi-07-daemon.diff
# date:2007-06-12 owner:padraig type:feature
Patch8:       avahi-08-man-page.diff
# date:2007-06-12 owner:padraig type:feature
Patch9:       avahi-09-resolve-host-name.diff
# date:2007-06-12 owner:padraig type:feature
Patch10:      avahi-10-resolve-address.diff
# date:2007-06-12 owner:padraig type:feature
Patch11:      avahi-11-browse-domain.diff
# date:2007-06-12 owner:padraig type:feature
Patch12:      avahi-12-browse.diff
# date:2007-06-12 owner:padraig type:feature
Patch13:      avahi-13-remove-debug-trap.diff
# date:2009-01-20 owner:fujiwara type:bug bugid:122 bugster:6795230 state:upstream
Patch14:      avahi-14-desktop.diff
# date:2009-03-05 owner:gheet type:branding bugid:263 bugster:6794539 
Patch15:      avahi-15-secure-dbus-dest.diff
URL:          http://ww.avahi.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define libdaemon_version 0.11
%define dbus_version 1.1.2
%define python_version 2.4

Requires:      libdaemon >= %{libdaemon-version}
BuildRequires: libdaemon-devel >= %{libdaemon-version}

Requires:      dbus >= %{dbus-version}
BuildRequires: dbus-devel >= %{dbus-version}

%description
Avahi is a system which facilitates service discovery on a local network.
This means that you can plug your laptop or computer into a network and
instantly be able to view other people you can chat with, find printers
to print to or find files being shared. This kind of technology is also
in Apple's Bonjour.


%package devel
Summary:      System which facilitiates service disconvery on a local network.
Group:        Development/Libraries
Requires:     %{name} = %{version}

%description devel
Avahi is a system which facilitates service discovery on a local network.
This measn thyat you can plug your laptop or computer into a network and
instantly be able to view other people you can chat with, find printers
to print to or find files being shared. This kind of technology is also
in Apple's Bonjour.


%prep
%setup -q
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

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

CONFLAGS="--prefix=%{_prefix}		\
          --with-avahi-user=daemon	\
          --with-avahi-group=other	\
          --sysconfdir=%{_sysconfdir}	\
          --localstatedir=%{_localstatedir} \
          --mandir=%{_mandir} 		\
          --with-distro=none		\
          --disable-qt3			\
          --disable-qt4			\
          --disable-mono		\
          --disable-monodoc		\
          --enable-tests		\
          --disable-compat-howl		\
          --disable-compat-libdns_sd	\
          --enable-expat		\
          --disable-autoipd		\
          --disable-gdbm		\
          --enable-dbm"

libtoolize --force
glib-gettextize -f
intltoolize --force --copy

bash -x %SOURCE1 --enable-copyright

autoreconf
autoheader
autoconf
CFLAGS="$RPM_OPT_FLAGS"
./configure $CONFLAGS

make -j $CPUS	\
   pyexecdir=%{_libdir}/python%{python_version}/vendor-packages

%install

make DESTDIR=$RPM_BUILD_ROOT install	\
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
rm -rf $RPM_BUILD_ROOT%{_libdir}/libavahi*a
rm -rf $RPM_BUILD_ROOT%{_localstatedir}
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.pyo" -exec rm -f {} ';'
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/avahi/avahi-daemon.conf
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/avahi/avahi-dnsconfd.action
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/avahi/hosts
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/avahi/services/sftp-ssh.service
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/avahi/services/ssh.service
rm -rf $RPM_BUILD_ROOT%{_sbindir}/avahi-dnsconfd
rm -rf $RPM_BUILD_ROOT%{_bindir}/avahi-discover-standalone
rm -rf $RPM_BUILD_ROOT%{_bindir}/avahi-bookmarks
rm -rf $RPM_BUILD_ROOT%{_mandir}/man5/avahi-daemon.conf.5
rm -rf $RPM_BUILD_ROOT%{_mandir}/man5/avahi.hosts.5
rm -rf $RPM_BUILD_ROOT%{_mandir}/man5/avahi.service.5
rm -rf $RPM_BUILD_ROOT%{_mandir}/man5
rm -rf $RPM_BUILD_ROOT%{_mandir}/man8
rm -rf $RPM_BUILD_ROOT%{_mandir}/man1/avahi-bookmarks.1


%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Tue Jan 20 2009 - takao.fujiwara@sun.com
- Add patch avahi-14-desktop.diff
- Remove patch avahi-14-show-menu-items.diff
* Wed Aug 06 2008 - padraig.obriain@sun.com
- Add patch avahi-14-show-menu-items.diff for 6726720.
  See http://www.avahi.org/ticket/234.
* Thu Jun 26 2008 - padraig.obriain@sun.com
- Uprev to 0.6.23; add calls to libtoolize and autoreconf
* Fri Jun 06 2008 - padraig.obriain@sun.com
- Uprev to 0.6.22; remove patch -14.
* Thu Sep 20 2007 - padraig.obriain@sun.com
- Add patch avahi-14-ui.diff to fix crash when no services are found.
* Tue June 12 2007 - padraig.obriain@sun.com
- Initial spec file for avahi.
