#
# spec file for package SUNWgnome-libs
#
# includes module(s): rarian, startup-notification, libgtkhtml,
# 	              libgnome, libbonoboui, libgnomeui, libexif-gtk
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
%include Solaris.inc
%use rarian = rarian.spec
%use startupnotification = startup-notification.spec
%use libgtkhtml = libgtkhtml.spec
%use libgnome = libgnome.spec
%use libbonoboui = libbonoboui.spec
%use gnomekeyring = gnome-keyring.spec
%use libgnomeui = libgnomeui.spec
%use libexif_gtk = libexif-gtk.spec

Name:                    SUNWgnome-libs
Summary:                 GNOME platform libraries
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-vfs
Requires: SUNWgnome-audio
Requires: SUNWlibexif
Requires: SUNWlibgcrypt
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWfreetype2
Requires: SUNWlibpopt
Requires: SUNWpng
Requires: SUNWTiff
Requires: SUNWjpg
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWlxsl
Requires: SUNWdesktop-cache
Requires: SUNWlibC
Requires: SUNWlibtasn1
Requires: SUNWbash
Requires: SUNWhal
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWlibexif-devel
BuildRequires: SUNWlibgcrypt-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWlibC
BuildRequires: SUNWlibtasn1-devel
BuildRequires: SUNWhal

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc
Requires: SUNWgnome-xml-root
Requires: SUNWpostrun

%package devel		
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs-devel
Requires: SUNWgnome-audio-devel
Requires: SUNWperl584usr
Requires: SUNWlibms
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWlibpopt

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
%rarian.prep -d %name-%version
%startupnotification.prep -d %name-%version
%libgtkhtml.prep -d %name-%version
%libgnome.prep -d %name-%version
%libbonoboui.prep -d %name-%version
%gnomekeyring.prep -d %name-%version
%libgnomeui.prep -d %name-%version
%libexif_gtk.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED
export PKG_CONFIG_PATH=../libgnome-%{libgnome.version}/libgnome:../gnome-keyring-%{gnomekeyring.version}/library:../libbonoboui-%{libbonoboui.version}/bonobo:%{_pkg_config_path}
%if %cc_is_gcc
%else
export CXX="${CXX} -norunpath"
%endif
export CXXFLAGS="%cxx_optflags"
export CFLAGS="%optflags -I/usr/sfw/include -DANSICPP"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -norunpath"
export STRIP="/usr/ccs/bin/strip"

%rarian.build -d %name-%version
%startupnotification.build -d %name-%version
%libgtkhtml.build -d %name-%version
%libgnome.build -d %name-%version
%libbonoboui.build -d %name-%version
%gnomekeyring.build -d %name-%version
%libgnomeui.build -d %name-%version
%libexif_gtk.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%rarian.install -d %name-%version
%startupnotification.install -d %name-%version
%libgtkhtml.install -d %name-%version
%libgnome.install -d %name-%version
%libbonoboui.install -d %name-%version
%gnomekeyring.install -d %name-%version
%libgnomeui.install -d %name-%version
%libexif_gtk.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

