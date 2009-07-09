#
# spec file for package gok
#
# Copyright (c) 2005 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
%include l10n.inc
Name:         gok
License:      LGPL
Group:        System/Libraries
Version:      2.26.0
Release:      1 
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME On-screen Keyboard
Source:       http://ftp.gnome.org/pub/GNOME/sources/gok/2.26/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
%ifos linux
#owner:padraig date:2004-08-17 type:branding
Patch1:       gok-01-linux-apps.diff
%else
#owner:padraig date:2004-08-17 type:branding
Patch1:       gok-01-solaris-apps.diff
%endif
URL:          http://developer.gnome.org/projects/gap/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:       %{_defaultdocdir}/%{name}
Autoreqprov:  on
Prereq:	      /sbin/ldconfig
Prereq:       GConf

%define gtk2_version 2.2.4
%define libgnomeui_version 2.4.0
%define atk_version 1.6.0
%define gail_version 1.5.7
%define at_spi_version 1.5.4
%define gnome_speech_version 0.3.5
%define intltool_version 0.31.3

BuildRequires: gtk2-devel >= %{gtk2_version}
BuildRequires: libgnomeui-devel >= %{libgnomeui_version}
BuildRequires: gail-devel >= %{gail_version}
BuildRequires: at-spi-devel >= %at_spi_version
BuildRequires: gnome-speech-devel >= %gnome_speech_version
BuildRequires: esound-devel
BuildRequires: intltool >= %intltool_version
Requires:      gtk2 >= %{gtk2_version}
Requires:      libgnomeui >= %{libgnomeui_version}
Requires:      gail >= %{gail_version}
Requires:      at-spi >= %at_spi_version
Requires:      gnome-speech >= %gnome_speech_version
Requires:      esound

%description
The GNOME On-screen Keyboard (GOK) is a dynamic on-screen keyboard for UNIX
and UNIX-like operating systems.  It features Direct Selection, Dwell
Selection, Automatic Scanning and Inverse Scanning access methods and
includes word completion.

%prep
%setup -q
m4 gok-with-references.schemas.m4 > gok-with-references.schemas.in
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
  # Hardcode 1 to overcome the 'dir exists' intermittent build error.
  CPUS=1
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f
CFLAGS="$RPM_OPT_FLAGS"			\
./configure --prefix=%{_prefix}			\
            --sysconfdir=%{_sysconfdir}		\
	    --libdir=%{_libdir}         	\
	    --bindir=%{_bindir}         	\
	    --mandir=%{_mandir}			\
	    --enable-xevie=no			\
            --disable-gtk-doc
make

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL


# Remove unwanted files
rm -rf $RPM_BUILD_ROOT%{_prefix}/var
rm -rf $RPM_BUILD_ROOT%{_prefix}/share/gtk-doc

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="gok.schemas"
for S in $SCHEMAS; do
        gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%files
