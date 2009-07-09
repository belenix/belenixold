#
# spec file for package metacity
#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include l10n.inc
Name:         metacity
License:      GPL
Group:        System/GUI/GNOME
Version:      2.26.0
Release:      1
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Window Manager
Source:       http://ftp.gnome.org/pub/GNOME/sources/metacity/2.26/metacity-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
#owner:erwannc date:2000-00-00 type:branding
Patch1:       metacity-01-default-theme.diff
%if %option_with_indiana_branding
#owner:jedy date:2008-09-05 type:branding
Patch2:       metacity-02-shortcut-indiana.diff
%endif
%if %option_with_sun_branding
#owner:jedy date:2008-09-05 type:branding
Patch3:       metacity-03-shortcut.diff
%endif
#owner:erwannc date:2004-10-06 type:bug bugster:5101706
Patch4:       metacity-04-branding-hack.diff
#owner:erwannc date:2006-11-02 type:feature bugster:6393724
Patch5:       metacity-05-trusted-extensions.diff
#owner:bewitche date:2008-05-23 type:bug bugster:6676458 bugzilla:156543
Patch6:       metacity-06-wireframe.diff
#owner:erwannc date:2008-06-02 type:feature bugster:0000000
Patch7:       metacity-07-remove-xopen-source-posix.diff

URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define intltool_version 0.30
%define GConf_version 2.6.1
%define pkgconfig_version 0.15.0
%define libglade_version 2.3.6

Requires: GConf >= %{GConf_version}
Requires: libglade >= %{libglade_version}
BuildRequires: intltool >= %{intltool_version}
BuildRequires: pkgconfig >= %{pkgconfig_version}
BuildRequires: GConf >= %{GConf_version}
BuildRequires: libglade >= %{libglade_version}

%description
Metacity is the window manager for the GNOME Desktop.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%if %option_with_indiana_branding
%patch2 -p1
%endif
%if %option_with_sun_branding
%patch3 -p1
%endif
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1

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

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
# Note, you need to install SFElibcm (from spec-files-extra) and 
# add --enable-compositor to the configure call to use metacity
# with compositing mode.  Note SFElibcm requires Xorg 7.1 
# Xcomposite library.
#
CFLAGS="$RPM_OPT_FLAGS -Icore -Iui -lgthread-2.0 "	\
./configure --prefix=%{_prefix}		\
	    --mandir=%{_mandir}		\
            --libexecdir=%{_libexecdir} \
	    --sysconfdir=%{_sysconfdir} 
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la
                                                                                                                                                             
%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="metacity.schemas"
for S in $SCHEMAS; do
	gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, root)