chmod 755 $RPM_BUILD_ROOT%{_mandir}/man1/*.1
chmod 755 $RPM_BUILD_ROOT%{_mandir}/man3/*.3
chmod 0644 $RPM_BUILD_ROOT%{_libdir}/bonobo/servers/Bonobo_Sample_Controls.server
chmod 0644 $RPM_BUILD_ROOT%{_libdir}/bonobo/servers/GNOME_Moniker_std.server

rm -rf $RPM_BUILD_ROOT%{_datadir}/doc
rm -rf $RPM_BUILD_ROOT%{_datadir}/applications

rm -rf $RPM_BUILD_ROOT/var
rm -rf $RPM_BUILD_ROOT%{_prefix}/var

rm -rf $RPM_BUILD_ROOT%{_libdir}/gnome-keyring/devel
rm -rf $RPM_BUILD_ROOT%{_libdir}/gnome-keyring/standalone
rm -rf $RPM_BUILD_ROOT%{_libdir}/gnome-keyring/*.la

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri gconf-cache

%post root
( echo 'xmlcatalog --noout --add "rewriteSystem" \' ;
  echo '"http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0" \' ;
  echo '"file://%{_datadir}/xml/scrollkeeper/dtds" %{_sysconfdir}/xml/catalog'
) | $BASEDIR/var/lib/postrun/postrun -c JDS

%preun root
test -x $BASEDIR/var/lib/postrun/postrun || exit 0
( echo 'xmlcatalog --noout --del \' ;
  echo '"http://scrollkeeper.sourceforge.net/dtds/scrollkeeper-omf-1.0" \' ;
  echo '%{_sysconfdir}/xml/catalog'
) | $BASEDIR/var/lib/postrun/postrun -i -c JDS

%postun root
rm -rf $BASEDIR/var/lib/scrollkeeper

%files
%doc(bzip2) gnome-keyring-%{gnomekeyring.version}/COPYING
%doc(bzip2) gnome-keyring-%{gnomekeyring.version}/COPYING.LIB
%doc(bzip2) gnome-keyring-%{gnomekeyring.version}/NEWS
%doc(bzip2) gnome-keyring-%{gnomekeyring.version}/ChangeLog
%doc gnome-keyring-%{gnomekeyring.version}/AUTHORS
%doc gnome-keyring-%{gnomekeyring.version}/README
%doc(bzip2) libbonoboui-%{libbonoboui.version}/COPYING
%doc(bzip2) libbonoboui-%{libbonoboui.version}/COPYING.LIB
%doc(bzip2) libbonoboui-%{libbonoboui.version}/NEWS
%doc(bzip2) libbonoboui-%{libbonoboui.version}/ChangeLog
%doc libbonoboui-%{libbonoboui.version}/MAINTAINERS
%doc libbonoboui-%{libbonoboui.version}/README
%doc(bzip2) libexif-gtk-%{libexif_gtk.version}/COPYING
%doc(bzip2) libexif-gtk-%{libexif_gtk.version}/NEWS
%doc(bzip2) libexif-gtk-%{libexif_gtk.version}/ChangeLog
%doc libexif-gtk-%{libexif_gtk.version}/README
%doc(bzip2) libgnome-%{libgnome.version}/COPYING.LIB
%doc(bzip2) libgnome-%{libgnome.version}/NEWS
%doc(bzip2) libgnome-%{libgnome.version}/ChangeLog
%doc libgnome-%{libgnome.version}/AUTHORS
%doc libgnome-%{libgnome.version}/MAINTAINERS
%doc libgnome-%{libgnome.version}/README
%doc(bzip2) libgnomeui-%{libgnomeui.version}/COPYING.LIB
%doc(bzip2) libgnomeui-%{libgnomeui.version}/NEWS
%doc(bzip2) libgnomeui-%{libgnomeui.version}/ChangeLog
%doc libgnomeui-%{libgnomeui.version}/AUTHORS
%doc libgnomeui-%{libgnomeui.version}/MAINTAINERS
%doc libgnomeui-%{libgnomeui.version}/README
%doc(bzip2) libgtkhtml-%{libgtkhtml.version}/COPYING.LIB
%doc(bzip2) libgtkhtml-%{libgtkhtml.version}/NEWS
%doc(bzip2) libgtkhtml-%{libgtkhtml.version}/ChangeLog
%doc libgtkhtml-%{libgtkhtml.version}/AUTHORS
%doc libgtkhtml-%{libgtkhtml.version}/README
%doc(bzip2) rarian-%{rarian.version}/COPYING
%doc(bzip2) rarian-%{rarian.version}/COPYING.LIB
%doc(bzip2) rarian-%{rarian.version}/NEWS
%doc(bzip2) rarian-%{rarian.version}/ChangeLog
%doc rarian-%{rarian.version}/MAINTAINERS
%doc rarian-%{rarian.version}/README
%doc(bzip2) startup-notification-%{startupnotification.version}/COPYING
%doc(bzip2) startup-notification-%{startupnotification.version}/NEWS
%doc(bzip2) startup-notification-%{startupnotification.version}/ChangeLog
%doc startup-notification-%{startupnotification.version}/AUTHORS
%doc startup-notification-%{startupnotification.version}/README
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/rarian-sk-install
%{_bindir}/rarian-sk-get-extended-content-list
%{_bindir}/rarian-sk-extract
%{_bindir}/rarian-sk-preinstall
%{_bindir}/rarian-sk-get-content-list
%{_bindir}/rarian-sk-migrate
%{_bindir}/rarian-example
%{_bindir}/rarian-sk-get-scripts
%{_bindir}/rarian-sk-gen-uuid
%{_bindir}/rarian-sk-rebuild
%{_bindir}/rarian-sk-update
%{_bindir}/rarian-sk-get-cl
%{_bindir}/rarian-sk-config
%{_bindir}/scrollkeeper-config
%{_bindir}/scrollkeeper-get-cl
%{_bindir}/scrollkeeper-get-content-list
%{_bindir}/scrollkeeper-get-extended-content-list
%{_bindir}/scrollkeeper-get-index-from-docpath
%{_bindir}/scrollkeeper-get-toc-from-docpath
%{_bindir}/scrollkeeper-get-toc-from-id
%{_bindir}/scrollkeeper-install
%{_bindir}/scrollkeeper-preinstall
%{_bindir}/scrollkeeper-rebuilddb
%{_bindir}/scrollkeeper-uninstall
%{_bindir}/scrollkeeper-update
%{_bindir}/gnome-keyring*
%{_bindir}/gnome-open
%{_bindir}/bonobo-browser
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%{_libdir}/bonobo/monikers/*.so
%{_libdir}/bonobo/servers/*.server
%{_libdir}/gnome-keyring/*
%{_libdir}/libglade/2.0/*.so
%{_libexecdir}/gnome-keyring-ask
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/dbus-1
%dir %attr (0755, root, bin) %{_datadir}/dbus-1/services
%{_datadir}/dbus-1/services/org.gnome.keyring.service
%dir %attr (0755, root, other) %{_datadir}/gcr
%dir %attr (0755, root, other) %{_datadir}/gcr/ui
%{_datadir}/gcr/ui/*


%{_datadir}/gnome-2.0/*
%{_datadir}/help
%{_datadir}/librarian
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/gnome-background-properties
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/scrollkeeper-extract
%{_bindir}/scrollkeeper-gen-seriesid
%{_bindir}/test-moniker
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo-2.0
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%{_mandir}/man3/*

%files root
%attr (0755, root, sys) %dir %{_sysconfdir}
%defattr (-, root, sys)
%{_sysconfdir}/gconf/schemas/desktop_gnome_accessibility_keyboard.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_accessibility_startup.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_applications_at_visual.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_applications_at_mobility.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_applications_browser.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_applications_office.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_applications_terminal.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_applications_window_manager.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_background.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_file_views.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_interface.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_lockdown.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_keyboard.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_peripherals_mouse.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_sound.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_thumbnailers.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_thumbnail_cache.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_typing_break.schemas
%{_sysconfdir}/gconf/schemas/gnome-keyring.schemas
%{_sysconfdir}/sound
%{_sysconfdir}/xdg/autostart/gnome-keyring-daemon.desktop

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Tue Apr 14 2009 - halton.huo@sun.com
- Correct restart_fmri service name to gconf-cache
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/bin/rarian-sk-config (SUNWgnome-libs) requires /usr/bin/bash
  which is found in SUNWbash, add the dependency.
* Wed Mar 03 2009 - jeff.cai@sun.com
- Not ship ssh pkcs11 modules and *.la files.
* Wed Feb 04 2009 - jeff.cai@sun.com
- Move gnome-keyring-daemon.desktop to /etc/xdg/autostart
* Fri Dec 12 2008 - jeff.cai@sun.com
- Add gnome-keyring-daemon.desktop in %files section
* Thu Sep 11 2008 - padraig.obriain@sun.com
- Add %doc to %files for copyright
* Tue Jun 24 2008 - damien.carbery@sun.com
- Remove "-lgailutil" from LDFLAGS. Root cause found in gtk+: bugzilla 536430.
* Fri Jun 20 2008 - jeff.cai@sun.com
  gnome-keyring requires SUNWlibtasn1 and SUNWlibtasn1-devel
* Wed Jun 18 2008 - jeff.cai@sun.com
  Bump gnome-keyring and ship some new files.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Update %files, removing %{_libdir}/gtk-2.0/2.*.*/filesystems/lib*.so* as those
  files are no longer installed.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Add desktop_gnome_thumbnail_cache.schemas to %files and %post root.
