#
# spec file for package SUNWgnome-dictionary, SUNWgnome-search-tool
#
# includes module(s): gnome-utils
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: mattman
#
%include Solaris.inc

%use gnome_utils = gnome-utils.spec

Name:                    SUNWgnome-utils
Summary:                 GNOME utilities: dictionary, search tool
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-doc-utils
BuildRequires: SUNWlibgtop-devel
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-component
Requires: SUNWlibgtop

%package -n SUNWgnome-search-tool
Summary:                 GNOME file search tool
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-search-tool-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-panel
Requires: SUNWgnome-vfs
Requires: SUNWdesktop-cache
Requires: SUNWxcu4

%package -n SUNWgnome-search-tool-root
Summary:                 GNOME file search tool - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-dictionary
Summary:                 GNOME dictionary tool
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-dictionary-root
Requires: SUNWgnome-libs
Requires: SUNWgnome-panel
Requires: SUNWgnome-print
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWlibms

%package -n SUNWgnome-dictionary-root
Summary:                 GNOME dictionary tool - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-screenshot
Summary:                 GNOME screenshot tool
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-screenshot-root
Requires: SUNWgnome-config
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWdesktop-cache

%package -n SUNWgnome-screenshot-root
Summary:                 GNOME screenshot tool - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-log-viewer
Summary:                 GNOME log viewer
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-log-viewer-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-panel
Requires: SUNWgnome-vfs
Requires: SUNWdesktop-cache
Requires: SUNWlibms

%package -n SUNWgnome-log-viewer-devel
Summary:                 GNOME log viewer development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-log-viewer-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-panel
Requires: SUNWgnome-vfs
Requires: SUNWdesktop-cache
Requires: SUNWlibms

%package -n SUNWgnome-log-viewer-root
Summary:                 GNOME log viewer - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package -n SUNWgnome-disk-analyzer
Summary:                 GNOME disk usage analyzer
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-libs
Requires: SUNWgnome-vfs
Requires: SUNWlibgtop
Requires: SUNWgnome-disk-analyzer-root
Requires: SUNWdesktop-cache