%defattr(-,root,root)
%{_bindir}/gok
%{_bindir}/create-branching-keyboard
%{_libdir}/bonobo/servers/*.server
%{_libdir}/pkgconfig/*.pc
%{_datadir}/applications/*
%{_datadir}/gok
%{_datadir}/pixmaps/*
%{_datadir}/gnome/help/gok/*
%{_datadir}/locale/*/*/*
%{_datadir}/omf/gok/*.omf
%{_sysconfdir}/gconf/schemas/*.schemas
%{_mandir}/man1/*

%changelog
* Tue Mar 24 2009 - takao.fujiwara@sun.com
- Remove patch build-intltool.diff. Fixes bugzilla 542061.
* Tue Mar 17 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Tue Feb 17 2009 - dave.lin@sun.com
- Bump to 2.25.91
* Thu Feb 05 2009 - christian.kelly@sun.com
- Bump to 2.25.90.
* Thu Feb 05 2008 - li.yuan@sun.com
- Disable xevie. Bug #6801596.
* Thu Jan 22 2009 - li.yuan@sun.com
- Bump to 2.25.3.
* Thu Dec 11 2008 - li.yuan@sun.com
- Removed upstream patch gok-03-fix-restart.diff.
* Wed Dec 03 2008 - dave.lin@sun.com
- Bump to 2.25.2
* Thu Oct 09 2008 - ghee.teo@sun.com
- Removed patch gok-02-menu-entry.diff, no longer required.
* Mon Sep 29 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Mon Tue 08 2008 - patrick.ale@gmail.com
- Correct download URL
* Mon Sep 01 2008 - christian.kelly@sun.com
- Bump to 2.23.91.
* Fri Aug 22 2008 - jedy.wang@sun.com
- Rename dot-desktop.diff to menu-entry.diff.
* Tue Jul 15 2008 - christian.kelly@sun.com
- Bump to 1.4.0, rework gok-03-build-intltool.diff
* Tue Mar 04 2008 - takao.fujiwara@sun.com
- Add gok-03-build-intltool.diff to fix build failure caused by 
  bugzilla 487817.
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 1.3.7.
* Tue Oct 09 2007 - ghee.teo@sun.com
- Added patch gok-02-dot-desktop.diff
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 1.3.4.
* Thu Sep 06 2007 - damien.carbery@sun.com
- Bump to 1.3.3.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 1.3.2. Remove upstream patch 02-no-login-warn.
* Tue Jul 10 2007 - damien.carbery@sun.com
- Bump to 1.3.1.
* Mon May 28 2007 - damien.carbery@sun.com
- Remove upstream patches, 02-g11n-i18n-ui and 03-menu-comment. Rename rest.
* Mon May 28 2007 - damien.carbery@sun.com
- Bump to 1.2.5.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 1.2.3. Remove upstream patch gok-05-fixlogin.diff.
* Tue Feb 27 2007 - brian.cameron@sun.com
- Fix patch comments.
* Tue Feb 13 2007 - takao.fujiwara@sun.com
- Add l10n tarball.
* Fri Feb 09 2007 - brian.cameron@sun.com
- Fix patch 05-fixlogin so it applies with -p1
* Tue Jan 30 2007 - brian.cameron@sun.com
- Add patch, 05-fixlogin, to fix #383514.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 1.2.1.
* Fri Aug 25 2006 - damien.carbery@sun.com
- Bump to 1.2.0.
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 1.1.1.
* Mon Jul 03 2006 - damien.carbery@sun.com
- Redo patch 3 (gok.desktop.in) to *not* point at /usr/sfw as /usr is new 
  location. Rename patch (sfw-path to menu-comment) to reflect change. #6446011
* Tue May 23 2006 - laca@sun.com
- Bump to 1.0.10
* Thu Apr 27 2006 - damien.carbery@sun.com
- Bump to 1.0.8.
* Tue Mar 13 2006 - damien.carbery@sun.com
- Bump to 1.0.7.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Bump to 1.0.6.
- Remove upstream patch, dialog-container-add-children.
* Fri Dec 02 2005 - srirama.sharma@wipro.com
- Added gok-05-sfw-path.diff to use the absolute path of the executable 
  in the .desktop file as usr/sfw/bin should not be included in $PATH.
  Fixes bug #6345489.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Fri Jul 29 2005 - damien.carbery@sun.com
- Set CPUS to 1 on Solaris to fix intermittent 'dir exists' build error.
* Fri Jun 03 2005 - bill.haneman@sun.com
- Added gok-09-no-login-warn-6279448.diff, to fix stopper #6279448,
  which impaired accessible login.
* Fri May 20 2005 - bill.haneman@sun.com
- Added gok-05-dialog-container-add-children.diff, to fix issue with 
  StarOffice installer.
* Wed May 18 2005 - bill.haneman@sun.com
- Added gok-04-menu-doubleaction-patch.diff to fix StarOffice and 
  Java double activation of menus.
* Wed May 18 2005 - bill.haneman@sun.com
- Added gok-03-help-input-devices.diff to fix bugzilla #304524.
- Also fixes the missing corepointer-warning dialog problem discovered 
  with dwell mode, today.
* Mon May 16 2005 - bill.haneman@sun.com
- Revised gok-01-jdsapps.diff to fix bug #6264341.
* Fri May 06 2005 - bill.haneman@sun.com
- Revved to 1.0.5 - workaround for bug #6222814.
- Removed patch gok-03-primary-container.diff, now in tarball.
* Fri May 06 2005 - bill.haneman@sun.com
- Added patch gok-03-primary-container.diff, bugfix for #6238185.
* Thu Apr 28 2005 - bill.haneman@sun.com
- Revved to 1.0.4, bugfix for #6244239.
* Wed Mar 23 2005 - bill.haneman@sun.com
- Revved to 1.0.3, bugfixes for 
  and bugzilla #168093, #168405, #160726, #169761, #170347,
  #171231.
* Fri Mar 11 2005 - glynn.foster@sun.com
- Bring back Requires and BuildRequires.
* Wed Feb 16 2005 - kieran.colfer@sun.com
- Updating l10n tarball rev to latest version (1.12)
* Fri Feb 11 2005 - bill.haneman@sun.com
- Revved to 0.12.4, bugfixes for input device autodetection, 
  and final strings.
- Removed patch gok-09-toggle-button.diff, as it is no longer
  needed.
* Thu Feb 10 2005 - muktha.narayan@wipro.com
- Added gok-09-toggle-button.diff to enable gok search
  the children of ROLE_TOGGLE_BUTTON objects. Fixes bug #6223576.
* Thu Jan 27 2005 - damien.carbery@sun.com
- Finish build error fix: Source8 -> Source 2.
* Thu Jan 27 2005 - kazuhiko.maekawa@sun.com
- Fixed the build error from l10n tarball
* Wed Jan 26 2005 - damien.carbery@sun.com
- Update docs with Linux specific tarball from irene.ryan@sun.com.
* Wed Jan 19 2005 - bill.haneman@sun.com
- Revved to 0.12.1; fixes for bugs including 5109895.
- Removed patch5, as it is in the new tarball.
* Fri Jan 14 2005 - kazuhiko.maekawa@sun.com
- Updated l10n help tarball for cinnabar-linux
* Mon Jan 10 2005 - damien.carbery@sun.com
- Fix 6196403 - add gok-08-help-figs.diff to install 'figures' directory.
* Fri Jan 07 2005 - bill.haneman@sun.com
- Added %ifos solaris version of patch1, to add exec prefix to Mozilla.
- Fixes bug 6211656.
* Mon Dec 13 2004 - bill.haneman@sun.com
- Removed unwanted scrollkeeper and gtk-doc files.  Thanks Damien.
* Tue Dec 07 2004 - bill.haneman@sun.com
- Revved to 0.11.17.  
- Removed gok-03-toolbarfix.diff, as it is in the new tarball. 
- Includes fix for 6200712.
* Fri Nov 19 2004 - damien.carbery@sun.com
- add --bindir=%{_bindir} and --libdir=%{_libdir} to configure opts.
* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Added workaround fix for 6193354
* Fri Nov 05 2004 - bill.haneman@sun.com
- Revved to 0.11.16.  Fixes for 6185980, 6177484, 5087990, 6185984.
* Fri Nov 05 2004 - takao.fujiwara@sun.com
- Added intltoolize to get the latest intltool-update/merge
- Added gok-06-g11n-i18n-ui.diff to fix 6173646
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add create-branching-keyboard.1, gok.1 man pages
* Wed Oct 27 2004 - bill.haneman@sun.com
- Revved to gok-0.11.14.  Removed patches 3 and 4 (integrated).
  Contains fixes for bugs 5108516, 6179076, 5087916, 
  bugzilla bugs 154604, 154499, 156479, 156153, 155344, 155512.
* Tue Oct 26 2004 - damien.carbery@sun.com
- Integrate updated docs tarball from irene.ryan@sun.com.
* Wed Oct 13 2004 - padraig.obriain@sun.com
- Added patch gok-05-fix-strings.diff for bugzilla 155229.
* Wed Oct 13 2004 - takao.fujiwara@sun.com
- Added m4 in %prep to pre-generate .schemas.in
* Tue Oct 12 2004 - bill.haneman@sun.com
- Added patch gok-04-actionfix.diff for P1 6176892.
  Should be removed when we rev to gok-0.11.11 or higher.
* Wed Oct 08 2004 - bill.haneman@sun.com
- Added buildfix patch gok-03-buildfix.diff (forte build failed).
* Wed Oct 06 2004 - bill.haneman@sun.com
- Revved to 0.11.10, to fix P1 6174262.
* Fri Oct 01 2004 - bill.haneman@sun.com
- Revved to 0.11.9
* Fri Sep 24 2004 - yuriy.kuznetsov@sun.com
- Added gok-02-g11n-potfiles.diff
* Wed Sep 16 2004 - laca@sun.com
- added missing dependencies
* Wed Sep 15 2004 - damien.carbery@sun.com
- Integrate updated docs tarball from irene.ryan@sun.com.
* Thu Sep 02 2004 - damien.carbery@sun.com
- Add docs tarball from irene.ryan@sun.com.
* Wed Sep 01 2004 - bill.haneman@sun.com
- Revved to 0.11.7.
* Wed Aug 25 2004 - damien.carbery@sun.com
- Add create-branching-keyboard to %files.
* Tue Aug 24 2004 - bill.haneman@sun.com
- Removed "launcher.kbd" part of gok-01-jds-apps.diff, we only need to patch
- the .kbd.in file and re-make.
* Thu Aug 17 2004 - bill.haneman@sun.com
- Added patch gok-01-jds-apps.diff, for bug #5085248.  This is a JDS-specific 
- branding patch, which needed to be applied now due to string freeze impact.
* Mon Aug 16 2004 - bill.haneman@sun.com
- Bumped to 0.11.6.
* Thu Aug 12 2004 - bill.haneman@sun.com
- Removed the gok g11n patches, they should have been applied to cvs instead.
- They were also incorrect; root cause of problem appears to be an intltool bug
- Bumped version to 0.11.5.
* Wed Jul 15 2004 - takao.fujiwara@sun.com
- Added gok-01-g11n-potfiles.diff and gok-02-g11n-i18n-ui.diff. Fixes bug
  #5074183
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gok-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Wed Jun 23 2004 - muktha.narayan@wipro.com
- Install gconf schema files. Fixes bug #5045140
* Fri Jun 11 2004 - dermot.mccluskey@sun.com
- fix 0.11.4.1 tarball and Source tag
* Thu Jun 10 2004 - <bill.haneman@sun.com>
- Bump to 0.11.4.1
* Thu Jun 10 2004 - <padraig.obriain@sun.com>
- Bump to 0.11.4
* Fri May 14 2004 - <padraig.obriain@sun.com>
- Bump to 0.11.2
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gok-l10n-po-1.1.tar.bz2
* Thu Apr 22 2004 - <padraig.obriain@sun.com>
- Bump to 0.10.2
* Sun Apr 18 2004 - laca@sun.com
- enable javahelp conversion on Solaris
* Thu Apr 01 2004 - matt.keenan@sun.com
- Javahelp converison
* Wed Mar 31 2004 - brian.cameron@sun.com
- replace tar jxf with the more solaris friendly
  bzcat piped through tar
* Mon Mar 29 2004 - damien.donlon@sun.com
- Adding gok-l10n-po-1.0.tar.bz2 l10n content
* Tue Mar 23 2004 - <padraig.obriain@sun.com>
- Bump to 0.10.0
* Mon Mar 15 2004 - <damien.carbery@sun.com>
- Remove gtk-doc line from %files section as no files there any more.
* Thu Mar 11 2004 - <damien.carbery@sun.com>
- Reset release to 1.
* Wed Mar 10 2004 - damien.carbery@sun.com
- Bump to 0.9.10
* Mon Feb 23 2004 - damien.carbery@sun.com
- Created new spec file for gok