* Tue Jun 03 2008 - damien.carbery@sun.com
- Add "-lgailutil" to LIBS so that libgailutil is linked in when libgnomecanvas 
  is linked. libgnomecanvas.so includes some gail functions.
* Thu Mar 27 2008 - alvaro.lopez@sun.com
- Added copyright file
* Thu Mar 06 2008 - damien.carbery@sun.com
- Add desktop_gnome_applications_office.schemas to %files root and %post root.
* Thu Jan 29 2008 - damien.carbery@sun.com
- Remove refs to desktop_gnome_applications_help_viewer.schemas.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Oct 26 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWlibC after check-deps.pl run.
* Thu Oct 25 2007 - damien.carbery@sun.com
- Add -norunpath to CXX to fix runpath issue in librarian.so. Fixes 6614963.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Add -norunpath to LDFLAGS to fix 6614963.
* Mon Oct  8 2007 - damien.carbery@sun.com
- Remove %{_datadir}/gnome-background-properties from %files devel because it
  is already in the base package. Fixes 6613798.
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X deps
* Wed Sep 19 2007 - damien.carbery@sun.com
- Add %{_datadir}/gnome-background-properties to %files.
* Thu Sep 06 2007 - ghee.teo@sun.com
- Remove  %{_libdir}/pam_gnome_keyring.so from %files as it is currently
  premature to include this pam module. Details to use it fully is
  http://live.gnome.org/GnomeKeyring/Pam
