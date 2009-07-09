#
# spec file for package tracker
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan
#

%include l10n.inc
Name:           tracker
License:        GPL v2
Group:          Applications/System
Version:        0.6.94
Release:        1
Distribution:   Java Desktop System
Vendor:         Sun Microsystems, Inc.
URL:            http://www.tracker-project.org
Summary:        Desktop search tool
Source:         ftp://ftp.gnome.org/pub/GNOME/sources/tracker/0.6/tracker-%{version}.tar.gz
Source1:        l10n-configure.sh
Source2:        %{name}-po-sun-%{po_sun_version}.tar.bz2
# date:2008-01-23 owner:halton type:branding
Patch1:         %{name}-01-disable-autostart.diff
# date:2008-01-23 owner:jerrytan type:branding
Patch2:         %{name}-02-man.diff
# date:2008-08-22 owner:jerrytan type:branding bugster:6723896
Patch3:        tracker-03-removetag.diff
# date:2008-09-12 owner:jedy type:branding
Patch4:        tracker-04-menu-entries.diff
# date:2008-10-27 owner:jerrytan type:branding
Patch5:        tracker-05-disable-home-index.diff
# date:2009-02-24 owner:jerrytan type:branding
Patch6:        %{name}-06-upgrade.diff
# date:2009-03-04 owner:jerrytan type:branding
Patch7:        %{name}-07-replace-odt2txt-with-o3read.diff
# date:2009-03-30 owner:jerrytan type:branding
Patch8:        %{name}-08-strcasestr.diff 
BuildRoot:      %{_tmppath}/%{name}-%{version}-root

BuildRequires: gmime-devel, poppler-devel, gettext
BuildRequires: gnome-desktop-devel, gamin-devel
BuildRequires: libexif-devel, libgsf-devel, gstreamer-devel
BuildRequires: desktop-file-utils, intltool
BuildRequires: sqlite-devel
BuildRequires: dbus-devel, dbus-glib


%description
Tracker is a powerful desktop-neutral first class object database,
tag/metadata database, search tool and indexer.

It consists of a common object database that allows entities to have an
almost infinte number of properties, metadata (both embedded/harvested as
well as user definable), a comprehensive database of keywords/tags and
links to other entities.

It provides additional features for file based objects including context
linking and audit trails for a file object.

It has the ability to index, store, harvest metadata. retrieve and search
all types of files and other first class objects

%package devel
Summary: Headers for developing programs that will use %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains the static libraries and header files needed for
developing with tracker

%prep
%setup -q
bash %SOURCE1 --enable-sun-linguas
bzcat %SOURCE2 | tar xf -
cd po-sun; make; cd ..

%if %option_with_sun_branding
%patch1 -p1
%endif
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1

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

intltoolize --force --automake

bash -x %SOURCE1 --enable-copyright

libtoolize --force
aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} \
			--bindir=%{_bindir} \
			--mandir=%{_mandir} \
			--libdir=%{_libdir} \
			--libexecdir=%{_bindir} \
			--datadir=%{_datadir} \
			--includedir=%{_includedir} \
			--sysconfdir=%{_sysconfdir} \
			--disable-warnings \
			--enable-external-sqlite \
			--enable-evolution-push-module 

make -j $CPUS

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
%doc AUTHORS ChangeLog COPYING NEWS README
%{_bindir}/htmless
%{_bindir}/tracker*
%{_datadir}/tracker/
%{_datadir}/pixmaps/tracker/
%{_datadir}/dbus-1/services/org.freedesktop.Tracker.*
%{_datadir}/gtk-doc/
%{_libexecdir}/tracker*
%{_libdir}/*.so.*
%{_mandir}/man1/tracker*.1.gz
%{_sysconfdir}/xdg/autostart/trackerd.desktop

%files devel
%defattr(-, root, root)
%{_includedir}/tracker*
%{_libdir}/*.so
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Apr 15 2009 - dave.lin@sun.com
- Bump to 0.6.93
* Wed Mar 04 2009 - jerry.tan@sun.com
- Add tracker-18-replace-odt2txt-with-o3read.diff to use o3read until odt2txt introduced
* Tue Feb 24 2009 - jerry.tan@sun.com
- Add tracker-17-upgrade.diff to upgrade to tracker0.6.90
* Mon Feb 16 2009 - jerry.tan@sun.com
- Add tracker-16-extract-jpeg-core-dump.diff to fix bug 6802570 
* Fri Feb 06 2009 - jerry.tan@sun.com
- Add tracker-15-libumem-check.diff to fix bug 6763771
* Mon Dec 15 2008 - takao.fujiwara@sun.com
- Apply po.diff before l10n tarball is extracted.
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Fri Sep 12 2008 - jedy.wang@sun.com
- Add tracker-12-menu-entries.diff.
* Wed Aug 13 2008 - takao.fujiwara@sun.com
- Add tracker-10-po.diff from community trunk.
* Mon Mar 03 2008 - halton.huo@sun.com
- Bump to 0.6.6
- Remove upstreamed patch r1071-latest.diff and firefox-history.diff, reorder
* Wed Feb 27 2008 - halton.huo@sun.com
- Update comment for thunderbird.diff and firefox-history.diff to type:feature 
* Tue Feb 26 2008 - halton.huo@sun.com
- Update comment for r1071-latest.diff to type:feature state:upstream
* Wed Jan 23 2008 - nonsea@users.sourceforge.net
- Remove upstreamed patch preferences-explicit-apply.diff
- Add temporary patch tp-reindex.diff
* Tue Jan 22 2008 - nonsea@users.sourceforge.net
- Add patch preferences-explicit-apply.diff
- Add patch evo-reload.diff
- Add patch man.diff
- Rename r1071-r1092.diff to r1071-latest.diff
- Reorder patches.
* Thu Jan 03 2008 - nonsea@users.sourceforge.net
- Add patch disable-autostart.diff
- Add patch check-remote.diff
- Add patch r1071-r1092.diff
* Sat Nov 17 2007 - daymobrew@users.sourceforge.net
- Unbump to 0.6.3 and remove obsolete patch, 02-thunderbird.
* Fri Nov 02 2007 - nonsea@users.sourceforge.net
- Initial version, spilit from SFEtracker.spec
