#
# spec file for package nautilus
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
%include l10n.inc

Name:         nautilus
License:      GPL
Group:        Productivity/File utilities
Version:      2.26.2
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      The GNOME Filemanager
URL:          http://www.gnome.org
Source:       http://ftp.gnome.org/pub/GNOME/sources/nautilus/2.26/nautilus-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
# NOTE: If the version is bumped the new tarball must be uploaded to the
#       Sun Download Center. Contact GNOME RE for assistance.
Source2:      http://dlc.sun.com/osol/jds/downloads/extras/nautilus-acl-icons-0.2.tar.bz2 
%if %build_l10n
Source3:      l10n-configure.sh
%endif
Source4:      restore.png
Source5:      restore-no.png
Source6:      restore-search.png
Source7:      camera.png
#owner:stephen date:2004-10-29 type:bug bugster:5105006,5070031 bugzilla:137282
Patch1:       nautilus-01-trash-only-home.diff
#owner:stephen date:2005-02-25 type:bug bugster:5011528
Patch2:       nautilus-02-desktop-cluttered-icons.diff
#owner:stephen date:2005-05-07 type:bug bugster:6238031 bugzilla:170761
Patch3:       nautilus-03-ftp-rename.diff
#owner:stephen date:2004-11-10 type:bug bugster:6174222
Patch4:      nautilus-04-execute-shellscript.diff
#owner:stephen date:2005-06-17 type:branding
Patch5:      nautilus-05-context-menu.diff
#owner:stephen date:2005-05-20 type:feature bugster:6211279
Patch6:      nautilus-06-frame-buffer.diff
#owner:stephen date:2004-02-19 type:feature bugzilla:397715
Patch7:      nautilus-07-lockdown.diff
#owner:padraig date:2006-05-11 type:feature
Patch8:      nautilus-08-acl.diff
#owner:stephen date:2006-07-12 type:feature
Patch9:       nautilus-09-trusted-extensions.diff
#owner:padraig date:2007-11-23 type:feature bugster:6556913
Patch10:       nautilus-10-star-desktop.diff
#owner:padraig date:2008-05-02 type:bug bugster:6693915 bugzilla:530858
Patch11:       nautilus-11-update-bookmarks.diff
#owner:erwannc date:2008-08-28 type:feature bugster:6738643
Patch13:       nautilus-13-zfs-snapshot.diff
%if %option_with_sun_branding
#owner:gman date:2006-04-25 type:branding
Patch14:      nautilus-14-interface-changes.diff
%endif
%if %option_with_indiana_branding
#owner:gman date:2007-10-19 type:branding
Patch14:      nautilus-14-interface-changes-indiana.diff
%endif

BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/nautilus2
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define fam_version  2.6.10
%define glib2_version 2.4.0
%define pango_version 1.4.0
%define gtk2_version 2.4.0
%define libgnomeui_version 2.6.0
%define eel_version 2.6.1
%define gnome_icon_theme_version 1.2.0
%define libxml2_version 2.6.7
%define eog_version 2.6.1
%define gail_version 1.6.3
%define gnome_desktop_version 2.6.1
%define gnome_vfs_version 2.6.0
%define startup_notification_version 0.5
%define libgnomecups_version 0.1.6
%define gnome_cups_manager_version 0.17
%define scrollkeeper_version 0.3.14
%define libgnomeprint_version 2.6.0
%define libgnomeprintui_version 2.6.0
%define esound_version 0.2.27
%define gettext_version 0.14.0

Requires:	fam >= %{fam_version}
Requires:       gnome-vfs >= %{gnome_vfs_version}
Requires:       eel >= %{eel_version}
Requires:       gnome-icon-theme >= %{gnome_icon_theme_version}
Requires:       libgnomecups >= %{libgnomecups_version}
Requires:       libgnomeprint >= %{libgnomeprint_version}
Requires:       libgnomeprintui >= %{libgnomeprintui_version}