* Wed Sep 05 2007 - damien.carbery@sun.com
- Remove references to SUNWgnome-a11y-base-libs as its contents have been
  moved to SUNWgnome-base-libs.
* Fri Aug 17 2007 - damien.carbery@sun.com
- Replace scrollkeeper with rarian.
* Tue Jul 31 2007 - damien.carbery@sun.com
- Add new file %{_libdir}/pam_gnome_keyring.so to %files. Remove
  %{_libexecdir}/gnome_segv2 as it is no longer installed.
* Wed May 16 2007 - damien.carbery@sun.com
- Add Build/Requires SUNWlibgcrypt/-devel for gnome-keyring. Adjust
  PKG_CONFIG_PATH because gnome-keyring .pc file in subdir now.
* Thu May  3 2007 - laca@sun.com
- reshuffle postrun scripts so that adding/removing the scrollkeeper
  dtd rewrite rule actually works.
- add dependency on SUNWgnome-xml-root so /etc/xml/catalog exists
* Thu Apr 19 2007 - laca@sun.com
- add postrun scripts that add/delete a rewrite rule for the scrollkeeper
  dtd to /etc/xml/catalog, so that libxml2 can find it locally and not
  try to download it from the net
* Wed Jan 10 2007 - damien.carbery@sun.com
- Add 2 new schema files to %files and %preun root.
* Wed Dec 13 2006 - damien.carbery@sun.com
- Update %files (add some docs) after removal of scrollkeeper.spec patch.
* Tue Nov 28 2006 - damien.carbery@sun.com
- Change attr of scrollkeeper.conf file in root package to fix 6497737.
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Thu Jun 29 2006 - laca@sun.com
- Remove gtksourceview and move it in its own pkg because it also depends
  on SUNWgnome-print and SUNWgnome-print depends on this pkg.
