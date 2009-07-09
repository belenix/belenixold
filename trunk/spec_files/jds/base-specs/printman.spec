#
# spec file for package printman
#
# Copyright (c) 2003 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include l10n.inc
Name:         printman
License:      GPL
Group:        System/GUI/GNOME
Version:      0.0.2
Release:      3
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Print manager for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/printman/0.0/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
# date:2007-02-06 type:branding owner:gheet 
Patch1:       printman-01-menu-entry.diff
# date:2007-02-06 type:branding owner:gheet 
Patch2:       printman-02-help-dir-changed.diff
# date:2007-02-06 type:branding owner:gheet 
Patch3:       printman-03-pkgconfig.diff
# date:2007-11-29 type:bug owner:fujiwara bugster:6311379 bugzilla:320600
Patch4:     printman-04-g11n-iconf-file-name.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       scrollkeeper

%define libgnomeui_version 2.4.0.1
%define scrollkeeper_version 0.3.12

Requires:       libgnomeui >= %{libgnomeui_version}
Requires:       scrollkeeper >= %{scrollkeeper_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:  scrollkeeper >= %{scrollkeeper_version}

%description
The GNOME Print Manager application enables you to control and manage printers and 
print jobs.

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
intltoolize --force --copy --automake
libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
	--sysconfdir=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
	--localstatedir=/var/lib
make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make -i install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

#remove its desktop file as ospm-pm is replacing its functiionality.
rm  -rf $RPM_BUILD_ROOT%{_datadir}/applications

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS=" gnome-print-manager.schemas "
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done
scrollkeeper-update -q

%postun
scrollkeeper-update -q

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/control-center-2.0/capplets/
%{_datadir}/gnome/help/gnome-printinfo/
%{_datadir}/omf/printman/
%{_datadir}/pixmaps/
%{_datadir}/locale/*/LC_MESSAGES/printman.mo

%changelog
* Fri Jan 16 2009 - christian.kelly@sun.com
- Added intltoolize command.
* Thu Nov 29 2007 - takao.fujiwara@sun.com
- Add printman-04-g11n-iconf-file-name.diff to show none UTF-8 icon names.
  Fixes 6311379

* Wed May 16 2007 - takao.fujiwara@sun.com
- Add l10n tarball.

* Sat Dec 10 2005 - laca@sun.com
- remove l10n help patch

* Wed Nov 30 2005 - damien.carbery@sun.com
- Remove javahelp stuff.

* Wed Jun 29 2005 - balamurali.viswanathan@wipro.com
- Modified printman-06-pkgconfig.diff so that all the required libs 
  are added.

* Thu Jun 23 2005 - balamurali.viswanathan@wipro.com
- Add patch pkgconfig.diff that add required libs explictly

* Wed Nov 24 2004 - kieran.colfer@sun.com
- updating l10n tarballs to fix 5094817, 6197170, 6197173, 6197203
(tarball revisions have to be kept consistent)

* Tue Nov 16 2004 - ciaran.mcdermott@sun.com
- Backing out printman-05-g11n-potfiles.diff until for for Linux

* Tue Nov 16 2004 - ciaran.mcdermott@sun.com
- Added printman-05-g11n-potfiles.diff to update potfiles.in
 
* Fri Oct 29 2004 - kieran.colfer@sun.com
- Uprevved l10n po tarball version from 1.6 to 1.7

* Fri Oct 29 2004 - kazuhiko.maekawa@sun.com
- Added
  printman-l10n-po-1.6.tar.bz2
  printman-l10n-online-help-ci.tar.bz2
  printman-03-l10n-online-help.diff
  printman-04-l10n-alllinguas.diff
  These came from spec-files/patches which was in wrong place.
* Wed Aug 25 2004 - archana.shah@wipro.com
- Install help document in gnome-printinfo/ instead of gnome-print-manager/.
  Also install help files under javahelp/
  Fixes bug#5081826
* Fri Jun 18 2003 - glynn.foster@Sun.COM
- Install the desktop file into another location
  to get picked up by the preference menu.
* Mon Jun 14 2003 - glynn.foster@Sun.COM
- Initial Sun release
