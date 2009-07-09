#
# spec file for package gnome-system-tools
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include l10n.inc
Name:		gnome-system-tools
License:	GPL
Group:		System/GUI/GNOME
# WARNING: Do NOT bump version as other dependencies (e.g DBUS) need work first.
Version:	2.14.0
Release:	1
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	GNOME System Tools
Source:		http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.14/%{name}-%{version}.tar.bz2
Source1:	%{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:        l10n-configure.sh
%endif
Source3:        %{name}-network-admin.ksh
# date:2006-03-10 owner:dkenny type:feature
Patch1:		gnome-system-tools-01-config.diff
# date:2006-03-10 owner:dkenny type:feature bugster:6357680
Patch2:		gnome-system-tools-02-forkpty.diff
# date:2006-03-10 owner:dkenny type:feature
Patch3:		gnome-system-tools-03-network.diff
# date:2006-03-10 owner:dkenny type:feature
Patch4:		gnome-system-tools-04-tz.diff
# date:2006-03-10 owner:dkenny type:feature
Patch5:		gnome-system-tools-05-shares.diff
# date:2006-03-28 owner:padraig type:feature
Patch6:		gnome-system-tools-06-time.diff
# date:2006-03-27 owner:padraig type:feature
Patch7:		gnome-system-tools-07-users.diff
# date:2006-08-30 owner:dkenny type:feature
Patch8:		gnome-system-tools-08-services.diff
# date:2006-11-15 owner:calumb bugster:6489289 bugzilla:375678 type:bug
Patch9:         gnome-system-tools-09-launch-menu-item.diff
# date:2007-03-04 owner:dcarbery bugzilla:414654 type:bug
Patch10:        gnome-system-tools-10-role-maintainer.diff
# date:2007-08-30 owner:dcarbery type:branding
Patch11:        gnome-system-tools-11-all-linguas.diff
# date:2008-01-11 owner:dcarbery type:bug bugzilla:508804
Patch12:        gnome-system-tools-12-nautilus-dir.diff
# date:2009-04-06 owner:fujiwara type:bug bugster:6493486,6493462
Patch13:        gnome-system-tools-13-g11n-i18n-ui.diff
URL:		http://www.gnome.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/%{name}
Autoreqprov:	on
Prereq:         GConf

%define libgnomeui_version 2.9.0
%define GConf_version 2.2.0
%define system_tools_backends_version 1.2.0
%define nautilus_version 2.9.3

Requires:	libgnomeui >= %{libgnomeui_version}
Requires:	GConf >= %{GConf_version}
Requires:	system-tools-backends >= %{system_tools_backends_version}
Requires:	nautilus >= %{nautilus_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:	system-tools-backends >= %{system_tools_backends_version}
BuildRequires:	nautilus-devel >= %{nautilus_version}
BuildRequires:  intltool

%description
These tools are intended to simplify the tasks of configuring a Unix system
for workstations. They are not intended for configuring Unix servers.

Configuring different Unix systems is different; every Unix system has
different ways of being administrated. The GNOME System Tools aspire to
unify these systems.

Each one of the GNOME System Tools is split in two parts: a backend (which
is typically written in Perl) and a user interface frontend (which is
typically written in C or Python).

The backends are written in a way that should allow us to quickly adapt
them to various different flavors of Unix; the backend probes your system
and parses the existing system files. When the user has finished editing
the system settings, the configuration is written back as patches to the
system files.

This means that the GNOME System Tools use whatever configuration files are
available on your system, and you can still edit those files by hand or
with other configuration tools without conflicts or data loss.

%prep
%setup -q
# intltool needs extension ".sh"
cp %SOURCE3 network-admin.sh

%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
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

glib-gettextize -f
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
libtoolize --force
autoheader
automake -a -c -f
autoconf

%ifos solaris
CFLAGS="-D NOPTY -D USE_AUTHEN_PAM $RPM_OPT_FLAGS" \
%else
CFLAGS="$RPM_OPT_FLAGS" \
%endif

  ./configure \
	--prefix=%{_prefix} 		  \
	--sysconfdir=%{_sysconfdir}       \
	--localstatedir=%{_localstatedir} \
	--mandir=%{_mandir}	          \
	--disable-scrollkeeper
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
rm $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/libnautilus-gst-shares.la
rm $RPM_BUILD_ROOT%{_libdir}/nautilus/extensions-2.0/libnautilus-gst-shares.a
rm -rf $RPM_BUILD_ROOT%{_localstatedir}/scrollkeeper

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gnome-system-tools.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libdir}/nautilus/extensions-2.0/libnautilus-gst-shares.so
%{_libdir}/pkgconfig/
%{_datadir}/applications/
%{_datadir}/gnome-system-tools/
%{_datadir}/gnome/help/
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/
%{_sysconfdir}/gconf/schemas/*

%changelog
* Mon Apr 06 2009 - takao.fujiwara@sun.com
- Add patch 13-g11n-i18n-ui.diff for i18n time-admin CR 6493486,6493462
- Update 02-forkpty.diff for gettext().
- Update 06-time.diff for SUN_BRANDING and community strings & translations.
- Update 08-services.diff to get community strings & translations.

* Wed Jul  9 2008 - takao.fujiwara@sun.com
- Add %{name}-network-admin.ksh to get the SUN_BRANDING translation.

* Fri Jan 11 2008 - damien.carbery@sun.com
- Add patch 12-nautilus-dir to determine nautilus extension dir via pkgconfig.

* Thu Aug 30 2007 - damien.carbery@sun.com
- Add patch, 11-all-linguas, to list locales on one line in po/Makefile. This
  is required after a bump of intltool.

* Wed May 16 2007 - takao.fujiwara@sun.com
- Add l10n tarball.

* Sun Mar 04 2007 - damien.carbery@sun.com
- Add patch, 10-role-maintainer, to fix C locale xml files. Fixes 414654.

* Wed Nov 15 2006 - calum.benson@sun.com
- Change menu item to match latest UI spec.

* Sat Oct 21 2006 - jim.li@sun.com
- Run autoconf since we're patching configure.ac to look for gksu.

* Mon Apr 10 2006 - padraig.obriain@sun.com
- Add define USE_AUTHEN_PAM for Solaris

* Fri Mar 24 2006 - padraig.obriain@sun.com
- Add patch gnome-system-tools-07-users.diff.

* Thu Mar 16 2006 - padraig.obriain@sun.com
- Move patches here from Solaris package spec file.

* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.0.

* Thu Feb  2 2006 - damien.carbery@sun.com
- Bump to 2.13.2.

* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 2.13.1.

* Tue Sep 27 2005 - damien.carbery@sun.com
- Bump to 1.3.92.

* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 1.3.2.

* Tue May 24 2005 - glynn.foster@sun.com
- Initial spec
