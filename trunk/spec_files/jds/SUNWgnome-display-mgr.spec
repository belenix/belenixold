#
# spec file for package SUNWgnome-display-mgr
#
# includes module(s): gdm
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yippi
#
%include Solaris.inc

%use gdm = gdm.spec

Name:                    SUNWgnome-display-mgr
Summary:                 GNOME display manager
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
Source1:                 gdm.xml
Source2:                 svc-gdm
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires: SUNWlibrsvg-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWlxml
BuildRequires: SUNWlibcroco
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWlibrsvg-devel
#%if %option_without_fox
#
# GDM's configure depends on Xephyr to be installed so it properly
# sets Xnest configure option.
BuildRequires: SUNWxorg-server
Requires: SUNWxorg-server
Requires: SUNWxwplt
#%else
# if SUNWxwplt is installed, then configure finds /usr/X11/bin/Xserver
# instead of /usr/X11/bin/Xorg
#BuildConflicts: SUNWxwplt
#%endif
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-display-mgr-root
Requires: SUNWgnome-dialog
Requires: SUNWlibrsvg
Requires: SUNWlxml
Requires: SUNWlibcroco
Requires: SUNWdesktop-cache
%if %option_with_dt
Requires: SUNWgnome-dtlogin-integration
%else
Requires: SUNWdesktop-startup
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWgnome-display-mgr

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
rm -rf %name-%version
mkdir %name-%version
%gdm.prep -d %name-%version
chmod -R u+w %{_builddir}/%name-%version/gdm-%{gdm.version}
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export LDFLAGS="%_ldflags -L/usr/openwin/lib -lXau -R/usr/openwin/lib -R/usr/sfw/lib"
export PKG_CONFIG_PATH=%{_pkg_config_path}
X11_CFLAGS=
pkg-config --exists x11 && X11_CFLAGS=`pkg-config --cflags x11`
export CFLAGS="%optflags $X11_CFLAGS"
#FIXME:
# This is to fix CR #6781266 -gdmsetup fails to startup when compiled with -xO3
# or higher, it is actually compiler bug, CR #6781229.
# Current workaround is adding -W2,-Rcond_elim to CFLAGS in non-debug mode.
# Remove the logic after CR#6781229 is fixed
%if %debug_build
%else
export CFLAGS="$CFLAGS -W2,-Rcond_elim"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%if %option_without_dt
export GDMGNOMESESSIONCMD="/usr/bin/dtstart jds"
%endif
%gdm.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gdm.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT/var/svc/manifest/application/graphical-login
install --mode=0444 %SOURCE1 $RPM_BUILD_ROOT/var/svc/manifest/application/graphical-login
install -d $RPM_BUILD_ROOT/lib/svc/method
cp %SOURCE2 $RPM_BUILD_ROOT/lib/svc/method/

rmdir $RPM_BUILD_ROOT/etc/X11/dm
rmdir $RPM_BUILD_ROOT/etc/pam.d

# The %{_datadir}/xsessions file contains two files: a gnome.desktop file
# and a CDE.desktop file.  We always want to delete the gnome.desktop
# file since it is now delivered by the gnome-session module.  If not
# shipping with CDE support, then remove the entire xsessions directory.
#
%if %option_with_dt
rm $RPM_BUILD_ROOT%{_datadir}/xsessions/gnome.desktop
%else
rm -fR $RPM_BUILD_ROOT%{_datadir}/xsessions
%endif

