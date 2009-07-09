#
# spec file for package devhelp.spec
#
# Copyright (c) 2007 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%include l10n.inc
Name:          devhelp
License:       GPL v2
Group:         System/GUI/GNOME
#### DO NOT BUMP MODULE TO 0.22 or LATER AS IT IS DEPEND ON WEBKIT WHICH IS
#### NOT YET READY FOR SOLARIS
Version:       0.23
Release:       1
Distribution:  Java Desktop System
Vendor:        Sun Microsystems, Inc.
Summary:       API documentation browser for GNOME 
Source:        http://download.gnome.org/sources/devhelp/0.23/devhelp-%{version}.tar.bz2
%if %build_l10n
Source1:       %{name}-po-sun-%{po_sun_version}.tar.bz2
%endif
#date:2008-08-15 owner:jedy type:branding
Patch1:       devhelp-01-menu-entry.diff

URL:           http://developer.imendio.com/projects/devhelp
BuildRoot:     %{_tmppath}/%{name}-%{version}-build

%define gtk2_version 2.5.3
%define gnome_vfs_version 2.6.0
%define libgnomeui_version 2.6.0
%define libbonobo_version 2.6.0
%define libxslt_version 1.1.14
%define libglade_version 2.5.1
%define libxml2_version 2.6.5
%define mozilla_version 1.7
%define libwnck_version 2.16.0

Requires: gtk2 >= %{gtk2_version}
Requires: gnome-vfs >= %{gnome_vfs_version}
Requires: libgnomeui >= %{libgnomeui_version}
Requires: libbonobo >= %{libbonobo_version}
Requires: libxslt >= %{libxslt_version}
Requires: libglade >= %{libglade_version}
Requires: libxml2 >= %{libxml2_version}
Requires: mozilla >= %{mozilla_version}
Requires: libwnck >= %{libwnck_version}

BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: libxslt-devel >= %{libxslt_version}
BuildRequires: mozilla-devel >= %{mozilla_version}
BuildRequires: libwnck-devel >= %{libwnck_version}

%description
Devhelp is an API documentation browser for GNOME 2. It works natively with gtk-doc (the API reference framework developed for GTK+ and used throughout GNOME for API documentation).

%package devel
Summary:                 Library to embed Devhelp in other applications
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
Requires: SUNWgnome-base-libs-devel

%description devel
Library of Devhelp for embedding into other applications.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif

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
glib-gettextize -f
intltoolize --force --copy
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir} --disable-gtk-doc
make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)
%doc AUTHORS ChangeLog COPYING NEWS README TODO
%config %{_sysconfdir}/gconf/schemas/devhelp.schemas
%{_bindir}/devhelp*
%{_datadir}/applications/devhelp.desktop
%{_datadir}/devhelp/
%{_datadir}/mime-info/devhelp.*
%{_datadir}/pixmaps/devhelp.png
%{_libdir}/libdevhelp-1.so.*

%files devel
%defattr(-, root, root)
%{_includedir}/devhelp-1.0/
%{_libdir}/libdevhelp-1.so
%{_libdir}/pkgconfig/libdevhelp-1.0.pc

%changelog
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.

* Tue Sep 23 2008 - simon.zheng@sun.com
- Bump to 0.21.

* Tue Sep 09 2008 - simon.zheng@sun.com
- Bump to 0.20.
- Remove upstream 03-using-firefox3-gecko.diff.

* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.

* Thu Aug 21 2008 - jedy.wang@sun.com
- remove option_with_indiana_branding

* Fir Aug 14 2008 - jedy.wang@sun.com
- add 02-desktop.diff.

* Mon May 26 2008 - evan.yan@sun.com
- add option "--with-ff3" to enable building with Firefox3

* Mon May 26 2008 - damien.carbery@sun.com
- Bump to 0.19.1.

* Fri May 16 2008 - damien.carbery@sun.com
- Comment out Evan's patch, 01-using-firefox3-gecko, so that we build against
  firefox 2 because FF3 is not stable enough to be the default browser in
  Nevada.

* Thu May 08 2008 - evan.yan@sun.com
- Add patch devhelp-01-using-firefox3-gecko.diff:
  build devhelp with firefox3 package
- Add running auto tools

* Fri Feb 08 2008 - damien.carbery@sun.com
- Bump to 0.19.

* Wed Jan 30 2008 - damien.carbery@sun.com
- Bump to 0.18.

* Mon Jan 08 2008 - damien.carbery@sun.com
- Bump to 0.17.

* Sun Dec 16 2007 - patrick.ale@gmail.com
- Change the way version is defined so pkgtool plays
  nicely with minor versions [due to HTTP 404 upon fetching]

* Mon Oct 08 2007 - damien.carbery@sun.com
- Bump to 0.16.1.

* Tue Sep 11 2007 - damien.carbery@sun.com
- Bump to 0.16.

* Tue Jun 19 2007 - simon.zheng@sun.com
- Bump to 0.15. Remove upstream patch, 01-va-args.

* Thu May 17 2007 - simon.zheng@sun.com
- Bump to 0.14. Add patch 01-va-args to fix 439054.

* Fri Mar 14 2007 - simon.zheng@sun.com
- Initial version created, which stems from extra-spec-file
  created by li.ma@sun.com on sourceforge.net svn repository.