%{_bindir}/*
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_sysconfdir}/gconf/schemas/metacity.schemas
%{_libexecdir}/*
%{_libdir}/*.so*
%{_libdir}/pkgconfig/*.pc
%{_includedir}/metacity-1/metacity-private
%{_datadir}/gnome/wm-properties/metacity.desktop
%{_datadir}/metacity
%{_datadir}/themes/*/metacity-1/*
%{_datadir}/control-center/keybindings/*
%{_mandir}/man1/*

%changelog
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Mon Feb 16 2009 - dave.lin@sun.com
- Bump to 2.25.144
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.34
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.21
* Fri Nov 11 2008 - jedy.wang@sun.com
- Remove 04-sunpowerswitch-key.diff, 06-logout-shortcut.diff and reorder
  the others.
* Mon Oct 27 2008 - brian.cameron@sun.com
- Add patch metacity-11-fixcrash.diff to fix a crashing issue noticed
  when using metacity with the new GDM 2.24.
* Sat Sep 27 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Wed Sep 10 2008 - jedy.wang@sun.com
- Remove 11-font.diff.
* Fri Sep 05 2008 - jedy.wang@sun.com
- Fix broken link.
- Merge 02-ctrl-esc-mod4-r.diff with 09-enable-sun-keys-Open-Front.dif
  into one patch and rename it to 02-shortcut.diff.
- New patch 02-shortcut-indiana.diff.
- Reorder patches.
* Tue Sep 02 2008 - christian.kelly@sun.com
- Bump to 2.25.1.
- Rework patches/metacity-08-trusted-extensions.diff.
* Fri Aug 22 2008 - jedy.wang@sun.com
- Remove option_with_indiana_branding.
  Rename opensolaris-branding.diff to font.diff.
  Fix download link.
* Tue Aug 19 2008 - dave.lin@sun.com
- Bump to 2.25.0
- Update the patch metacity-08-trusted-extensions.diff
* Mon Aug 18 2008 - jedy.wang@sun.com
- Add 12-opensolaris-branding.diff.
* Mon Jul 14 2008 - christian.kelly@sun.com
- Bump to 2.23.55.
* Fri Jul 11 2008 - chris.wang@sun.com
- Update orange patch 10 status
* Sat Jun 21 2008 - patrick.ale@gmail.com
- Change source download location to 2.23 directory
* Mon Jun 02 2008 - erwann.chenede@sun.com
- Bump to 2.23.21. Remove upstream patches, 10-lame-client-crash, 14-wireframe,
  11-iconic.diff. Add 11-remove-xopen-source-posix. 
* Fri May 23 2008 - chris.wang@sun.com
- add patch metacity-14-wireframe.diff to fixed bug 6676458 with regular size
  window maximize it and then minimize it and a wire frame will appear.  
* Tue May 20 2008 - stephen.browne@sun.com
- remove conditional build of tjds patch
* Wed May 07 2008 - simon.zheng@sun.com
- Rework 04-sunpowerswitch-key.diff to use gpm interface.
* Wed Apr 30 2008 - chris.wang@sun.com
- Add patch metacity-13-fail-windowattr.diff fix the bugster bug 6661472
  Metacity dumps core with an assertion failed
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Thu Mar 06 2008 - padraig.obriain@sun.com
- Add metacity-11-iconic.diff
* Thu Feb 28 2008 - damien.carbery@sun.com
- Bump to 2.21.21.
* Tue Feb 19 2008 - damien.carbery@sun.com
- Add '-Icore -Iui' to CFLAGS so that TJDS changes can build.
* Fri Feb 15 2008 - damien.carbery@sun.com
- Remove patch 11-src-includes. The TJDS patch needs to be reworked. Disable
  TJDS patch for the moment so that module builds okay.
* Wed Feb 13 2008 - damien.carbery@sun.com
- Bump to 2.21.13.
* Tue Feb 05 2008 - damien.carbery@sun.com
- Add patch 11-src-includes to get module to build after source tree reorg.
* Mon Feb 04 2008 - damien.carbery@sun.com
- Bump to 2.21.8.
* Thu Jan 03 2008 - damien.carbery@sun.com
- Bump to 2.21.5. Comment out patch8 and patch9 to get it to build.
* Tue Dec 18 2007 - damien.carbery@sun.com
- Bump to 2.21.3.
* Mon Nov 12 2007 - damien.carbery@sun.com
- Bump to 2.21.1.
* Fri Sep 28 2007 - laca@sun.com
- disable tjds patch when tjds support is not requested
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Tue Aug 07 2007 - damien.carbery@sun.com
- Bump to 2.19.55.
* Tue Jul 24 2007 - damien.carbery@sun.com
- Bump to 2.19.34.
* Fri Jun 22 2007 - damien.carbery@sun.com
- Unbump to 2.19.8 because .13 and .21 tarballs have linker error. Readd patch
  XX-empty-struct (fixes 397296).
* Mon Jun 18 2007 - damien.carbery@sun.com
- Bump to 2.19.21. Remove upstream patches, 09-empty-struct and 
  11-func-declaration-mismatch.
* Mon Jun 11 2007 - damien.carbery@sun.com
- Bump to 2.19.13. Add patch, 12-func-declaration-mismatch, to fix bugzilla
  446535.
* Mon May 14 2007 - erwann.chenede@sun.com
- Bump to 2.19.5
- removed a patch 
- added dir in %files
* Thu Apr 05 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.8.
* Thu Jan 25 2007 - takao.fujiwara@sun.com
- Added l10n tarball for metacity-xx-trusted-extensions.diff.
* Wed Jan 17 2007 - damien.carbery@sun.com
- Bump to 2.17.5.
* Fri Dec 22 2006 - takao.fujiwara@sun.com
- Updated metacity-10-trusted-extensions.diff. Fixes 6468212.
* Mon Dec 11 2006 - damien.carbery@sun.com
- Bump to 2.17.3.
* Thu Nov 23 2006 - damien.carbery@sun.com
- Bump to 2.17.2. Remove upstream patch, 13-terminal-strict-focus. Comment out 
  patch 9 as it needs rework.
* Sat 28 Oct 2006 - glynn.foster@sun.com
- Commit patch to preserve strict focus mode with terminals
  and keep a few kernel hackers on our side. Bugzilla #361054.
* Tue Oct 03 2006 - damien.carbery@sun.com
- Bump to 2.16.3.
* Wed Sep 27 2006 - brian.cameron@sun.com
- Add patch metacity-12-composite.diff so that if pkg-config
  finds cm.pc on the system, that it will build with 
  composite support. 
* Tue Sep 26 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.21.
* Mon Jul 24 2006 - damien.carbery@sun.com
- Bump to 2.15.13.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.14.5.
* Tue Apr 18 2006 - damien.carbery@sun.com
- Bump to 2.14.3.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.2.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.144.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 2.13.89.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Bump to 2.13.55.
* Sat Jan 21 2006 - damien.carbery@sun.com
- Bump to 2.13.34
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.21
* Sun Jan 15 2006 - damien.carbery@sun.com
- Bump to 2.13.13
* Mon Jan 09 2006 - damien.carbery@sun.com
- Add patch, pretty-function, to use a Gnome define instead of a pragma not
  available in forte. Bugzilla 326281.
- Call intltoolize to process intltool-update/merge.
* Wed Jan 04 2006 - damien.carbery@sun.com
- Remove obsolete patch, 08-constrain-window.
* Tue Dec 20 2005 - dermot.mccluskey@sun.com
- Bump to 2.13.5
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1
* Sat Sep 17 2005 - glynn.foster@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.3.
* Tue Aug 16 2005 - damien.carbery@sun.com
- Bump to 2.11.2.
* Wed Aug 03 2005 - laca@sun.com
- remove upstream patch splash-layer.diff
* Fri Jul 01 2005 - matt.keenan@sun.com
- Add patch -09-pkgconfig.diff to add needed libs
* Thu May 19 2005 - brian.cameron@sun.com
- Fix patch so it uses -p1 instead of -p0 since Solaris is less
  forgiving than Linux.  Remove patch 4 since it breaks the build.
* Tue May 17 2005 - arvind.samptur@wipro.com
-  Adding patch to fix splash screens not to be
   on top of all windows all the time Fixes #6268588
* Wed Feb 16 2005 - leena.gunda@wipro.com
- Added metacity-11-constrain-window.diff to constrain windows within 
  the strut area when shown for the first time. Fixes bug #6182510.
* Fri Feb 11 2005 - srirama.sharma@wipro.com
- Added metacity-10-window-title.diff to enable user to edit 
  window title using font capplet. Fixes bug #6227065.
* Thu Jan 20 2005 - leena.gunda@wipro.com
- Added metacity-09-wireframe-double-click.diff to restore window on
  double-clicking the title-bar to unmaximize. Fixes bug 6204338.
* Tue Jan 11 2005 - vinay.mandyakoppal@wipro.com
- Modified metacity-02-ctrl-esc-mod4-r.diff to map 'show desktop' to <mod4>+d
  Fixes bug #5028221.
* Mon Jan 03 2005 - arvind.samptur@wipro.comm
- Add patch to disable wireframe feature when
  accessiblity is on.
* Wed Nov 24 2004 - leena.gunda@wipro.com
- Updated metacity-04-sunpowerswitch-key.diff to fix stopper bug #5104104.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add metacity-message.1, metacity-window-demo.1 man pages
* Mon Oct 11 2004 - leena.gunda@wipro.com
- Updated metacity-04-sunpowerswitch-key.diff to check if Xserver is local
  for GDM also. Fixes bug #5107206.
* Wed Oct 06 2004 - vinay.mandyakoppal@wipro.com
- Added metacity-07-logout-shortcut.diff Patch to implement an
  "apps/metacity/global_keybindings/logout" gconf key and
  its functionality. Fixes bug #5101706.
* Fri Oct 01 2004 - arvind.samptur@wipro.com
- Add the window_raise_on_frame_only key under sun-extenstions
* Sat Sep 11 2004 - laca@sun.com
- Move Solaris specific LDFLAGS to the Solaris spec file
* Fri Sep 10 2004 - damien.carbery@sun.com
- Set LDFLAGS so Xrandr and Xrender can be found.
* Mon Aug 16 2004 - bill.haneman@sun.com
- Added patch metacity-05-bigstruts.diff for bugzilla #144126.
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to metacity-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to metacity-l10n-po-1.1.tar.bz2
* Wed May 12 2004 - leena.gunda@wipro.com
- Do aclocal, autoheader, autoconf and automake before doing a configure.
* Fri Apr 30 2004 - leena.gunda@wipro.com
- Added patch metacity-04-sunpowerswitch-key.diff to bind SunPowerSwitch
  key to gnome-sys-suspend for Solaris.
* Wed Apr 07 2004 - arvind.samptur@wipro.com
- Updated to 2.8.0
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to metacity-l10n-po-1.0.tar.bz2
* Tue Feb 24 2004 - <glynn.foster@sun.com> 2.7.0-1
- Update to 2.7.0
* Thu Feb 12 2004 - <niall.power@sun.com>
- add "-p0" strip argument to patch commands
* Tue Dec 16 2003 - <glynn.foster@sun.com> 2.6.3-1
- Update to 2.6.3
* Thu Oct 16 2003 - <markmc@sun.com> 2.6.2-1
- Update to 2.6.2
* Thu Oct 09 2003 - <markmc@sun.com> 2.6.1-1
- Update to 2.6.1
- Remove panel keybindings patches - they're in 2.6.x
* Fri Aug 01 2003 - <markmc@sun.com> 2.4.55-1
- Update to 2.4.55
* Thu Jul 31 2003 - <markmc@sun.com> 2.4.34-11
- Add patch to fix workspace names not retained after
  logging out.
* Thu Jul 17 2003 - <ghee.teo@sun.com>
- Combined the esc-ctrl patch with Mod4 (window) R key
  patch.
* Thu Jul 10 2003 - <michael.twomey@sun.com>
- Added .po tarball
* Thu Jul 03 2003 - <markmc@sun.com>
- redo default window border theme patch
* Wed Jul 02 2003 - <markmc@sun.com>
- add metacity-04-ctrl-escape.diff
* Wed Jul 02 2003 - <markmc@sun.com>
- new version of metacity-01-panel-keybindings.diff
* Fri May 30 2003 - <markmc@sun.com>
- Backport panel keybindings patches.
* Tue May 13 2003 - <Stephen.Browne@sun.com>
- initial release