%package -n SUNWgnome-disk-analyzer-root
Summary:                 GNOME disk usage analyzer - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

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
%gnome_utils.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -
cd %{_builddir}/%name-%version/gnome-utils-%{gnome_utils.version}

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
%gnome_utils.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gnome_utils.install -d %name-%version
rm -f $RPM_BUILD_ROOT%{_mandir}/*/*.gz
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/gnome-system-log/plugins/*.la

# Remove developer files and documentation.
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome-system-log
rm -r $RPM_BUILD_ROOT%{_datadir}/gtk-doc
rm -r $RPM_BUILD_ROOT%{_includedir}/gdict*
rm -r $RPM_BUILD_ROOT%{_libdir}/pkgconfig
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome-utils

# Never install English locales because should support full functions
# on English locales as same as Solaris.
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/baobab/en_GB
rm -r $RPM_BUILD_ROOT%{_datadir}/locale/en_GB
rm $RPM_BUILD_ROOT%{_datadir}/omf/baobab/baobab-en_GB.omf
rm $RPM_BUILD_ROOT%{_datadir}/omf/gnome-system-log/gnome-system-log-en_GB.omf
rm $RPM_BUILD_ROOT%{_datadir}/omf/gnome-dictionary/gnome-dictionary-en_GB.omf
rm $RPM_BUILD_ROOT%{_datadir}/omf/gnome-search-tool/gnome-search-tool-en_GB.omf

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/[a-z]*/[a-z]*
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -f $RPM_BUILD_ROOT%{_datadir}/omf/*/*-??_??.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

# process doc files
cd %{_builddir}/%name-%version/gnome-utils-%{gnome_utils.version}
bzip2 COPYING ChangeLog po/ChangeLog NEWS logview/ChangeLog logview/help/ChangeLog gsearchtool/ChangeLog gsearchtool/help/ChangeLog gnome-screenshot/ChangeLog gnome-dictionary/ChangeLog gnome-dictionary/help/ChangeLog baobab/ChangeLog baobab/help/ChangeLog

# doc files for SUNWngome-log-viewer
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-log-viewer
tar cf - AUTHORS README COPYING.bz2 ChangeLog.bz2 NEWS.bz2 po/ChangeLog.bz2 logview/ChangeLog.bz2 logview/help/ChangeLog.bz2 | ( cd $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-log-viewer; tar xf - )

# doc files for SUNWngome-search-tool
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-search-tool
tar cf - AUTHORS README COPYING.bz2 ChangeLog.bz2 NEWS.bz2 po/ChangeLog.bz2 gsearchtool/AUTHORS gsearchtool/ChangeLog.bz2 gsearchtool/help/ChangeLog.bz2| ( cd $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-search-tool; tar xf - )

# doc files for SUNWngome-search-dictionary
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-dictionary
tar cf - AUTHORS README COPYING.bz2 ChangeLog.bz2 NEWS.bz2 po/ChangeLog.bz2 gnome-dictionary/AUTHORS gnome-dictionary/README gnome-dictionary/ChangeLog.bz2 gnome-dictionary/help/ChangeLog.bz2| ( cd $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-dictionary; tar xf - )

# doc files for SUNWngome-screenshot
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-screenshot
tar cf - AUTHORS README COPYING.bz2 ChangeLog.bz2 NEWS.bz2 po/ChangeLog.bz2 gnome-screenshot/ChangeLog.bz2 | ( cd $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-screenshot; tar xf - )

# doc files for SUNWngome-disk-analyzer
mkdir -p $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-disk-analyzer
tar cf - AUTHORS README COPYING.bz2 ChangeLog.bz2 NEWS.bz2 po/ChangeLog.bz2 baobab/AUTHORS baobab/README baobab/ChangeLog.bz2 baobab/help/ChangeLog.bz2 | ( cd $RPM_BUILD_ROOT%{_datadir}/doc/SUNWgnome-disk-analyzer; tar xf - )

%clean
rm -rf $RPM_BUILD_ROOT

%post -n SUNWgnome-disk-analyzer
%restart_fmri desktop-mime-cache gconf-cache

%postun -n SUNWgnome-disk-analyzer
%restart_fmri desktop-mime-cache

%post -n SUNWgnome-log-viewer
%restart_fmri desktop-mime-cache gconf-cache

%postun -n SUNWgnome-log-viewer
%restart_fmri desktop-mime-cache

%post -n SUNWgnome-search-tool
%restart_fmri desktop-mime-cache gconf-cache

%postun -n SUNWgnome-search-tool
%restart_fmri desktop-mime-cache

%post -n SUNWgnome-dictionary
%restart_fmri desktop-mime-cache gconf-cache

%postun -n SUNWgnome-dictionary
%restart_fmri desktop-mime-cache

%post -n SUNWgnome-screenshot
%restart_fmri desktop-mime-cache gconf-cache

%postun -n SUNWgnome-screenshot
%restart_fmri desktop-mime-cache

%files -n SUNWgnome-log-viewer
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gnome-system-log
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-system-log/C
%{_datadir}/omf/gnome-system-log/gnome-system-log-C.omf
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gnome-system-log.desktop
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*system-log*
%{_mandir}/*/*.conf.4
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-system-log/*
%doc %{_datadir}/doc/SUNWgnome-log-viewer
%dir %attr (0755, root, other) %{_datadir}/doc

%files -n SUNWgnome-log-viewer-devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%files -n SUNWgnome-log-viewer-root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/logview.schemas

%files -n SUNWgnome-search-tool
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gnome-search-tool
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-search-tool/C
%{_datadir}/omf/gnome-search-tool/gnome-search-tool-C.omf
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gnome-search-tool.desktop
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/gsearchtool
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*search*
%doc %{_datadir}/doc/SUNWgnome-search-tool
%dir %attr (0755, root, other) %{_datadir}/doc


%files -n SUNWgnome-search-tool-root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-search-tool.schemas

%files -n SUNWgnome-dictionary
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gnome-dictionary
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgdict*
%{_libdir}/bonobo/servers/GNOME_DictionaryApplet.server
%{_libexecdir}/gnome-dictionary-applet
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gnome-dictionary.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gnome-dictionary/C
%{_datadir}/omf/gnome-dictionary/gnome-dictionary-C.omf
%{_datadir}/gnome-2.0/ui/GNOME_DictionaryApplet.xml
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%{_datadir}/gdict-1.0/*
%{_datadir}/gnome-dictionary/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*dict*
%doc %{_datadir}/doc/SUNWgnome-dictionary
%dir %attr (0755, root, other) %{_datadir}/doc


%files -n SUNWgnome-dictionary-root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-dictionary.schemas

%files -n SUNWgnome-screenshot
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/gnome*screenshot
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-screenshot
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gnome-screenshot.desktop
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*screenshot*
%doc %{_datadir}/doc/SUNWgnome-screenshot
%dir %attr (0755, root, other) %{_datadir}/doc


%files -n SUNWgnome-screenshot-root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gnome-screenshot.schemas

%files -n SUNWgnome-disk-analyzer
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/baobab
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/baobab
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/baobab.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/baobab/C
%{_datadir}/omf/baobab/baobab-C.omf
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/baobab.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/baobab.svg
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*baobab*
%doc %{_datadir}/doc/SUNWgnome-disk-analyzer
%dir %attr (0755, root, other) %{_datadir}/doc


%files -n SUNWgnome-disk-analyzer-root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/baobab.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/[a-z]*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Thu Feb 26 2009 - lin.ma@sun.com
- Move logview manpage installation to basic spec. 
* Wed Sep 24 2008 - matt.keenn@sun.com
- Update copyright again
* Thu Sep 11 2008 - matt.keenn@sun.com
- Update copyright
* Wed Sep 10 2008 - jedy.wang@sun.com
- Remove NoDisplay=true for dictionary item.
* Thu Aug 28 2008 - dave.lin@sun.com
- Uncomment the line %{_datadir}/omf/*/*-[a-z][a-z]_[A-Z][A-Z].omf in %files
  to include share/omf/baobab/baobab-zh_HK.omf & baobab-zh_TW.omf
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Wed Oct 10 2007 - damien.carbery@sun.com
- Remove 'Requires: SUNWgnome-doc-utils' as it is only used during building;
  change SUNWgnome-doc-utils-devel to SUNWgnome-doc-utils to match change in
  SUNWgnome-doc-utils.spec.
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X deps
- delete some unneeded env vars
* Fri Sep 07 2007 - damien.carbery@sun.com
- Remove icons. See bugzilla #470287.
* Thu Aug 16 2007 - damien.carbery@sun.com
- Delete more en_GB files in %install.
* Wed Apr 04 2007 - glynn.foster@sun.com
- Set NoDisplay=true for dictionary item.
* Wed Feb 14 2006 - damien.carbery@sun.com
- Delete en_GB files in %install.
* Wed Feb 14 2007 - damien.carbery@sun.com
- Add to %files l10n to include baobab-en_GB.omf.
* Thu Jan 25 2007 - damien.carbery@sun.com
- Delete *.la in %install. Add SUNWgnome-doc-utils/-devel dependencies so that
  the log viewer is built. Remove the code that deleted %{_localstatedir}
  because it isn't installed.
