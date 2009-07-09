#
# spec file for package gnome-terminal
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include l10n.inc
Name:         gnome-terminal
License:      GPL v2, Public Domain
Group:        System/GUI/GNOME
# DO NOT BUMP TO 2.25.x until we have EggSMClient is available
# Please refer to http://live.gnome.org/SessionManagement/EggSMClient
# and http://svn.gnome.org/viewvc/gnome-terminal?view=revision&revision=3072
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Terminal
Source:       http://download.gnome.org/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:yippi date:2006-05-04 type:branding
Patch1:       gnome-terminal-01-menu-entry.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:       GConf

%define libglade_version 2.6.0
%define libgnomeui_version 2.4.0
%define vte_version 0.13.3
%define startup_notification_version 0.5
%define scrollkeeper_version 0.3.12

BuildRequires: libglade-devel >= %{libglade_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: vte-devel >= %{vte_version}
BuildRequires: startup-notification-devel >= %{startup_notification_version}
BuildRequires: scrollkeeper >= %{scrollkeeper_version}
Requires:      libglade >= %{libglade_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      vte >= %{vte_version}
Requires:      startup-notification >= %{startup_notification_version}

%description
GNOME Terminal application, which uses the VTE terminal emulation widget.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1

# dos2unix to fix 400207.
dos2unix -ascii po/be.po po/be.po

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

intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

libtoolize --force
aclocal $ACLOCAL_FLAGS
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir} \
	    --disable-scrollkeeper
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
chmod 644 $RPM_BUILD_ROOT%{_datadir}/gnome/help/gnome-terminal/*/*.xml
rm -rf $RPM_BUILD_ROOT/usr/var/scrollkeeper

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

%clean
rm -rf $RPM_BUILD_ROOT

%post
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gnome-terminal.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%files
%defattr (-, root, root)
%{_datadir}/applications/gnome-terminal.desktop
%{_datadir}/gnome/help/gnome-terminal
%{_datadir}/omf/gnome-terminal
%{_datadir}/locale/*/LC_MESSAGES/gnome-terminal.mo
%{_libdir}/bonobo/servers/gnome-terminal.server
%{_sysconfdir}/gconf/schemas/gnome-terminal.schemas
%{_datadir}/pixmaps/gnome-terminal.png
%{_datadir}/gnome-terminal/glade/gnome-terminal.glade2
%{_bindir}/gnome-terminal
%{_mandir}/man1/*

%changelog
* Wed Mar 18 2009 - brian.cameron@sun.com
- Bump to 2.26.0.
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
- Removed upstreamed patch 02-gthread.diff.
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.5.  Remove upstream patch gnome-terminal-02-aa-no-xrender.diff.
  Add patch gnome-terminal-02-gthread.diff needed for code to compile.
* Wed Sep 24 2008 - christian.kelly@sun.com
- Bump to 2.24.0.
- Rework gnome-terminal-01-menu-entry.diff.
* Wed Sep 17 2008 - brian.cameron@sun.com
- Add gnome-terminal-02-aa-no-xrender.diff patch so that anti-aliasing is
  turned on when Xrender is not present.  Otherwise gnome-terminal looks
  really bad with Xsun, which normally doesn't have Xrender.  Partially
  fixes bug #6712204.
* Mon Sep 01 2008 - christian.kelly@sun.com
- Bumped to 2.23.91.
* Wed Aug 13 2008 - jedy.wang@sun.com
- Add root-terminal.desktop according to UI spec of OpenSolaris 2008.11.
* Tue Aug 05 2008 - christian.kelly@sun.com
- Bump to 2.23.6.
* Wed Jun 18 2008 - damien.carbery@sun.com
- Bump to 2.23.4.2.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.1.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Thu Jun 05 2008 - damien.carbery@sun.com
- Bump to 2.23.3.1.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Tue May 27 2008 - damien.carbery@sun.com
- Bump to 2.22.2.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Wed Feb 27 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.1.
* Tue Feb 12 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Wed Jan 30 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 15 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Sun Dec 23 2007 - damien.carbery@sun.com
- Bump to 2.21.4 because glib 2.15.0 has been released.
* Wed Dec 19 2007 - damien.carbery@sun.com
- Unbump to 2.21.3 because 2.21.4 requires glib 2.15.0 which has not yet been
  released.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.4. Remove upstream patch 01-encodings. Rename remainder.
* Wed Dec 05 2007 - brian.cameron@sun.com
- Bump to 2.21.3.  Remove patch gnome-terminal-03-fix-focus.diff and
  gnome-terminal-04-window-resizing.diff.  I verified that the bugster bugs
  #6462305 and #6463098 are no longer issues with the latest gnome-terminal,
  so these patches are no longer needed.
* Tue Nov 27 2007 - damien.carbery@sun.com
- Bump to 2.18.3.
* Tue Nov 06 2007 - brian.cameron@sun.com
- Add --disable-scrollkeeper to configure.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.18.2.
* Thu Apr 19 2007 - laca@sun.com
- add -ascii option to dos2unix so that utf8 strings are not messed up
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Wed Jan 24 2007 - damien.carbery@sun.com
- dos2unix be.po to fix 400207. Uncomment patch4 - reworked by dkenny.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Bump to 2.17.90. Comment out patch4, asking owner (dkenny) to rework it.
* Wed Nov 22 2006 - darren.kenny@sun.com
- Backport CVS HEAD fix for bugzilla bug#342968 and bugster#6463098 
* Tue Oct 10 2006 - padraig.obriain@sun.com
- Add patch gnome-terminal-03-fix-focus.diff for bug 6462305
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 01 2006 - damien.carbery@sun.com
- Bump to 2.15.4.
* Tue Jul 25 2006 - damien.carbery@sun.com
- Bump to 2.15.3.
* Fri Jul 21 2006 - brian.cameron@sun.com
- Bump to 2.15.2 for GNOME 2.15.
- Remove patch gnome-terminal-02-xft-pangoxft.diff as its change
  is already present.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.14.2.
* Fri May 05 2006 - glynn.foster@sun.com
- Move terminal to system tools rather than accessories.
* Mon Apr 10 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Sun Mar  5 2006 - damien.carbery@sun.com
- Bump to 2.13.93.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Add patch, 02-xft-pangoxft, to get build info for Xrender.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 2.13.3
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.2
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.1.
* Sat Jan 07 2006 - damien.carbery@sun.com
- Call intltoolize to process intltool-update/merge.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.0
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.3.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.2.
* Fri May 13 2005 - balamurali.viswanathan@wipro.com
- Bump 2.10.1
* Tue Jan 25 2005 - damien.carbery@sun.com
- Incorporate Linux specific docs tarball from maeve.anslow@sun.com.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Thu Oct 28 2004 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball and added pt_BR
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Updated l10n help contents with patch
* Mon Aug 16 2004 - damien.carbery@sun.com
- Updated /usr/share/gnome/help/gnome-terminal/*/*.xml to 0644 for Solaris
  integration.
* Thu Aug 05 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-terminal-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 25 2004 muktha.narayan@wipro.com
- Modified gnome-terminal-04-encodings.diff to correct the
  encoding names.
* Wed Jun 09 2004 muktha.narayan@wipro.com
- Added gnome-terminal-04-encodings.diff to fix the problem of 
  encodings not being listed on Solaris. Bug #5043182.
  Uploaded the patch in bugzilla - bug #144000.
* Wed Jun 02 2004 damien.carbery@sun.com
- Incorporate new docs tarball from breda.mccolgan@sun.com.
* Tue May 25 2004 - yuriy.kuznetsov@sun.com
- Added gnome-terminal-03-g11n-potfiles.diff
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-terminal-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - matt.keenan@sun.com
- Updated tarball to 2.6.1
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Fri Apr 02 2004 - ghee.teo@sun.com
- Updated tarball to 2.6.0
* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-terminal-l10n-po-1.0.tar.bz2
* Tue Mar 16 2004 - takao.fujiwara@sun.com
- Added gnome-terminal-01-g11n-schemas.diff to fix 4980332
- Added gnome-terminal-02-g11n-potfiles.diff
* Wed Feb 18 2004 - <matt.keenan@sun.com>
- Bump to 2.5.5
* Tue Dec 16 2003 - <glynn.foster@sun.com>
- Bump to 2.5.1
* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove the Sun Supported keyword, since we're removing 
  Extras now.
* Fri Oct 17 2003 - <ghee.teo@sun.com>
- Upgraded to 2.4.0 for Quicksilver build.
  removed patch  gnome-terminal-01-config-add-1l0n-help.diff
  and modified patch gnome-terminal-02-menu-entry.diff
  to make it gnome-terminal-01-menu-entry.diff
* Fri Sep 26 2003 Laszlo Peter <laca@sun.com>
- Intergate Sun docs
* Tue Aug 26 2003 Michael Twomey <michael.twomey@sun.com>
- Updated to 0.2 l10n docs tarball to fix seriesid issues.
- Added GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL to make install.
* Fri Aug 01 2003 - glynn.foster@sun.com
- Add supported menu category
* Fri Jul 25 2003 - niall.power@sun.com
- uses scrollkeeper for postinstall - add a dependency
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Wed May 14 2003 - ghee.teo@Sun.COM
- Created new spec file for gnome-terminal

