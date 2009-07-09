#
# spec file for package notificatioin-daemon
#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#Owner: jedy
#

Name:         notification-daemon
Version:      0.4.0
Release:      1
Summary:      A notification daemon for the GNOME desktop environment.

Group:        System/Libraries
License:      GPL
URL:          http://www.galago-project.org/news/index.php
URL:          http://www.galago-project.org/news/index.php
Distribution: java-desktop-system
Source:       http://www.galago-project.org/files/releases/source/notification-daemon/notification-daemon-%{version}.tar.bz2
# date:2008-11-13 owner:dkenny type:bug bugster:6752569 
Patch1:       notification-daemon-01-resize.diff
%if %build_l10n
Source1:                 l10n-configure.sh
%endif

BuildRoot:    %{_tmppath}/%{name}-%{version}-build

BuildRequires: gtk2 >= 2.4
BuildRequires: dbus-devel >= 0.36
BuildRequires: gnome-panel-devel
BuildRequires: libpopt-devel
BuildRequires: libsexy-devel >= 0.1.3
Requires: gtk2
Requires: dbus
Requires: gnome-panel
Requires: libpopt
Requires: libsexy

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q
%patch1 -p1

%build
%ifos linux
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --copy --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f 
autoconf
./configure --prefix=%{_prefix} \
		--libexecdir=%{_libexecdir} \
		--sysconfdir=%{_sysconfdir} \
		--libdir=%{_libdir}
make -j $CPUS

%install
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-, root, root)
%doc README AUTHORS COPYING
%{_sysconfdir}/gconf/schemas/notification-daemon.schemas
%{_libdir}/notification-daemon-1.0/engines/*.so*
%{_libexecdir}/notification-daemon
%{_datadir}/dbus-1/services/org.freedesktop.Notifications.service
%{_datadir}/locale/nl


%changelog
* Wed Dec 03 2008 - jedy.wang@sun.com
- Bump to 0.4.0.
* Wed Nov 12 2008 - darren.kenny@sun.com
- Add patch notification-daemon-01-resize.diff to fix bug#6752569 where the
  standard theme is not resizig the summary area if the body changes.
* Mon Jun 16 2008 - jedy.wang@sun.com
- Remove 01-no-libsexy to bring the libsexy dependency back.

* Thu Mar 25 2007 - jedy.wang@sun.com
- Initial spec