- Undo removal of SUNWgnome-log-viewer-devel. Will try to find out what pkg
  that SUNWgnome-utils should be added to the dependencies.
* Wed Jan 24 2007 - damien.carbery@sun.com
- Remove SUNWgnome-log-viewer-devel package as no files are installed for it.
  Remove other files that are no longer installed. Remove -f from rm calls.
* Fri Nov 24 2006 - damien.carbery@sun.com
- Update %files (baobab icons) for 2.17.0 tarball.
* Wed Nov 15 2006 - damien.carbery@sun.com
- Remove unneeded chmod call. It changed help xml files to 0755 for no obvious 
  reason.
* Mon Nov 13 2006 - lin.ma@sun.com
- Added logview plugin
* Fri Sep 08 2006 - Matt.Keenan@sun.com
- Remove "rm" of _mandir during %install
* Wed Sep 06 2006 - lin.ma@sun.com
- Turn to NROFF gnome-system-log manpage
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Tue Aug 29 2006 - glynn.foster@sun.com
- Add post/un rules for SUNWgnome-disk-analyzer
* Fri Aug 25 2006 - brian.cameron@sun.com
- Add gnome-panel-screenshot.1 shadown manpage pointing to gnome-screenshot.1
* Wed Aug 16 2006 - damien.carbery@sun.com
- Change 'icons' line in %files to pick up files.
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Tue Aug 08 2006 - damien.carbery@sun.com
- Add Requires list for SUNWgnome-disk-analyzer after check-deps.pl run.
* Sat Jul 29 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWlibgtop/-devel.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Thu Jun 29 2006 - laca@sun.com
- update %post/%preun gconf scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Fri May 12 2006 - damien.carbery@sun.com
- Small update to dependency list after check-deps.pl run.
* Wed May 10 2006 - laca@sun.com
- merge all remaining -share pkg(s) into the base pkg(s)
* Thu May 04 2006 - laca@sun.com
- merge SUNWgnome-screenshot-share into the base SUNWgnome-screenshot
* Fri Apr 21 2006 - brian.cameron@sun.com
- Add gnome-dictionary and gdict-1.0 to dictionary-share package since these
  are needed.
