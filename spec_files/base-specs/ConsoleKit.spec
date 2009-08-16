#
# spec file for package ConsoleKit
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
# bugdb: http://bugs.freedesktop.org/show_bug.cgi?id=
#

Name:         ConsoleKit
License:      GPL v2+
Group:        Libraries
Version:      0.3.1
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Framework for tracking users, login sessions, and seats.
URL:          http://www.freedesktop.org/wiki/Software/ConsoleKit
Source:       http://www.freedesktop.org/software/ConsoleKit/dist/%{name}-%{version}.tar.bz2
# date:2008-03-04 owner:halton type:bug bugid:18261
Patch1:       ConsoleKit-01-ck-history.diff
# date:2008-12-30 owner:halton type:bug bugid:19333
Patch2:       ConsoleKit-02-ck-dynamic.diff
# date:2009-07-23 owner:halton type:branding
Patch3:       ConsoleKit-03-add-sunray-type.diff
# date:2009-07-23 owner:halton type:branding
Patch4:       ConsoleKit-04-dynamic-tty.diff
# date:2009-07-23 owner:halton type:branding
Patch5:       ConsoleKit-05-solaris-vtdaemon.diff
# date:2009-07-23 owner:yippi type:branding
Patch6:       ConsoleKit-06-dev-console.diff
# date:2009-07-27 owner:gheet type:bug doo:10291 bugid:22986
Patch7:       ConsoleKit-07-close-fp.diff

# Moinakg: Fix PAM module build.
Patch8:       ConsoleKit-08-pam_build.diff

BuildRequires:  PolicyKit-devel >= 0.7
BuildRequires:  autoconf >= 2.60
BuildRequires:  automake >= 1:1.9
BuildRequires:  dbus-glib-devel >= 0.30
BuildRequires:  gettext-devel
BuildRequires:  glib2-devel >= 1:2.8.0
# for <sys/inotify.h>
BuildRequires:  glibc-devel >= 6:2.4
BuildRequires:  libtool >= 1.4
BuildRequires:  pam-devel >= 0.80
BuildRequires:  pkgconfig
BuildRequires:  rpmbuild(macros) >= 1.268
BuildRequires:  xmlto
BuildRequires:  xorg-lib-libX11-devel >= 1.0.0
BuildRequires:  zlib-devel
Requires:       /sbin/chkconfig
Requires:       %{name}-libs = %{version}-%{release}
Requires:       dbus-glib >= 0.30
Requires:       glib2 >= 1:2.8.0
Requires:       rc-scripts
Requires:       xorg-lib-libX11 >= 1.0.0
BuildRoot:      %{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
ConsoleKit is a framework for defining and tracking users, login
sessions, and seats.

%package libs
Summary:        ConsoleKit library
Summary(pl.UTF-8):      Biblioteka ConsoleKit
License:        AFL v2.1 or GPL v2
Group:          Libraries
Requires:       dbus-libs >= 0.30
Conflicts:      ConsoleKit < 0.1-0.20061203.6

%description libs
ConsoleKit library.

%package devel
Summary:        Header files for ConsoleKit
Summary(pl.UTF-8):      Pliki nagłówkowe ConsoleKit
License:        AFL v2.1 or GPL v2
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}
Requires:       dbus-devel >= 0.30

%description devel
Header files for ConsoleKit.

%package static
Summary:        Static ConsoleKit library
Summary(pl.UTF-8):      Statyczna biblioteka ConsoleKit
License:        AFL v2.1 or GPL v2
Group:          Development/Libraries
Requires:       %{name}-devel = %{version}-%{release}

%description static
Static ConsoleKit library.

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

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

glib-gettextize -f
libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix}                     \
            --libdir=%{_libdir}                     \
            --libexecdir=%{_libexecdir}             \
            --localstatedir=%{_localstatedir}       \
            --sysconfdir=%{_sysconfdir}             \
            --mandir=%{_mandir}                     \
%if %build_pam_module
            --enable-pam-module                     \
            --with-pam-module-dir=%{_libdir}/security   \
%endif
            --enable-rbac-shutdown=solaris.system.shutdown
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'
%if %build_pam_module
%else
# delete useless directory /usr/man/man8 which stores pam_ck_connector.8 
#
rm -rf $RPM_BUILD_ROOT/%{_mandir}
%endif

# The /var/run directory should not be included with the packages.
# ConsoleKit will create it at run-time.
#
rmdir $RPM_BUILD_ROOT/var/run/ConsoleKit
rmdir $RPM_BUILD_ROOT/var/run

%clean
rm -rf $RPM_BUILD_ROOT

%post   libs -p /sbin/ldconfig
%postun libs -p /sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/ck-history
%attr(755,root,root) %{_bindir}/ck-launch-session
%attr(755,root,root) %{_bindir}/ck-list-sessions
%attr(755,root,root) %{_sbindir}/ck-log-system-restart
%attr(755,root,root) %{_sbindir}/ck-log-system-start
%attr(755,root,root) %{_sbindir}/ck-log-system-stop
%attr(755,root,root) %{_sbindir}/console-kit-daemon
%attr(755,root,root) %{_libdir}/ck-collect-session-info
%attr(755,root,root) %{_libdir}/ck-get-x11-server-pid
%attr(755,root,root) %{_libdir}/ck-get-x11-display-device
%dir %{_prefix}/lib/ConsoleKit/scripts
%attr(755,root,root) %{_prefix}/lib/ConsoleKit/scripts/*
%attr(755,root,root) /%{_lib}/security/pam_ck_connector.so
%{_datadir}/PolicyKit/policy/org.freedesktop.consolekit.policy
%{_datadir}/dbus-1/system-services/org.freedesktop.ConsoleKit.service
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Manager.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Seat.xml
%{_datadir}/dbus-1/interfaces/org.freedesktop.ConsoleKit.Session.xml
%{_sysconfdir}/dbus-1/system.d/ConsoleKit.conf
%dir %{_sysconfdir}/ConsoleKit
%dir %{_sysconfdir}/ConsoleKit/run-session.d
%dir %{_sysconfdir}/ConsoleKit/seats.d
%{_sysconfdir}/ConsoleKit/seats.d/00-primary.seat
%{_mandir}/man8/pam_ck_connector.8*
%dir %{_localstatedir}/run/ConsoleKit
%dir %{_localstatedir}/log/ConsoleKit

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libck-connector.so.0

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libck-connector.so
%{_libdir}/libck-connector.la
%dir %{_includedir}/ConsoleKit
%dir %{_includedir}/ConsoleKit/ck-connector
%{_includedir}/ConsoleKit/ck-connector/*.h
%{_libdir}/pkgconfig/ck-connector.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libck-connector.a

%changelog
* Mon Jul 27 2009 - halton.huo@sun.com
- New from SFEconsolekit.spec
