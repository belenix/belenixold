#
# spec file for package ospm
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
# bugdb: defect.opensolaris.org/bz
#
Name:			ospm
License:		GPL v2
Group:			System/GUI/GNOME
# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
Version:		1.4.8
Release:		1
Distribution:	Java Desktop System
Vendor:			Sun Microsystems, Inc.
Summary:		GNOME Remote Desktop
Source:			http://dlc.sun.com/osol/jds/downloads/extras/%{name}/%{name}-%{version}.tar.bz2
Source1:                l10n-configure.sh
BuildRoot:		%{_tmppath}/%{name}-%{version}-build
Docdir:			%{_defaultdocdir}/doc
Autoreqprov:		on

%define			gtk2_version 2.2.0
%define			GConf_version 2.2.0
%define			libglade_version 2.0.0
%define                 intltool_version 0.25

Requires:		gtk2           >= %{gtk2_version}
Requires:		GConf          >= %{GConf_version}
Requires:		libglade       >= %{libglade_version}
BuildRequires:		gtk2-devel     >= %{gtk2_version}
BuildRequires:		GConf-devel    >= %{GConf_version}
BuildRequires:		libglade-devel >= %{libglade_version}
BuildRequires:		intltool       >= %{intltool_version}

%description
Ospm is an printer management tool. It can support local USB printer
queue plug/unplug configration automaticlly. A printer management tool
to let use mamnage own printers and jobs.

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

aclocal $ACLOCAL_FLAGS
libtoolize --force
gnome-doc-prepare --copy --force --automake
intltoolize --force --automake

bash -x %SOURCE1 --enable-copyright

autoheader
automake -a -f -c --gnu
autoconf 

CFLAGS="$RPM_OPT_FLAGS"				\
./configure   --prefix=%{_prefix}		\
	      --sysconfdir=%{_sysconfdir}

make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT

export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/ospm-server.schemas >/dev/null

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_bindir}/*
%{_libdir}/bonobo/servers/*
%{_libexecdir}/*
%{_datadir}/applications/
%{_datadir}/gnome/ospm/*
%{_datadir}/icons/
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%config %{_sysconfdir}/gconf/schemas/*

%changelog
* Thu Mar 05 2009 - ghee.teo@sun.com
- Up-rev tarball to 1.4.8 to fix 6811380.
* Tue Feb 10 2009 - halton.huo@sun.com
- Add ospm-02-conflict-func.diff to fix CR #6803372
* Tue Dec 02 2008 - takao.fujiwara@sun.com
- Add ospm-01-no-net-during-build.diff to stop a build failure.
  The http dtd should be defined in /usr/share/sgml/docbook/xmlcatalog
  not to access network.
* Thu Oct 30 2008 - haltn.huo@sun.com
- Bump to 1.4.7 to contain non-C gnome-help and omf
- Add add gnome-doc-prepare
* Wed Oct 01 2008 - ghee.teo@sun.com
- Bump to 1.4.6 to contain fix for 6754585.
* Sat Sep 27 2008 - halton.huo@sun.com
- Bump to 1.4.5
- Fix Source URL error
* Thu Sep 24 2008 - ghee.teo@sun.com
- Uprev tarball to 1.4.4
* Thu Sep 18 2008 - ghee.teo@sun.com
- Uprev tarball to 1.4.3
* Wed Sep 10 2008 - halton.huo@sun.com
- Remove some files not exist
* Wed Aug 27 2008 - halton.huo@sun.com
- Bump to 1.4.1
* Thu Jul 24 2008 - halton.huo@sun.com
- Bump to 1.4.
- Remove upsteamed patches dbus-error-init.diff, po.diff and add-libsocket.diff 
* Wed May 14 2008 - dave.lin@sun.com
- Add patch ospm-03-add-libsocket.diff to fix build error
* Thu May 08 2008 - takao.fujiwara@sun.com
- Add ospm-01-po.diff for cs.po
  Contributed l10n from Hana Zalska <Hana.Zalska@sun.com>
* Fri Mar 21 2008 - halton.huo@sun.com
- Bump to 0.2.1
- Remove upstreamed patches: hal-miss-data.diff
  freed-file-pointer.diff, queue-exists-on-system.diff
  disable-hal-crash.diff
* Wed Dec 06 2007 - halton.huo@sun.com
  Added patch ospm-04-disable-hal-crash.diff to fix bugster 6633471.
* Wed Dec 05 2007 - ghee.teo@sun.com
  Added patch ospm-03-queue-exists-on-system.diff 
* Tue Dec 04 2007 - ghee.teo@sun.com
- Modified ospm-02-freed-file-pointer.diff to include
  also printer to have MAXPATHLEN committed by Norm.
* Tue Aug 14 2007 - evan.yan@sun.com
- Add patch hal-miss-data.diff
* Thu Jul 10 2007 - evan.yan@sun.com
- Bump to version 0.2 and remove upstream patches
* Tue Jun 26 2007 - halton.huo@sun.com
- Add patches critical-warning.diff and quit-crash.diff
* Thu Jun 21 2007 - halton.huo@sun.com
- Fix source url error.
* Fri Apr 27 2007 - halton.huo@sun.com
- Initial spec file