# Create the 'interface' directory so that user's session scripts can be
# run by gdm and which are populated by other applications.
install -d $RPM_BUILD_ROOT/%{_sysconfdir}/X11/xinit/xinitrc.d

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/*help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/gdm/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache

%post root
cat >> $BASEDIR/var/svc/profile/upgrade <<\EOF

# We changed gdm's FMRI.  If the old service exists and is enabled,
# disable it and enable the new one.
gdm=svc:/application/gdm2-login:default
if svcprop -q $gdm; then
	set -- `svcprop -C -t -p general/enabled $gdm`
	if [ $? -ne 0 ]; then
		echo "Could not read whether $gdm was enabled."
	elif [ $2 != boolean ]; then
		echo "general/enabled property of $gdm has bad type."
	elif [ $# -ne 3 ]; then
		echo "general/enabled property of $gdm has the wrong number\c"
		echo " of values."
	elif [ $3 = true ]; then
		svcadm disable $gdm
		svcadm enable svc:/application/graphical-login/gdm:default
	fi
fi

EOF

%postun
%restart_fmri desktop-mime-cache

%iclass preserve -f i.preserve

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/gdm
%{_sbindir}/gdm-binary
%{_sbindir}/gdm-restart
%{_sbindir}/gdm-safe-restart
%{_sbindir}/gdm-stop
%attr (0700, root, bin) %{_sbindir}/gdmsetup
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gtk-2.0/modules/*.so
%{_libexecdir}/gdm*
%dir %attr (0755, root, sys) %{_datadir}
%doc -d gdm-%{gdm.version} AUTHORS README
%doc(bzip2) -d gdm-%{gdm.version} COPYING NEWS
%doc(bzip2) -d gdm-%{gdm.version} ChangeLog po/ChangeLog docs/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/gdm
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gdm/C
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/16x16/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/22x22/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/24x24/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/32x32/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor/scalable/apps
%attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps/*
%attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps/*
%{_datadir}/omf/gdm/*-C.omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
# Include CDE desktop file if building with CDE.
%if %option_with_dt
%{_datadir}/xsessions
%endif
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%dir %attr(0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1/*
%{_mandir}/man1m/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%if %is_s10
%dir %attr (0755, root, other) %{_sysconfdir}/X11
%else
%dir %{_sysconfdir}/X11
%endif
%dir %{_sysconfdir}/X11/gdm
%{_sysconfdir}/X11/gdm/Init
%{_sysconfdir}/X11/gdm/Post*
%{_sysconfdir}/X11/gdm/Pre*
%{_sysconfdir}/X11/gdm/X*
%{_sysconfdir}/X11/gdm/gdmprefetchlist
%config %class(preserve) %{_sysconfdir}/X11/gdm/custom.conf
%{_sysconfdir}/X11/gdm/locale.alias
%{_sysconfdir}/X11/gdm/modules
%dir %{_sysconfdir}/X11/xinit
%dir %{_sysconfdir}/X11/xinit/xinitrc.d
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0555, root, bin) /lib/svc/method/svc-gdm
# don't use %_localstatedir here, because this is an absolute path
# defined by another package, so it has to be /var/svc even if this
# package's %_localstatedir is redefined
%dir %attr (0755, root, sys) /var
/var/svc/*
%dir %attr (0755, root, sys) /var/log
%dir %attr (0755, root, root) /var/log/gdm
%dir %attr (0755, root, other) %{_localstatedir}/lib
%dir %attr (1770, root, gdm) %{_localstatedir}/lib/gdm

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/*help/*/[a-z]*
%{_datadir}/omf/gdm/*-[a-z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed Apr 01 2009 - jeff.cai@sun.com
- Add the dependency of SUNWswmt for the root package since the customer.conf
  uses i.preserve.
* Tue Mar 24 2009 - jeff.cai@sun.com
- Add the dependency of SUNWgnome-display-mgr for the root package.
* Web Feb 25 2009 - dave.lin@sun.com
- Changed to Requires: SUNWdesktop-startup due to SUNWgnome-dtstart was renamed.
* Fri Dec 05 2008 - halton.huo@sun.com
- Add workaround to fix CR #6781266 - gdmsetup fails to startup
* Wed Nov 21 2008 - brian.cameron@sun.com
- Add /lib/svc/method/svc-gdm SMF method file so that the "stop" method
  doesn't cause errors on shutdown/restart.  Fix packaging permissions.
  Fix for doo bug #4887.
* Thu Oct 02 2008 - ghee.teo@sun.com
- Added directory /etc/X11/xinit/xinitrc.d as part of the fix to 6755007 and
  also d.o.o #4097.
* Sun Sep 14 2008 - brian.cameron@sun.com
- Add new copyright files.
* Tue Jun 24 2008 - damien.carbery@sun.com
- Remove "-lgailutil" from LDFLAGS. Root cause found in gtk+: bugzilla 536430.
* Thu Jun 05 2008 - damien.carbery@sun.com
- Add "-lgailutil" to LDFLAGS so that libgailutil is linked in when
  libgnomecanvas is linked. libgnomecanvas.so includes some gail functions.
* Wed May 07 2008 - damien.carbery@sun.com
- Remove PERL5LIB setting as it is not necessary.
* Thu May 01 2008 - brian.cameron@sun.com
- Fix packaging.  Ship the CDE desktop file if building with
  "with_dt".
* Thu Mar 27 2008 - brian.cameron@sun.com
- Add SUNW_Copyright.
* Sat Jan 26 2008 - brian.cameron@sun.com
- Minor cleanup
* Thu Jan 17 2008 - damien.carbery@sun.com
- Delete %{_datadir}/xsessions/gnome.desktop file as it is now delivered by
  gnome-session module.
* Fri Oct 12 1007 - laca@sun.com
- add x11 compile flags to CFLAGS if x11.pc exists (FOX fix)
* Fri Sep 28 2007 - laca@sun.com
- add support for building with FOX and using dtstart instead of
  dtlogin-integration
* Fri May 11 2007 - brian.cameron@sun.com
- Fix packaging and add needed -R/usr/sfw/lib to link flags.
* Thu May 10 2007 - brian.cameron@sun.com
- Fix packaging for bumping to 2.19.0.
* Thu Apr 12 2007 - brian.cameron@sun.com
- Add SUNWxorg-server as a dependency, since GDM depends on Xephyr
* Fri Mar 09 2007 - brian.cameron@sun.com
- Change file permissions for gdmsetup to 700 so that the gdmsetup
  menu choice only appears for the root user.  Also no longer install
  the %{datadir}/applications directory since we now install to 
  /usr/share/gdm/applications.
* Sun Jan 28 2007 - laca@sun.com
- update %files root so that dir attributes work on both s10 and nevada
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Mon Aug 28 2006 - brian.cameron@sun.com
- Add gdmdynamic manpage.
* Fri Aug 25 2006 - laca@sun.com
- move the smf profile rename postinstall stuff into the -root subpkg,
  because the base package doesn't have access to the / files in the
  case of a diskless installation, part of CR6448317
* Wed Aug 23 2006 - brian.cameron@sun.com
- Move some GDM manpages to sman1m to reflect that the binaries have
  moved to /usr/sbin.
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Fri Jun 23 2006 - christopher.hanna@sun.com
- Removed manpages which arent needed: gdmchooser, gdmgreeter and gdmlogin
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri May 12 2006 - brian.cameron@sun.com
- Add SUNWgnome-dialog as a dependency since GDM does use zenity in places.
* Thu May 11 2006 - brian.cameron@sun.com
- Added %post scripting to migrate users from the old SMF service name
  to the new one.  
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue May 09 2006 - brian.cameron@sun.com
- No longer install the /var/gdm directories here since they get installed via
  make install.
* Tue Apr 18 2006 - brian.cameron@sun.com
- Mark custom.conf as in the preserve class so it doesn't get deleted on pkgrm.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Mark custom.conf as volatile (%config).
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Update %files for new tarball (conf files renamed).
* Sat Jan 21 2006 - damien.carbery@sun.com
- Remove locale.alias.orig file from %files. Mistake in build.
* Thu Jan 19 2006 - brian.cameron@sun.com
- Fixed packaging after updating to 2.13.0.6
* Thu Jan 19 2006 - damien.carbery@sun.com
- Add new %files from bumped tarball.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Add SUNWlibcroco to Build/Requires list.
* Mon Jan 16 2006 - damien.carbery@sun.com
- Move /usr/sfw/include reference from gdm.spec to here as it is Solaris only.
- Update Build/Requires lines.
* Mon Jan 16 2006 - padraig.obriain@sun.com
- add reference to %{_libexecdir}/X11/gdm/gdmprefetchlist
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Thu Sep 15 2005 - laca@sun.com
- Remove unpackaged empty directories
* Thu Jul 28 2005 - damien.carbery@suncom
- Add SUNWlibrsvg-devel build dependency. Add SUNWlibrsvg runtime dependency.
- Wed Jul 13 2005 - brian.cameron@sun.com
- Updated to 2.8.0.5.  Updated SVC (GreenLine) integration.
+ Mon Feb 07 2004 - brian.cameron@sun.com
- Fixed permissions on /var/lib/gdm so it doesn't complain on
  reinstall.  The gdm binary program changes the ownership and
  permissions of this file on runtime if they aren't set 
  properly.  This change makes the original permissions set
  by the package correct so gdm won't change them.
* Thu Nov 18 2004 - hidetoshi.tajima@sun.com
- #5081827 - required SUNWgnome-dtlogin-integration to run
/usr/dt/config/Xsession.jds in gnome session
* Wed Nov 17 2004 - matt.keenan@sun.com
- #6195852 - Fix manpage directory installed (stopper)
* Sat Nov 13 2004 - laca@sun.com
- include gdm.conf in the "preserve" class, fixes 5101934
  Note: requires pkgbuild-0.8.2 (CBE 0.18)
* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Revised files section
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 02 2004  <damien.carbery@sun.com>
- Add %dir %attr for mandir and mandir/man1. Attribute change install error.
* Thu Sep 02 2004  <matt.keenan@sun.com>
- Added gdm manpages for solaris
* Tue Jul 27 2004  <glynn.foster@sun.com>
- Put back the New Login in New Window as it's supported.
* Tue Jul 27 2004  <glynn.foster@sun.com>
- Remove the flexiserver .desktop items. Need to have a 
  look to see if the flexiserver binary stuff should be
  include as well or not. Part fix for #5043894.
* Fri Jul 23 2004  <brian.cameron@sun.com>
- Now include /var/lib/gdm and /var/lib/log/gdm in the
  package so that gdm can run out-of-the-box.
* Sun Jun 27 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Mon Mar 01 2004 - <laca@sun.com>
- define PERL5LIB.
- add share and root subpkgs
