#
# spec file for package gnome-media
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include l10n.inc
Name:         gnome-media
Summary:      GNOME Multimedia
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
License:      LGPL v2, GPL v2, FDL 1.1
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:yippi date:2006-05-04 type:branding
Patch1:       gnome-media-01-menu-entries.diff
#owner:jerrytan date:2007-02-06 type:bug bugzilla:387400
Patch2:       gnome-media-02-removenewbutton.diff
#owner:yippi date:2009-02-09 type:feature bugzilla:571106
# This patch will go upstream, but a bug has not been filed because the
# gst-plugins-base-03-flags.diff patch needs to be released by the
# community before this patch can go upstream.  The gst-plugins-base 
# patch has gone upstream, but hasn't yet been released in a tarball.
Patch3:       gnome-media-03-flags.diff
#owner:yippi date:2009-02-09 type:feature
Patch4:       gnome-media-04-sliders-on-options.diff
#owner:yippi date:2009-02-09 type:feature
Patch5:       gnome-media-05-mergetabs.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_docdir}
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Prereq:       GConf

%define build_with_gnome_cd %{?_with_gnome_cd:1}%{?!_with_gnome_cd:0}

%define 	gstreamer_version 		0.8.1
%define 	gstreamer_devel_version 	0.8.1
%define 	gstreamer_plugins_version 	0.8.1
%define 	gstreamer_plugins_devel_version	0.8.1
%define		scrollkeeper_version		0.3.14
%define         libgnomeui_version              2.6.0
%define         nautilus_cd_burner_version      2.12.0

Requires: 	gstreamer >= %{gstreamer_version}
Requires: 	gstreamer-plugins >= %{gstreamer_plugins_version}
Requires:       libgnomeui >= %{libgnomeui_version}
BuildRequires:  gstreamer-devel >= %{gstreamer_devel_version}
BuildRequires: 	gstreamer-plugins-devel => %{gstreamer_plugins_devel_version}
BuildRequires:	scrollkeeper >= %{scrollkeeper_version}
BuildRequires:  libgnomeui-devel >= %{libgnomeui_version}
Requires:       nautilus-cd-burner >= %{nautilus_cd_burner_version}

%description
This package contains some multimedia programs for GNOME.

