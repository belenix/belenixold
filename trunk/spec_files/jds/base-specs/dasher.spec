#
# spec file for package dasher
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include l10n.inc
Name:           dasher
License:	GPL v2, MIT/X
Group:		System/GUI/GNOME
Version:        4.10.0
Release:	1
Distribution:	Java Desktop System
Vendor:		Sun Microsystems, Inc.
Summary:	Predictive text entry system
Source:		http://ftp.gnome.org/pub/GNOME/sources/dasher/4.10/%{name}-%{version}.tar.bz2
Source1:	%{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
# owner:yippi date:2006-04-27 type:branding
Patch1:         dasher-01-menu-entry.diff
# owner:yippi date:2007-06-07 type:bug bugzilla:438925
Patch2:         dasher-02-vector.diff
# owner:yippi date:2009-03-17 type:bug bugzilla:575729
Patch3:         dasher-03-fixcompile.diff
# owner:yippi date:2009-03-31 type:bug bugzilla:575730
Patch4:         dasher-04-speed.diff
URL:		http://www.gnome.org
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
Docdir:		%{_defaultdocdir}/%{name}
Autoreqprov:	on

%define gtk2_version 2.3.1
%define GConf_version 2.4.0.1
%define libgnomeui_version 2.6.0
%define libwnck_version 2.6.0
%define gnome_speech_version 0.3.0

Requires:	gtk2 >= %{gtk2_version}
Requires:	GConf >= %{GConf_version}
Requires:	libgnomeui >= %{libgnomeui_version}
Requires:	libwnck >= %{libwnck_version}
Requires:	gnome-speech >= %{gnome_speech_version}
BuildRequires:  gtk2-devel >= %{gtk2_version}
BuildRequires:  GConf-devel >= %{GConf_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  libwnck-devel >= %{libwnck_version}
BuildRequires:  gnome-speech-devel >= %{gnome_speech_version}
BuildRequires:  intltool

%description
Dasher is a zooming predictive text entry system, designed for situations
where keyboard input is impractical (for instance, accessibility or PDAs). It
is usable with highly limited amounts of physical input while still allowing
high rates of text entry.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1

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
intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
	--mandir=%{_mandir}
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/applications
%{_datadir}/dasher
%{_datadir}/gnome/help
%{_datadir}/icons
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/man
%{_datadir}/omf

%changelog
* Tue Mar 31 2009 - brian.cameron@sun.com
- Add patch dasher-04-speed.diff so that the speed selection works in dasher.
  Fixes bugzilla bug #575730.
* Tue Mar 17 2009 - brian.cameron@sun.com
- Bump to 4.10.0.  Remove upstream patches dasher-03-add-libsocket.diff
  and dasher-04-fixcompile.diff.  Add new patch dasher-03-fixcompile.diff
  to address new compilation issue.
* Thu Jun 05 2008 - brian.cameron@sun.com
- Add patch dasher-05-fixcompile.diff so that 4.9.0 compiles.
  Fixes bugzilla bug 536926.
* Wed May 28 2008 - damien.carbery@sun.com
- Bump to 4.9.0.
* Wed May 14 2008 - dave.lin@sun.com
- Add patch dasher-03-add-libsocket.diff to fix build error
* Wed Apr 08 2008 - damien.carbery@sun.com
- Bump to 4.7.3. Remove upstream patches, 03-gnu_cxx and 04-fixcompile.
* Tue Nov 13 2007 - brian.cameron@sun.com
- Add patch dasher-05-fixcompile.diff to fix Sun Studio compile issues.
- Remove dasher-02-joystick.diff since it is no longer needed.  Now
  joystick support is off by default, and you have to use
  --enable-joystick to turn on the joystick code that breaks on
  Solaris.
* Tue Nov 13 2007 - damien.carbery@sun.com
- Bump to 4.7.0.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 4.6.1.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 4.6.0.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 4.5.2.
* Fri Jun 09 2007 - damien.carbery@sun.com
- Add Brett Albertson's three patches that get dasher to successfully build.
* Tue Jun 05 2007 - damien.carbery@sun.com
- Bump to 4.5.1.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 4.5.0.
* Thu Apr 12 2007 - damien.carbery@sun.com
- Bump to 4.4.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 4.4.0.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Remove upstream patch, 03-return-value.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 4.3.5.
* Wed Feb 14 2007 - damien.carbery@sun.com
- Add patch, 03-return-value, to return values from functions (functions
  involved as in the process of being reimplemented). Fixes #407773.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 4.3.4.
* Thu Jan 04 2007 - damien.carbery@sun.com
- Add patch, 02-joystick, to get module to build. It is a dreadful hack, but
  pushed upstream (#388198) to encourage the maintainer to find a better
  solution. Add intltoolize call to get l10n files installed.
* Wed Dec 20 2006 - brian.cameron@sun.com
- Remove nodividebyzero patch since it is no longer needed.  New
  version of dasher no longer allows the problem to happen.  Remove
  unnecessary linguas patch.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 4.3.3.
* Thu Dec 14 2006 - brian.cameron@sun.com
- Patch to avoid divide by zero which causes dasher to core dump.
* Mon Dec 04 2006 - damien.carbery@sun.com
- Bump to 4.3.2. Remove upstream patches, 01-forte and 03-fixcompile. Renumber
  remainder.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 4.2.2.
* Wed Oct 25 2006 - damien.carbery@sun.com
- Bump to 4.2.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 4.2.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 4.1.10.
* Tue Aug 08 2006 - brian.cameron@sun.com
- Bump to 4.1.9.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 4.1.8.
* Web Jul 20 2006 - dermot.mccluskey@sun.com
- Bump to 4.1.7.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 4.1.4.  Add patches to fix build, now call glib-gettextize.
* Fri Apr 28 2006 - glynn.foster@sun.com
- Add patch to move Dasher into Universal
  Access.
* Mon Apr 3 2006 - damien.carbery@sun.com
- Bump to 4.0.2.
* Sat Mar 18 2006 - damien.carbery@sun.com
- Bump to 4.0.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 4.0.0.
* Sun Feb 26 2006 - damien.carbery@sun.com
- Bump to 3.99.5.
* Tue Feb 21 2006 - brian.cameron@sun.com
- Add patch 1 to get dasher to compile with Forte.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Remove upstream patch, 01-trace.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 3.99.4.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 3.99.3.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 3.99.2.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 3.99.1.
* Fri Sep 30 2005 - brian.cameron@sun.com
- Add patch 1 to get dasher to compile.  Got Trace.cpp from
  CVS head.  Seems to be a bug in dasher that this file isn't
  included in the compile, so submitted a bug to bugzilla.  
  I suspect Forte's stricter linking rules cause this issue
  on Solaris.
* Thu Sep 08 2005 - damien.carbery@sun.com
- Bump to 3.2.18.
* Tue May 24 2005 - glynn.foster@sun.com
- Initial spec