* Tue Jun 27 2006 - laca@sun.com
- Move gtksourceview from SUNWgnome-text-editor to here so that it gets built 
  in gnome-python-desktop.
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Jun  2 2006 - laca@sun.com
- s/RPM_BUILD_ROOT/PKG_INSTALL_ROOT/ in %postun... eeek!
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
- fix %postun script so that it nukes the scrollkeeper data rather than
  trying to execute scrollkeeper-update, which doesn't exist after this
  pkg is uninstalled anyway
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Wed Oct 26 2005 - damien.carbery@sun.com
- Delete %{_datadir}/locale when not %build_l10n. Fix %files for same.
* Mon Oct 10 2005 - damien.carbery@sun.com
- Add dependency on SUNWgnome-component (bonobo-activation reqd by libgnome).
* Fri Sep 09 2005 - <laca@sun.com>
- remove unpackaged files
* Wed Jun 15 2005 - laca@sun.com
- Add bonobo-browser to %files
* Tue Oct 19 2004 - kazuhiko.maekawa@sun.com
- Remove unnecessary sym-links to avoid build err
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added gnome-open.1 manpage
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : sman3/4 files should be in a separate devel package
* Tue Aug 24 2004 - laca@sun.com
- move l10n files to the l10n package
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Thu Aug 19 2004 shirley.woo@sun.com
- Bug 5089621 : removed un-need doc due to duplicat entries
* Wed Aug 18 2004  damien.carbery@sun.com
- Changed /usr/share/man/sman3/*.3 permission to 0755 for Solaris integration
- Changed %{_libdir}/bonobo/servers/*.server perms for Solaris integration.
* Mon Aug 16 2004  shirley.woo@sun.com
- Changed /usr/share/man/sman1/*.1 permission to 0755 for Solaris integration
* Mon Jul 12 2004 - damien.carbery@sun.com
- Unset perms for /usr/share/pixmaps.
* Sun Jul 11 2004 - damien.carbery@sun.com
- Set perms for /usr/share/pixmaps.
* Sat Jul 10 2004 - damien.carbery@sun.com
- Remove omf/scrollkeeper dir from share package. The writing_omf_files docs
  are no longer delivered.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Mon Jun 07 2004 - brian.cameron@sun.com
- Added libexif-gtk to package.  Added SUNWlibexif dependency.
* Wed Jun 02 2004 - takao.fujiwara@sun.com
- Added locale symbolic links
* Thu May 27 2004 - laca@sun.com
- added l10n subpkg
* Sun May 02 2004 - laca@sun.com
- remove unnecessary SUNWgnome-javahelp-convert dependency
  to avoid circular dep
* Sun Apr 04 2004 - laca@sun.com
- Added %{_libdir}/gtk-2.0/*/filesystems/libgnome-vfs.so to %files
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Fri Mar 12 2004 - niall.power@sun.com
- added missing stuff in libexecdir and bindir.
* Mon Mar 01 2004 - niall.power@sun.com
- add missing libglade subdir to files
* Sat Feb 28 2004 - laca@sun.com
- fix gconf dir permissions (a+rX)
* Wed Feb 25 2004 - niall.power@sun.com
- add "-R%{_libdir}" to LDFLAGS
* Web Feb 25 2004 - laca@sun.com
- moved libgnomecanvas into SUNWgnome-base-libs
* Web Feb 25 2004 - laca@sun.com
- moved libart_lgpl and librsvg into SUNWgnome-base-libs
* Mon Feb 23 2004 - niall.power@sun.com
- install gconf schemas at the end of the install stage.
* Fri Feb 20 2004 - laca@sun.com
- Removed gail. It's now in SUNWgnome-base-a11y-libs.
* Wed Feb 18 2004 - laca@sun.com
- Moved librsvg here from SUNWgnome-file-mgr
- add libghttp
* Mon Feb 16 2004 - niall.power@sun.com
- Fix up dependencies and files mapping