BuildRequires:  fam-devel >= %{fam_version}
BuildRequires:	scrollkeeper >= %{scrollkeeper_version}
BuildRequires:	glib2-devel >= %{glib2_version}
BuildRequires:	pango-devel >= %{pango_version}
BuildRequires:	gtk2-devel >= %{gtk2_version}
BuildRequires:	libgnomeui-devel >= %{libgnomeui_version}
BuildRequires:	libxml2-devel >= %{libxml2_version}
BuildRequires:  eel-devel >= %{eel_version}
BuildRequires:  gail-devel >= %{gail_version}
BuildRequires:  gnome-icon-theme >= %{gnome_icon_theme_version}
BuildRequires:  gnome-desktop-devel >= %{gnome_desktop_version}
BuildRequires:  gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires:  startup-notification-devel >= %{startup_notification_version}
BuildRequires:  librsvg >= 2.2.4
BuildRequires:  intltool >= 0.25
BuildRequires:  XFree86-devel >= 4.3.0
BuildRequires:  libgnomecups-devel >= %{libgnomecups_version}
BuildRequires:  libgnomeprint-devel >= %{libgnomeprint_version}
BuildRequires:  libgnomeprintui-devel >= %{libgnomeprintui_version}
BuildRequires:  esound-devel >= %{esound_version}
BuildRequires:  gettext >= %{gettext_version}

%description
This package contains Nautilus, the advanced filemanager for the GNOME platform.


%package devel
Summary:      Development package for Nautilus
Group:        Development/Libraries/GNOME
Requires:     %name = %version-%release

%description devel
This package contains all files needed to develop programs that use the features of the Nautilus filemanager.

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
%patch5 -p1
%patch6 -p1
%patch7 -p1
##%patch8 -p1 ## not porting this patch until gvfs acl code is ready.  
%patch9 -p1 
%patch10 -p1
%patch11 -p1
%patch13 -p1
%if %option_with_sun_branding
%patch14 -p1
%endif
%if %option_with_indiana_branding
%patch14 -p1
%endif

cp %SOURCE4 icons
cp %SOURCE5 icons
cp %SOURCE6 icons
cp %SOURCE7 icons