* Thu Apr 20 2006 - lin.ma@sun.com
- Remove gnome-utils-01-disable-logview-dictionary.diff
- Add gnome-utils-01-logview.diff. Enable build logview
* Wed Mar 15 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-component/-devel for ORBit2.
* Tue Mar 14 2006 - damien.carbery@sun.com
- Remove code that deleted gnome-dictionary .a and .la files. No longer present.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sun Jan 22 2006 - damien.carbery@sun.com
- Add gnome-screenshot.desktop, from new tarball.
* Wed Jan 18 2006 - damien.carbery@sun.com
- More %files updates for 2.13.4 tarball (gnome-dictionary related).
* Fri Jan 06 2006 - damien.carbery@sun.com
- Update %files for new tarball, incl adding gnome-dictionary files.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Fri Oct 14 2005 - damien.carbery@sun.com
- Remove javahelp references. Obsolete.
* Wed Sep 14 2005 - laca@sun.com
- define SUNWgnome-screenshot*
- install gconf schemas and add files to -root packages
* Wed Aug 30 2005 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-print(-devel) as required by gnome-utils.
* Fri Jul 01 2005 - laca@sun.com
- remove the gucharmap parts that Brian moved to SUNWgnome-character-map.spec
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Wed Aug 25 2004 - Kazuhiko.Maekawa@sun.com
- Updated files section to extract l10n help contents into l10n pkg
* Wed Aug 18 2004 - damien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Wed Aug 18 2004 - archana.shah@wipro.com
- javahelp also should get installed for gucharmap.
* Tue Jun 22 2004 - shirley.woo@sun.com
- changed install location to /usr/lib and /usr/bin
* Mon Jun 14 2004 - glynn.foster@sun.com
- Enable back gucharmap into the build.
* Wed Jun  2 2004 - shirley.woo@sun.com
- added "BuildRequires: SUNWgnome-panel-devel" to SUNWgnome-character-map so
  gnome-desktop-2.0 can be found during configure
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Mon May 03 2004 - laca@sun.com
- renamed to SUNWgnome-utils.spec, even though none of the packages is
  called SUNWgnome-utils (;
- added SUNWgnome-search-tool* and SUNWgnome-dictionary* package definitions
  and %files.
* Mon Mar 29 2004 - brian.cameron@sun.com
- Corrected packaging so man is installed as root/bin.  This
  corrects install failure.
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Fri Mar 05 2004 - damien.carbery@sun.com
- Add SUNWgnome-character-map package.