%prep
%setup -q
for po in po/*.po; do
  dos2unix -ascii $po $po
done
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif

%patch1 -p1
%patch2 -p1
%patch3 -p0
%patch4 -p1
%patch5 -p1

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
intltoolize --force --copy

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I ./m4
autoheader
automake -a -c -f
autoconf

CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}		\
	    --libexecdir=%{_libexecdir}	\
	    --sysconfdir=%{_sysconfdir} \
	    --disable-esdtest

make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1 
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL 

chmod -R a+rX $RPM_BUILD_ROOT%{_datadir}/gnome/help

#Clean up unpackaged files
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="CDDB-Slave2.schemas gnome-audio-profiles.schemas gnome-sound-recorder.schemas"
for S in $SCHEMAS; do
 gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%files
%defattr (-, root, root)
%{_bindir}/*
%{_libexecdir}/*
%{_libdir}/*.so.*
%{_libdir}/libgnome-media-profiles.so
%{_libdir}/bonobo/servers/*
%{_libdir}/pkgconfig/*
%{_libdir}/libglade/*
%{_includedir}/* 
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_datadir}/omf/gnome-media/*
%{_datadir}/gnome/help/*
%{_datadir}/idl/*
%{_datadir}/pixmaps/*
%{_sysconfdir}/gconf/schemas/*.schemas
%{_datadir}/applications/cddb-slave.desktop
%{_datadir}/applications/gnome-sound-recorder.desktop
%{_datadir}/applications/gnome-volume-control.desktop
%{_datadir}/applications/gstreamer-properties.desktop
%{_datadir}/applications/reclevel.desktop
%{_datadir}/applications/vumeter.desktop
%{_datadir}/gnome-media/*
%{_datadir}/gnome-sound-recorder/*
%{_datadir}/gstreamer-properties/*
%{_mandir}/man1/*
%{_mandir}/man5/*

%changelog
* Wed Mar 18 2009 - brian.cameron@sun.com
- Bump to 2.26.0.
* Fri Mar 06 2009 - brian.cameron@sun.com
- Bump to 2.25.92 and add patches gnome-media-04-head.diff, 
  gnome-media-05-flags.diff, and gnome-media-06-sliders-on-options.diff, and
  gnome-media-07-mergetabs.diff to support new OSS plugin.  Remove patch
  gnome-media-02-supportdevices.diff as it is no longer needed.
* Thu Jan 29 2009 - brian.cameron@sun.com
- Bump to 2.25.5.
* Tue Jan 20 2009 - brian.cameron@sun.com
- Bump to 2.25.1.  Remove upstream patch gnome-media-04-fixcrash.diff.
* Tue Jan 06 2008 - brian.cameron@sun.com
- Add patch gnome-media-04-fixcrash.diff to fix crashing issue.  Fixes doo
  bug #5677.
* Thu Sep 25 2008 - brian.cameron@sun.com
- Bump to 2.24.0.1.  Remove upstream patch gnome-media-04-fixmute.diff.
* Fri Aug 22 2008 - jedy.wang@sun.com
- merge 05-menu-entry into 01-menu-entries and fix category problem.
* Wed Sep 10 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.
* Mon Jul 14 2008 - jedy.wang@sun.com
- Add 06-desktop.diff.
* Tue Jun 10 2008 - brian.cameron@sun.com
- Remove gnome-media-02-disable-gnome-cd.diff since gnome-cd is now
  disabled by default.
* Thu Jun 05 2008 - brian.cameron@sun.com
- Add gnome-media-05-fixmute.diff patch which fixes the mute button so it
  works with SunAudio line-in and monitor.  Fixes bugzilla bug #537028.
* Tue Jun 03 2008 - brian.cameron@sun.com
- Remove upstream patch gnome-media-05-g11n-filename.diff.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Sun Mar 23 2008 - takao.fujiwara@sun.com
- Add gnome-media-05-g11n-filename.diff to fix crash with multibyte filenames
  on none UTF-8 locales. Fixes 6310908
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0. Remove upstream patch 05-profiles-edit.
* Mon Oct 22 2007 - brian.cameron@sun.com
- Fix bug #6609597 by adding patch gnome-media-05-profiles-edit.diff.  This
  fixes the problem where when you edit profiles in sound-juicer, the "Edit"
  button has no label.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Remove the code that removes Gstreamer Properties files as they are no longer
  installed.
* Tue Sep 18 2007 - damien.carbery@sun.com
- Bump to 2.20.0. Remove upstream patch, 05-i18n-ui.
* Wed Sep 05 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Thu Aug 16 2007 - takao.fujiwara@sun.com
- Add gnome-media-05-i18n-ui.diff to localize UI strings.
  Fixes 5095357 and 6553722
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - brian.cameron@sun.com
- Remove gnome-media-02-cddb-display.diff.  Patch no longer
  needed.
* Fri Feb 16 2007 - brian.cameron@sun.com
- Remove patch gnome-media-03-cdda.diff since it didn't fix the
  problem with Solaris device not being found by default.  Damien
  removed the useful bit of this patch when he updated to the
  latest version of gnome-media.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Wed Jan 24 2007 - brian.cameron@sun.com
- Change %with_cd option to %with_gnome_cd as per Laca's comments.
* Tue Jan 23 2007 - brian.cameron@sun.com
- Add %with_cd option so users can build with gnome-cd if desired.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Thu Jan 18 2007 - irene.huang@sun.com
- Remove patch -08-grecord-critical.diff for it's already in.
* Thu Jan 18 2007 - irene.huang@sun.com
- Add patch -08-grecord-critical.diff.
* Mon Jan 08 2007 - damien.carbery@sun.com
- Bump to 2.17.2. Remove upstream patch, 04-fixfunc. Renumber remainder.
* Wed Dec 20 2006 - brian.cameron@sun.com
- Remove unnecessary linguas patch.
* Wed Dec 20 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Tue Sep 05 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Thu Jun 29 2006 - brian.cameron@sun.com
- This patch makes gnome-volume-control support the same devices
  that sdtaudiocontrol supports.  It is a known bug that GStreamer
  mixer plugins do not allow you to set flags.  At some point
  when these flags can be set via a mixer plugin interface, so
  then we should use that interface rather than hacking the 
  mixer GUI directly.
* Wed Jun 21 2006 - brian.cameron@sun.com
- Bump to 2.14.2 and add patch to fix LINGUAS issue.
* Fri May 05 2006 - glynn.foster@sun.com
- Remove the silly window title patch, and replace with a patch
  that removes stuff from the menus according to the spec.
* Tue Mar 28 2006 - brian.cameron@sun.com
- Add patch 5 to no longer build gnome-cd, now using sound-juicer.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.93.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Fri Jan 20 2006 - brian.cameron@sun.com
- Add patch 4 so that 2.13.7 compiles.
* Fri Jan 20 2006 - damien.carbery@sun.com
- Bump to 2.13.7.
* Tue Nov 29 2005 - laca.com
- remove javahelp stuff
* Thu Sep 22 2005 - brian.cameron@sun.com
- Add back gnome-media-03-cdda.diff and remove patch that causes
  gnome-cd to not build.
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.91.
* Tue Jul 12 2005 - balamurali.viswanathan@wipro.com
- Don't build gnome-cd
* Tue Jun 21 2005 - matt.keenan@wipro.com
- Remove capplets from %files to build
* Thu Jun 16 2005 - matt.keenan@wipro.com
- Bump l10n tarballs
* Tue May 17 2005 - balamurali.viswanathan@wipro.com
- Bump to 2.10.2
* Fri May 13 2005 - brian.cameron@sun.com
- Bump to 2.10 and add -I ./m4 to aclocal flags since it is needed.
* Fri Apr 22 2005 - archana.shah@wipro.com
- Modified patch gnome-media-22-play-not-working.diff.
  Fixes bug #6185195
* Thu Mar 03 2005 - archana.shah@wipro.com
- Add patch gnome-media-22-play-not-working.diff. Handle EBUSY error.
  Fixes bug #6185195
* Mon Feb 21 2005 - balamurali.viswanathan@wipro.com
- Add patch gnome-media-21-lossless-wav.diff, use wavenc instead of flacenc.
  Fixes bug #6227666
* Mon Feb 07 2005 - takao.fujiwara@sun.com
- Removed gnome-media-01-g11n-potfiles.diff and
  gnome-media-17-g11n-potfiles.diff
  Use l10n-configure.sh
- Renamed *.diff
- Updated gnome-media-12-g11n-schemas.diff to avoid the warning during 
  the installation. Fixing bug 6226060
- Added gnome-media-20-g11n-i18n-ui.diff to localize the default filename.
  Fixing bug 6217696
* Fri Jan 28 2005 - Matt.keenan@sun.com
- #6222302 - Remove Gstreamer Properties from yelp
* Thu Jan 27 2005 - balamurali.viswanathan@wipro.com
- Add patch gnome-media-21-gstreamer-prop-xml.diff to fix xmllint error
  Fixes bug #6218084
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Wed Jan 05 2005 - balamurali.viswanathan@wipro.com
- Add patch gnome-media-20-enable-pause.diff to set the sensitivity of previous
  button correctly.  Solves bug #5053909
* Wed Dec 22 2004 - balamurali.viswanathan@wipro.com
- Add patch gnome-media-19-stop-on-quit.diff to stop playing when gnome-cd quits
  Solves bug #6210011
* Tue Nov 23 2004 - balamurali.viswanathan@wipro.com
- Modify patch gnome-media-14-remove-unusable-cache-entry.diff to fix 
  bug #6195969
* Wed Nov 09 2004 - archana.shah@wipro.com
- Added gnome-media-18-prompt-on-overwrite.diff so that it asks before
  overwriting any existing file.
  Patch taken from bugzilla. Fixes bug# 6186579
* Thu Nov 04 2004 - ciaran.mcdermott@sun.com
- Added gnome-media-17-g11n-potfiles.diff to update POTFILES.in
* Wed Nov 03 2004 - balamurali.viswanathan@wipro.com
- Added patch gnome-media-16-cddb-display.diff. Fixes bug#6179826
* Fri Oct 29 2004 - arvind.samptur@wipro.com
- Patch from Archana to fix saving files in
  gnome-sound-recorder. Fixes #6184521
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gnome-audio-profiles-properties.1, gnome-volume-control.1,
  gstreamer-properties.1, vumeter.1, gst-std-options.5 man pages
* Fri Oct 12 2004 - balamurali.viswanathan@wipro.com
- Modify patch gnome-media-12-play-pipeline.diff to fix bug #6176869
* Fri Oct 08 2004 - kaushal.kumar@wipro.com
- Added patch gnome-media-14-remove-unusable-cache-entry.diff to 
  remove the cache entry once it is stale. Fixed a leak, etc.
  Fixes bug #5089229.
* Tue Oct 05 2004 - takao.fujiwara@sun.com
- Removed gnome-media-14-g11n-i18n-ui.diff by community's comment.
  Bugzilla 154054
* Thu Sep 30 2004 - takao.fujiwara@sun.com
- Add gnome-media-14-g11n-i18n-ui.diff to fix bug 5108713
* Tue Sep 28 2004 - ciaran.mcdermott@sun.com
- Add patch gnome-media-13-g11n-schemas-fix.diff for bug #5057074
* Fri Sep 24 2004 - balamurali.viswanathan@wipro.com
- Add patch gnome-media-12-play-pipeline.diff for bug #5089100
* Wed Sep 15 2004 - balamurali.viswanathan@wipro.com
- Add patch gnome-media-11-enable-lineout.diff to enable lineout 
* Thu Sep 02 2004 - balamurali.viswanathan@wipro.com
- Remove patch gnome-media-10-disable-solaris-record.diff to enable record 
  button is Solaris. Since now we have source element for Solaris
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Added l10n help contents with patch
* Fri Aug 20 2004 - damien.carbery@sun.com
- Integrated updated docs tarball from breda.mccolgan@sun.com
* Sun Aug 16 2004  shirley.woo@sun.com
- change .../gnome-cd/*/*.xml permissions to 0644 for Solaris integration error
- change .../gnome-sound-recorder/*/*.xml permissions to 0644 for Solaris
  integration error
* Thu Aug 05 2004 - damien.carbery@sun.com
- Integrated docs 0.5 tarball from breda.mccoglan@sun.com
* Fri Jul 30 2004 - brian.cameron@sun.com
- Added patch 10 to disable the record button on Solaris.
* Fri Jul 23 2004 - balamurali.viswanathan@wipro.com
- Patch to make gnome-cd play in machines where there is no audio cable.
  Fixes bug #5061178
* Tue Jul 13 2004 - niall.power@sun.com
- Ported to rpm4 and updated dependency versions
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-media-l10n-po-1.2.tar.bz2
* Wed Jul  7 2004 - takao.fujiwara@sun.com
- Add gnome-media-08-g11n-configure.diff to install .mo into _datadir/locale.
  bugzilla 145087.
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Mon Jun 15 2004 - brian.cameron@sun.com
- Bumping to 2.6.1 made patch gnome-media-04-add-gst-cflags-ldflags.diff
  unnecessary, so removed.  This fixed bug 5061791.
* Fri Jun 11 2004 - damien.carbery@sun.com
- Integrated docs 0.4 tarball from breda.mccoglan@sun.com
* Wed Jun 09 2004 - balamurali.viswanathan@wipro.com
- Added patch 08, to set the audio port, so that the user need not set it
  through sdtaudicontrol whenever he wants to use gnome-cd
* Tue Jun 8 2004 - rich.burridge@sun.com
- Added patch 07, so that gnome-cd doesn't crash when a CD is reinserted on
  a Solaris x86 system. Fix is fine for Linux as well. Fixes bugtraq bug
  #5057711
* Fri May 28 2004 - brian.cameron@sun.com
- Added patch 06, so that gnome-sound-recorder works for most formats
  on Solaris.  This is needed due to a limitation in esdsink (default 
  on Solaris).  osssink (default on Linux) can handle all rates/formats,
  but esdsink can not.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-media-l10n-po-1.1.tar.bz2
* Fri May 07 2004 - brian.cameron@sun.com
- Add --disable-esdtest since this fails on Solaris due to the
  way we are building gnome-media and configure picks up the
  gstreamer *.la files from pkg-config, which can't be used by
  configure.
* Fri May 07 2004 - matt.keenan@sun.com
- Bump to 2.6.1
* Tue Apr 27 2004 - kaushal.kumar@wipro.com
- Added gnome-media-05-cddb-help-filename-update.diff to fix the help 
  for cddb-slave2-properties dialog.
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 01 2004 - matt.keenan@sun.com
- javahelp conversion
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-media-l10n-po-1.0.tar.bz2
* Wed Mar 24 2004 - <glynn.foster@sun.com>
- Bump to 2.6.0, and remove record scheduler, 
  grecord configure, audio schemas, gnome volume 
  desktop, gst mixer array and grecord prompt
  overwrite [needs to be rewritten] patches.
* Fri Mar 05 2004 - <niall.power@sun.com>
- pass in ACLOCAL_FLAGS to aclocal
* Wed Mar 03 2004 - <laca@sun.com>
- Add libgnomeui dependency
* Fri Feb 13 2004 - <matt.keenan@sun.com>
- Patch 08, patch 09
* Wed Feb 11 2004 - <matt.keenan@sun.com>
- Bump to 2.5.2, l10n to 0.7, docs 0.2
  Re-apply patchs 01->05
  Remove original patch 06
  Add new patch 06 to build gnome-sound-recorder
* Wed Dec 17 2003 - <glynn.foster@sun.com>
- Bump to 2.5.1
* Fri Oct 31 2003 - <glynn.foster@sun.com>
- Remove and rename patches to remove the Sun Settings 
  desktop keyword, since we're killing Extras menu.
* Mon Oct 20 2003 - <ghee.teo@sun.com>
- Forward port fix to #4880305 from wipro for QS.
  patch: gnome-media-07-fix-saving-zero-bytes-data.diff
* Mon Oct 13 2003 - <niall.power@sun.com>
- updated to version 2.4.0
- Removed gnome-media-01-window-icon.diff,
  gnome-media-07-gnome-cd-notification.diff,
  gnome-media-08-recorder-gst-state.diff - all merged upstream
* Fri Sep 26 2003 - <laca@sun.com>
- integrate Sun docs
* Tue Sep 23 2003 - <niall.power@sun.com>
- add patch from Balamurali.Viswanathan@wipro.com.
  Fixes BT# 4882371. gnome-media-08-recorder-gst-state.diff
* Fri Sep 19 2003 - <niall.power@sun.com>
- add patch from Kaushal.Kumar@wipro.com. Fixes BT#4913405
  gnome-media-07-gnome-cd-notification.diff
- add patch nautilus-media-06-record-scheduler.diff.
  Fixes BT# 4904323
* Thu Aug 14 2003 - <laca@sun.com>
- remove lib*.so, *.a, *.la
* Thu Aug 07 2003 - <niall.power@sun.com>
- post install uses scrollkeeper so make it a dependency
* Wed Aug 06 2003 - <glynn.foster@sun.com>
- Prompt before you overwrite a filename.
* Tue Aug 05 2003 - <glynn.foster@sun.com>
- New tarball, bump version, reset release.
* Fri Aug 01 2003 - <glynn.foster@sun.com>
- Add supported menu categories
* Tue Jul 21 2003 - <glynn.foster@sun.com>
- New mixer icon
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Wed May 14 2003 - Matt.Keenan@sun.com
- Initial Sun Release