for po in po/*.po; do
  dos2unix -ascii $po $po
done

bzcat %SOURCE2 | tar xf -

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

# FIXME: remove most locale files as they break the build
# something weird going on here...
# the error message looks like this:
#: /var/tmp/SUNWgnome-file-mgr-2.13.3-build//etc/gconf/schemas/apps_nautilus_preferences.schemas:61: parser error : Input is not proper UTF-8, indicate encoding !
#: Bytes: 0xC8 0xED 0x20 0x61
#:          <long>Se est<C8><ED> activado, os ficheiros agochados ser<C8><ED>n amosados no xest
#:                      ^

LC_ALL=
LANG=
export LANG LC_ALL
libtoolize --force --copy
intltoolize --force --copy
gtkdocize

%if %build_l10n
bash -x %SOURCE3 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoheader
automake -a -c -f
autoconf
EXTRA_CORE_MODULES="gnome-vfs-2.0 libgnomeui-2.0" \
CFLAGS="$RPM_OPT_FLAGS" \
  ./configure \
	--prefix=%{_prefix} \
    	--datadir=%{_datadir}       \
	--sysconfdir=%{_sysconfdir} \
        --libexecdir=%{_libexecdir} \
	--disable-update-mimedb \
	--localstatedir=/var/lib

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 
make install DESTDIR=$RPM_BUILD_ROOT
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL

rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="apps_nautilus_preferences.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%doc AUTHORS COPYING ChangeLog NEWS README
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%{_datadir}/nautilus
%{_datadir}/mime/packages/*
%{_libdir}/*.so.*
%{_bindir}/*
%{_libdir}/bonobo/servers/Nautilus_shell.server
%{_sysconfdir}/gconf/schemas/*.schemas
%{_mandir}/man1/*

%files devel
%defattr(-,root,root)
%{_libdir}/*.so
%{_includedir}/nautilus
%{_libdir}/pkgconfig/*.pc

%changelog
* Wed Apr 15 2009 - dave.lin@sun.com
- Bump to 2.26.2
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.93
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
- Add patch 15-gtkdoc-rebase.diff to fix GTKDOC_REBASE issue.
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.4
* Wed Dec 24 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.1
* Tue Nov 25 2008 - dave.lin@sun.com
- Bump to 2.24.2
* Sun Nov 02 2008 - christian.kelly@sun.com
- Bump to 2.24.1.
- Sun Sep 28 2008 - patrick.ale@gmail.com
- Correct download URL
* Wed Sep 24 2008 - matt.keenan@sun.com
- Bump to 2.24.0
- Re-apply nautilus-07-lockdown.diff
- Remove nautilus-12-blank-cd.diff, applied upstream
* Fri Sep 05 2008 - jijun.yu@sun.com
- Add a patch.
* Tue Aug 05 2008 - damien.carbery@sun.com
- Bump to 2.23.6.1.
* Fri Jul 25 2008 - stephen.browne@sun.com
- Removed upstream patch 13
* Fri Jul 04 2008 - damien.carbery@sun.com
- Add patch 13-stat-header to include sys/stat.h to get module to build.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4. Remove upstream patch, 13-void-function.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Add patch, 13-void-function to fix bugzilla ??????, void function returns
  value, breaks build.
* Wed Jun 04 2008 - stephen.browne@sun.com
- Bump to 2.23.3 remove upstream patch 13 and port others
* Fri May 16 2008 - stephen.browne@sun.com
- remve conditional build of tx patch
* Tue May 06 2008 - padraig.obriain@sun.com
- Add patches/nautilus-13-redirect-cd-window.diff for 6680894
* Fri May 02 2008 - padraig.obriain@sun.com
- Add patches/nautilus-12-update-bookmarks.diff for 6693915
* Thu Apr 10 2008 - damien.carbery@sun.com
- Bump to 2.22.2. Comment out failing patches.
* Fri Apr 04 2008 - padraig.obriain@sun.com
- patches/nautilus-09-interface-changes.diff: Add back label and accelerator
  for Computer. Fixes 6683252.
* Fri Mar 21 2008 - chris.wang@sun.com
- patches/nautilus-09-interface-changes.diff: revised the patch to fix bug
  6663349 restarting nautilus generates garbage in $HOME. The cause of the
  bug is that the return type of g_file_new_for_path is GFile not char*.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Tue Feb 26 2008 - damien.carbery@sun.com
- Bump to 2.21.92.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Tue Jan 29 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 22 2008 - damien.carbery@sun.com
- Bump to 2.21.6.
* Thu Jan 17 2008 - damien.carbery@sun.com
- Bump to 2.21.5.
* Thu Jan 10 2008 - padraig.obriain@sun.com
- Rework patch 01, trash only home patch.
* Tue Jan 08 2008 - damien.carbery@sun.com
- Bump to 2.21.2.
* Tue Jan 08 2008 - padraig.obriain@sun.com
- Add back patch 10, the tsol patch.
* Mon Jan 07 2008 - padraig.obriain@sun.com
- Add back patch 09.
* Fri Jan 04 2008 - padraig.obriain@sun.com
- Remove nautilus-11-thumbnail-fix.diff as it is no longer needed. Rename
  nautilus-12-star-desktop.diff to nautilus-11-star-desktop.diff
- Add back patches 7, 10; I only reworked 7.
* Thu Jan 03 2008 - brian.cameron@sun.com
- Add back patch 3 and 4 after reworking them so they apply to new
  nautilus version.
* Sun Dec 30 2007 - damien.carbery@sun.com
- Bump to 2.21.1. Hack: Disable most patches to try to get it to build.
* Fri Nov 23 2007 - padraig.obriain@sun.com
- Add nautilus-12-star-desktop.diff to fix bug 6556913
* Wed Nov 07 2007 - padraig.obriain@sun.com
- Add nautilus-11-thumbnail-fix.diff to fix bug 6620330, bugzilla 483884
* Fri Nov 02 2007 - dave.lin@sun.com
- Fixed the problem with branding Patch9 definition
* Wed Oct 24 2007 - stephen.browne@sun.com
- swap trusted-extensions.diff and acl.diff 
* Fri Oct 19 2007 - laca@sun.com on behalf of Glynn Foster
- add separate Nevada and Indiana branding patches with corresponding
  build options.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.19.91.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90. Remove upstream patch, 11-trim-uninstaled.
* Wed Aug 01 2007 - damien.carbery@sun.com
- Add patch 11-trim-uninstaled to fix 462496.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Bump to 2.19.6. Remove upstream patch, 08-uninstalled-pc. Renumber rest.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Bump to 2.19.5.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.4.
* Wed Jun 06 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Tue May 15 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Tue Apr 10 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.1.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91. Remove upstream patch, 12-eject-crash.
* Sun Jan 28 2007 - laca@sun.com
- add %if %build_tjds guard around tjds patch so we can build without trusted
  jds support
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Thu Jan 18 2007 - alvaro.lopez@sun.com
- Added URL for the nautilus-acl-icons tarball.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Tue Nov 28 2006 - damien.carbery@sun.com
- Remove upstream patch, 14-desktop-icon-placement.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.3.
* Wed Nov 08 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
- remove upstream patches
* Tue Oct 31 2006 - padraig.obriain@sun.com
- Add nautilus-20-properties-relations.diff to fix bug 6458330, bugzilla 356124
* Fri Oct 06 2006 - padraig.obriain@sun.com
- Add nautilus-19-add-relations.diff to fix bug 6458338.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Fri Sep 15 2006 - matt.keenan@sun.com
- Bug : 6470306, remove patch-19, problem was actually within patch 
  11-frame-buffer.diff
* Thu Sep 14 2006 - matt.keenan@sun.com
- Bug : 6470306, metadata read fail causing crash
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.1.
* Tue Aug 22 2006 - damien.carbery@sun.com
- Bump to 2.15.92.
* Tue Aug 08 2006 - padraig.obriain@sun.com
- Delete nautilus-09-floppy.diff
  Rework nautilus-11-frame-buffer.diff
* Tue Aug 08 2006 - padraig.obriain@sun.com
- Bump to 2.15.91.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Wed Jul 20 2006 - dermot.mccluskey@sun.com
- Bump to 2.15.4.
  Remove patch #19
* Tue May 23 2006 - laca@sun.com
- remove linguas.diff: not needed.
* Thu May 11 2006 - alvaro.lopez@sun.com
- Added patch #18: ACL support
* Wed May 03 2006 - brian.cameron@sun.com
- Update LINGUAS file so all languages are on one line, becuase this is causing
  problems building with the latest intltool.
* Thu Apr 13 2006 - dermot.mccluskey@sun.com
- replace sed with dos2unix to work around ^M problem in SVN
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Wed Mar  1 2006 - laca@sun.com
- use sed instead of dos2unix for converting the po files, because dos2unix
  corrupts some UTF-8 strings
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Wed Jan 18 2006 - damien.carbery@sun.com
- Add intltoolize call.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Thu Jan 12 2006 - glynn.foster@sun.com
- Add patch to change to browser mode by default.
* Tue Jan 03 2006 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Mon Oct 17 2005 - glynn.foster@sun.com
- Add uninstalled pc file for nautilus
* Fri Oct 14 2005 - laca@sun.com
- add patch locale.h.diff to fix the build
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Fri Jun 17 2005 - dinoop.thomas@wipro.com
- Added patch nautilus-14-floppy.diff for bug #5078858.
  Added nautilus-15-context-menu.diff.
* Fri Jun 17 2005 - archana.shah@wipro.com
- Added patch nautilus-13-subfs.diff
  Patch taken for bug #6195964 and #6193864.
* Fri Jun 17 2005 - archana.shah@wipro.com
- Added patch nautilus-12-execute-shellscript.diff
  Patch taken for bug #6174222
* Thu Jun 02 2005 - brian.cameron@sun.com
- Cleaned up so it builds.
* Thu May 26 2005 - balamurali.viswanathan@wipro.com
- Move patch nautilus-01-lockdown.diff to nautilus-X-lockdown.diff:
* Thu May 26 2005 - balamurali.viswanathan@wipro.com
- Bump to 2.10.1
* Fri May 20 2005 - narayana.pattipati@wipro.com
- Added patch nautilus-47-frame-buffer.diff to fix problem of icons not
  appearing on the magnified screen while working with dummy frame buffer.
  The patch fixes one SUN specific a11y requirement. Its not accepted in
  community. Bugtraq bug#6211279
* Fri May 06 2005 - archana.shah@wipro.com
- Added nautilus-46-upgrade-icons-missing.diff to make nautilus draw the 
  staroffice and Desktop Overview icons for an old user when machine is
  upgraded from QS to cinnabar.
  Fixes bug# 6257246
* Wed May 04 2005 - vinay.mandyakoppal@wipro.com
- Added nautilus-45-security-warning.diff to avoid security warning on
  double click of StarOffice 7 template. Fixes bug #6262830.
* Mon May 02 2005 - vinay.mandyakoppal@wipro.com
- Added nautilus-44-ctrl-space-crash.diff to prevent nautilus from 
  crashing on press of Ctrl+space. Fixes bug #6261299.
* Mon Apr 25 2005 - dinoop.thomas@wipro.com
- Added nautilus-43-smb-domain-name.diff to allow domain name to be
  entered along with username in smb.
  Fixes bug #6247186
* Fri Apr 22 2005 - archana.shah@wipro.com
- Added  nautilus-42-trash-skip-copy.diff to fix a trash issue.
  Fixes bug #6243507
* Fri Apr 22 2005 - dinoop.thomas@wipro.com
- Added nautilus-41-anonymous-ftp-error.diff to launch the 
  appropriate error dialog when anonymous ftp is not supported.
  Fixes bug #6254481.
* Wed Apr 20 2005 - archana.shah@wipro.com
- Added nautilus-40-icon-view-crash.diff. Fixes bug #6234894 
* Thu Apr 07 2005 - dinoop.thomas@wipro.com
- Added nautilus-39-ftp-rename.diff to fix nautilus not allowing
  the opening or renaming of folders after the deletion of a 
  bookmarked folder. Fixes bug 6238031.
* Thu Mar 31 2005 - takao.fujiwara@sun.com
- Added nautilus-38-g11n-filename.diff to handle localized
  background filenames. Fixes bug 6247833
* Fri Feb 25 2005 - suresh.chandrasekharan@sun.com
- Added patch #37 nautilus-37-desktop-cluttered-icons.diff
  Fixes bug #5011528
* Fri Feb 22 2005 - alvaro.lopez@sun.com
- Removed "Obsoltes: epiphany" headers.
* Fri Feb 11 2005 - archana.shah@wipro.com
- Added patch #36 nautilus-36-max-zoom-level.diff to set the max zoom
  level correctly.
* Fri Feb 04 2005 - dinoop.thomas@wipro.com
- Added patch #35 nautilus-35-printer-mnemonics.diff
  Included mnemonics for some menu items in context menu for
  printer.Fixes bug #4917219.  
* Thu Feb 03 2005 - dinoop.thomas@wipro.com
- Added patch #33 nautilus-33-add-network-place-mnemonics.diff
  Changed the shortcut for connect button in Add Network Place.
* Fri Jan 21 2005 - alvaro.lopez@sun.com
- Added patch #32 nautilus-32-move-trash-dup.diff
  Fixes bug #6212062
* Mon Jan 17 2005 - vijaykumar.patwari@wipro.com
- Added patch #31 nautilus-31-bookmarks-fix.diff
  Fixes bookmarks crash.
* Fri Dec 24 2004 - vijaykumar.patwari@wipro.com
- Added patch #30 nautilus-30-unescape-filename-to-print.diff
  Fixes print not working with spaced filename.
* Wed Dec 22 2004 - suresh.chandrasekharan@sun.com
- Added patch #29 nautilus-29-nonlocalized-history-fix.diff
* Mon Dec 13 2004 - padraig.obriain@sun.com
- Added patch #28 to fix crash when accessibility is enabled.
* Fri Dec 10 2004 - niall.powre@sun.com
- Fixed brokenness in patch #21 (trash handling). Change operation
  to a standard move to work across filesystem boundaries.
* Mon Dec 06 2004 - Vinay.mandyakoppal@wipro.com
- Added patch #27 to prevent nautilus crash when we right click
  print on floppy icon and select print. Fixes bug #6200498.
* Wed Dec 01 2004 - Yong.Sun@Sun.COM
- Added patch #27 to integrate fsexam into nautilus context menu.
  And only applied in Linux.
* Wed Nov 23 2004 - alvaro.lopez@sun.com
- Patch #26 is only applied in Linux by the moment: so10 code freeze
  and problems with the prev. patch. This has to be fixed to keep only
  one source tree.
* Wed Nov 23 2004 - alvaro.lopez@sun.com
- Added patch 26 to fix some problems about Subfs. Fixes #6195964
* Wed Nov 10 2004 - brian.cameron@sun.com
- Added patch 25 to support formatting floppy disks on Solaris and to
  fix Nautilus so it properly unmounts floppy disks on Solaris.
* Wed Nov 10 2004 - archana.shah@wipro.com
- Added patch nautilus-24-execute-shellscripts.diff so that it throws up
  dialog asking whether to execute the file or open with come application
  for shell scripts.
* Tue Nov 09 2004 - vinay.mandyakoppal@wipro.com
- Added nautilus-23-click-cur-crash.diff to fixes crash when double click
  on .cur file. Fixes bug #6183952.
* Tue Nov 09 2004 - srirama.sharma@wipro.com
- Updated the patch nautilus-02-default-setup.diff to enable startup
  notification for Desktop Overview desktop file.
* Thu Nov 04 2004 - vinay.mandyakoppal@wipro.com
- Added patch nautilus-22-create-archive-work.diff to make right click
  create archive option function. Fixes bug #6186537.
* Fri Oct 29 2004 - narayana.pattipati@wipro.com
- Added patch nautilus-21-trash-only-home.diff to treat only user's 
  home directory as trash volume. Don't look at all the mount points 
  in the system for trash. Fix bugtraq bugs#5105006 and 5070031
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add nautilus-file-management-properties.1 man page
* Wed Oct 27 2004 - srirama.sharma@wipro.com
- Removed nautilus-21-desktop-startup-notification.diff as the patch
  should be rolled into the original nautilus-02-default-setup.diff patch. 
* Wed Oct 27 2004 - srirama.sharma@wipro.com
- Added nautilus-21-desktop-startup-notification.diff to enable 
  startup notification for Desktop Overview desktop file.
  Fixes the bugtraq bug#6180411.
* Mon Oct 18 2004 - alvaro.lopez@sun.com
- Added esound-devel and gettext dependencies
- "Source" entry updated
* Tue Aug 31 2004 - vinay.mandyakoppal@wipro.com
- Modified patch nautilus-18-add-network-place.diff to provide help
  innvocation.
* Mon Aug 30 2004 - takao.fujiwara@sun.com
- Updated nautilus-04-g11n-potfiles.diff
* Mon Aug 30 2004 - narayana.pattipati@wipro.com
- Added patch nautilus-19-computer-size-sort-crash.diff to fix nautilus
  crash when sort is done on size in computer view. Fixes bugtraq
  bug#5093170. Submitted the fix to bugzilla also. Bugzilla bug#151228
* Wed Aug 18 2004 - brian.cameron@sun.com
- removed --disable-gtk-doc since this isn't an option this module's
  configure takes.
* Thu Jul 22 2004 - narayana.pattipati@wipro.com
- Modified patch nautilus-08-printing.diff to hide Print menu item 
  in Solaris, as there is no CUPS support available. Fixes bugtraq
  bug#5076500
* Fri Jul 16 2004 - johan.steyn@sun.com
- Added patch 18 for Network Places
* Wed Jul 14 2004 - narayana.pattipati@wipro.com
- Added patch nautilus-17-add-nfs-mime.diff to add x-directory/nfs-mount 
  and x-directory/nfs-share mimes under supported mime types for 
  Icon and List views. Fixes bugtraq bug#5034725.
* Tue Jul 13 2004 - narayana.pattipati@wipro.com
- Updated patch nautilus-16-use-default-action-for-files.diff to fix
  issue with printers:/// location. Fixes bugtraq bug#5069536.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to nautilus-l10n-po-1.2.tar.bz2
* Thu Jul 08 2004 - stephen.browne@sun.com
- ported to rpm4/suse91
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 25 2004 - stephen.browne@sun.com
- Added patch nautilus-16-use-default-action-for-files to fix
  butraq bug: 5064649
* Fri Jun 25 2004 - narayana.pattipati@wipro.com
- Added patch nautilus-15-host-name-crash.diff to fix nautilus crash
  when it tries to display host name in an error message for Solaris.
  Fixes bugtraq bug:5067212
* Wed Jun 09 2004 - kaushal.kumar@wipro.com
- Add patch nautilus-14-help-contents-link.diff to fix the 
  Help->Contents.
* Mon May 31 2004 - padraig.obriain@sun.com
- Add patch nautilus-13-deselect.diff to backport fix for bugzilla
  bug #140827.
* Thu May 20 2004 - balamurali.viswanathan@wipro.com
- Reverting back the previous change. Moving #include <config.h> alone
  solves the problem
* Thu May 20 2004 - balamurali.viswanathan@wipro.com
- Modified nautilus-01-printers.diff, to define HAVE_LIBGNOMECUPSUI 
  using AC_DEFINE_UNQUOTED instead of AC_DEFINE. Fixes bug #5042415
* Thu May 13 2004 - narayana.pattipati@wipro.com
- Added patch nautilus-12-view-as-image.diff to fix nautilus crash
  in solaris while browsing to a location with image files.
  Fixes bugtraq bug#5043908.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to nautilus-l10n-po-1.1.tar.bz2
* Thu May 12 2004 - laszlo.kovacs@sun.com
- replaced jds-help.sh with jdshelp
* Thu May 06 2004 - laszlo.kovacs@sun.com
- add jds-help.sh to second patch
* Thu May 06 2004 - glynn.foster@sun.com
- auto*-jds it
* Wed May 05 2004 - glynn.foster@sun.com
- Sort out patches. Dump share/mount patch, rewrite print from
  nautilus patch
* Fri Apr 30 2004 - niall.power@sun.com
- patch #02 no longer requires "%ifos" evil
* Tue Apr 27 2004 - kaushal.kumar@wipro.com
- Added patch nautilus-15-preference-tabs-help-links.diff to fix 
  help links for 'Behavior' and 'List Columns' tabs.
* Mon Apr 26 2004 - ghee.teo@sun.com
- patched nautilus-13-printing.diff correctly for 2.6.1
* Mon Apr 26 2004 - glynn.foster@sun.com
- Updated tarball to 2.6.1
* Wed Apr 21 2004 - ghee.teo@sun.com
- Updated tarball to 2.6.0
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to nautilus-l10n-po-1.0.tar.bz2
* Fri Mar 26 2004 - laca@sun.com
- added --libexecdir to configure args
* Mon Mar 15 2004 - takao.fujiwara@sun.com
- Updated nautilus-03-this-computer-and-documents.diff to fix 4938606
- Replaced nautilus-06-potfiles-update.diff with nautilus-06-g11n-potfiles.diff
- Replaced nautilus-08-schemas-chinese.diff with nautilus-08-g11n-schemas.diff
* Tue Mar 09 2004 - <ghee.teo@sun.com>
- Updated nautilus-13-printing.diff to fix the incorrectly placed
  Print menu item in fm-directory-view-ui.xml. Should be under the Selection
  popup section instead of background section.
* Thu Mar 04 2004 - <narayana.pattipati@wipro.com>
- Updated the patch nautilus-07-mount-nfs-share-options.diff to 
  port fixes from quicksilver to cinnabar for bugs:4968376, 4966836, 
  4997201, 4981761, 4966812
* Tue Feb 24 2004 - ghee.teo@sun.com
- ported nautilus-13-printing.diff and make it lnux only ATM.
  since no cups supports by default on SOlaris.
* Fri Feb 20 2004 - stephen.browne@sun.com
- ported cd reaonly emblem patch
* Thu Feb 19 2004 - stephen.browne@sun.com
- more patch munging :)
* Thu Feb 19 2004 - stephen.browne@sun.com
- readded gestures patch
* Thu Feb 19 2004 - stephen.browne@sun.com
- SO Desktop icon patch from QS
* Thu Feb 19 2004 - stephen.browne@sun.com
- two more patches 9 + 10 ported
* Wed Feb 18 2004 - stephen.browne@sun.com
- patches ported up to #6 more to go :/
* Wed Feb 18 2004 - matt.keenan@sun.com
- added nautilus-list-view-ui.xml to %files
- added %{_includedir}/nautilus to %files devel
* Wed Feb 18 2004 - matt.keenan@sun.com
- commented out nautlius-tree-view elements from files as not built anymore
* Wed Feb 18 2004 - matt.keenan@sun.com
- Updated some versions
* Thu Feb 12 2004 - niall.power@sun.com
- added ACLOCAL_FLAGS to aclocal invocation
- only apply patch 02 (printers) on linux
* Mon Feb 09 2004 - laszlo.kovacs@sun.com
- ported Network Places patch
* Mon Jan 26 2004 - damien.donlon@sun.com
- uprevved the l10n source tarball to 0.6
* Tue Jan 13 2004 - niall.power@sun.com
- added a couple of new ui xml files from latest version
* Thu Jan 08 2004 - niall.power@sun.com
- New patch #14 to build against gtk+-2.3.x
- Minimum libgnomeui version of 2.5.2 required
- New version 2.5.4. Most patches are commented out just
  to make it build for now.
- comment out "%{sysconfdir}/gnome-vfs-2.0" from %files
  (was necessarey for the my-computer view patch)
* Mon Nov 02 2003 - glynn.foster@sun.com
- Add Applications to system:///
* Tue Oct 21 2003 - ghee.teo@sun.com
- Added nautilus-11-printing.diff patch to allow printing in nautilus.
  bug#4938054.
* Tue Oct 21 2003 - stephen.browne@sun.com
- Reactvated the patches and the printers rpm
* Mon Oct 13 2003 - niall.power@sun.com
- New version 2.4.0, temporarily commented out patches and
  branding and related post-install scripts.
* Fri Sep 05 2003 - michael.twomey@sun.com
- Add nautilus-12-schemas-chinese.diff to fix font sizes.
  Fixes bug 4915643.
* Tue Aug 19 2003 - Laszlo.Kovacs@sun.com
- added nautilus-11-network-places-crash-4904221.diff
* Thu Aug 14 2003 - <laca@sun.com>
- remove *.a, *.la
* Tue Aug 12 2003 - stephen.browne@sun.com
- cleaned up patches bug time,
  s/my computer/this comuter
  s/my documents/documents
* Wed Aug 06 2003 - stephen.browne@sun.com
- add toplevel help to desktop window
* Tue Aug 05 2003 - glynn.foster@sun.com
- add bmp previews
* Tue Aug 05 2003 - Laszlo.Kovacs@sun.com
- add nautilus-26-network-place-shortcut-name.diff
* Tue Aug 05 2003 - stephen.browne@sun.com
- fix crash when viewing remote files
* Tue Aug 05 2003 - Laszlo.Kovacs@sun.com
- added nautilus-24-network-dialog-tree-rewrite.diff
* Fri Aug 01 2003 - glynn.foster@sun.com
- Add menu entry categorization.
* Thu Jul 31 2003 - ghee.teo@sun.com
- Move the gnome-cups-manager more explict.
* Mon Jul 28 2003 - markmc@sun.com
- Make nautilus-mount use usermode
* Fri Jul 25 2003 - glynn.foster@sun.com
- Add quick-start location to the icon lookup.
* Thu Jul 24 2003 - stephen.browne@sun.com
- Fly away Home Come back My Documents
* Wed Jul 23 2003 - michael.twomey@sun.com
- Fix inconsistent Wastebasket naming in en_GB
* Mon Jul 21 2003 - glynn.foster@sun.com
- Let's give the file manager preferences a window icon
* Thu Jul 17 2003 - glynn.foster@sun.com
- Make sure that we install the file management preferences desktop
* Thu Jul 17 2003 - Laszlo.Kovacs@sun.com
- added nautilus-18-network-place-window-icon.diff
* Wed Jul 16 2003 - Laszlo.Kovacs@sun.com
- added nautilus-17-network-directory-file.diff
* Tue Jul 15 2003 - Ghee.Teo@Sun.Com
- Added printers desktop into control-center-2.0 for preferences:///
* Tue Jul 15 2003 - Laszlo.Kovacs@sun.com
- added nautilus-15-server-connect-async-dir-load.diff
* Sun Jul 14 2003 - erwann.chenede@sun.com
- added patch 14-mount-nfs-share-options.diff
* Thu Jul 10 2003 - stephen.browne@sun.com
- added patch nautilus-13
* Thu Jul 10 2003 - michael.twomey@sun.com
- Added .po tarball
* Wed Jul 09 2003 - Stephen.Browne@sun.com
- nautilus-12-priniters-icon.diff added
* Wed Jul 09 2003 - Stephen.Browne@sun.com
- nautilus-11-pref-defaults.diff added
* Thu Jul 03 2003 - Laszlo. Kovacs@sun.com
- nautilus-09-restore-desktop-item-save-method.diff added
* Thu Jul 03 2003 - Laszlo. Kovacs@sun.com
- added nautilus-08-add-network-place-label.diff
* Thu Jul 03 2003 - niall.power@sun.com
- version 2.2.4 - contains fix for long desktop icon labels getting left clipped
- added nautilus-07-cdburn.diff to integrate cd burning menu items etc.
* Tue Jul 01 2003 - niall.power@sun.com
- added my computer/system vfolder support
* Tue Jul 01 2003 - stephen.browne@sun.com
- added new sun branded throbber
* Fri Jun 27 2003 - ghee.teo@sun.com
- added the printers patch to show printers:// view in nautilus
* Tue Jun 10 2003 - Laszlo.Kovacs@sun.com
- added %{datadir}/gnome to %files
* Thu Jun 5 2003 - Laszlo Kovacs@sun.com
- fill user name in password dialog if passed in URI (nautilus-01-fill-user-in-passwd-dialog.diff)
* Thu May 01 2003 - Niall.Power@Sun.COM
- Initial Sun release
