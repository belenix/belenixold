#
# spec file for package SUNWgnome-themes
#
# includes module(s): hicolor-icon-theme,  gnome-themes, gtk2-engines,
# blueprint, nimbus, sun-gdm-themes, gnome-icon-theme
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: erwannc
#
%include Solaris.inc
%ifarch amd64 sparcv9
%include arch64.inc
%use engines_64 = gtk2-engines.spec
%if %option_with_blueprint
%use blueprint_64 = blueprint.spec
%endif
%use nimbus_64 = nimbus.spec
%endif

%include base.inc
%use icon_naming = icon-naming-utils.spec
%use tango = tango-icon-theme.spec
%use hicolor = hicolor-icon-theme.spec
%use engines = gtk2-engines.spec
%use gthemes = gnome-themes.spec
%use dmz_cursor = dmz-cursor.spec
%use dmz_cursor_aa = dmz-cursor-aa.spec
%if %option_with_blueprint
%use blueprint = blueprint.spec
%endif
%use nimbus = nimbus.spec
%if %option_with_sun_branding
%use gdmtheme = sun-gdm-themes.spec
%endif
%if %option_with_indiana_branding
%use gdmtheme = opensolaris-gdm-themes.spec
%use neutralplus = neutral-plus-cursors.spec
%endif
%use icontheme = gnome-icon-theme.spec
%use backgrounds = gnome-backgrounds.spec
%if %option_with_indiana_branding
%use brandedbackgrounds = opensolaris-backgrounds.spec
%endif
%if %option_with_sun_branding
%use brandedbackgrounds = sun-backgrounds.spec
%endif
Name:                    SUNWgnome-themes
Summary:                 GNOME themes and support libraries
Version:                 %{default_pkg_version}
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-base-libs
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWfreetype2
Requires: SUNWlibpopt
Requires: SUNWpng
Requires: SUNWTiff
Requires: SUNWjpg
Requires: SUNWdesktop-cache
Requires: SUNWbash
BuildRequires: SUNWimagick
BuildRequires: SUNWperl-xml-parser
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWlibpopt-devel

%package hires
Summary:                 GNOME themes - high resolution icons
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %{name}

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-themes
Requires: SUNWperl584usr
Requires: SUNWperl584core
Requires: SUNWlibms
Requires: SUNWperl-xml-parser
Requires: SUNWgnome-themes-devel

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
%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%engines_64.prep -d %name-%version/%_arch64
%if %option_with_blueprint
%blueprint_64.prep -d %name-%version/%_arch64
%endif
%nimbus_64.prep -d %name-%version/%_arch64
%endif

mkdir %name-%version/%base_arch
%icon_naming.prep -d %name-%version/%base_arch
%tango.prep -d %name-%version/%base_arch
%hicolor.prep -d %name-%version/%base_arch
%engines.prep -d %name-%version/%base_arch
%gthemes.prep -d %name-%version/%base_arch
%dmz_cursor.prep -d %name-%version/%base_arch
%dmz_cursor_aa.prep -d %name-%version/%base_arch
%if %option_with_blueprint
%blueprint.prep -d %name-%version/%base_arch
%endif
%nimbus.prep -d %name-%version/%base_arch
%gdmtheme.prep -d %name-%version/%base_arch
%if %option_with_indiana_branding
%neutralplus.prep -d %name-%version/%base_arch
%endif
%icontheme.prep -d %name-%version/%base_arch
%backgrounds.prep -d %name-%version/%base_arch
%brandedbackgrounds.prep -d %name-%version/%base_arch

%build
export PKG_CONFIG=/usr/bin/pkg-config
PKG_CONFIG_DISABLE_UNINSTALLED=
unset PKG_CONFIG_DISABLE_UNINSTALLED
export EXTRA_CFLAGS="-I/usr/sfw/include -DANSICPP"
export CPPFLAGS="-I/usr/sfw/include"
export EXTRA_LDFLAGS="-L/usr/sfw/lib -R/usr/sfw/lib"
export PERL=/usr/perl5/bin/perl
%icon_naming.build -d %name-%version/%base_arch

export INU_DATA_DIR=%{_builddir}/%name-%version/%base_arch/icon-naming-utils-%{icon_naming.version}
chmod a+x $INU_DATA_DIR/icon-name-mapping
export PATH=$INU_DATA_DIR:$PATH

%ifarch amd64 sparcv9
export PKG_CONFIG_PATH=../../%{_arch64}/gtk-engines-%{engines.version}:%{_builddir}/%name-%version/%{base_arch}/icon-naming-utils-%{icon_naming.version}:/usr/lib/%{_arch64}/pkgconfig
%engines_64.build -d %name-%version/%_arch64
%if %option_with_blueprint
%blueprint_64.build -d %name-%version/%_arch64
%endif
%nimbus_64.build -d %name-%version/%_arch64
%endif

export PKG_CONFIG_PATH=../../%{base_arch}/gtk-engines-%{engines.version}:%{_builddir}/%name-%version/%{base_arch}/icon-naming-utils-%{icon_naming.version}:%{_pkg_config_path}

%tango.build -d %name-%version/%base_arch
%hicolor.build -d %name-%version/%base_arch
%engines.build -d %name-%version/%base_arch
%gthemes.build -d %name-%version/%base_arch
%if %option_with_indiana_branding
%neutralplus.build -d %name-%version/%base_arch
%endif
%if %option_with_blueprint
%blueprint.build -d %name-%version/%base_arch
%endif
%nimbus.build -d %name-%version/%base_arch
%gdmtheme.build -d %name-%version/%base_arch
%icontheme.build -d %name-%version/%base_arch
%backgrounds.build -d %name-%version/%base_arch
%brandedbackgrounds.build -d %name-%version/%base_arch

%install
rm -rf $RPM_BUILD_ROOT

%icon_naming.install -d %name-%version/%base_arch
export INU_DATA_DIR=%{_builddir}/%name-%version/%{base_arch}/icon-naming-utils-%{icon_naming.version}
export PATH=$INU_DATA_DIR:$PATH

%ifarch amd64 sparcv9
%engines_64.install -d %name-%version/%_arch64
%if %option_with_blueprint
%blueprint_64.install -d %name-%version/%_arch64
%endif
%nimbus_64.install -d %name-%version/%_arch64
%endif

%tango.install -d %name-%version/%base_arch
%hicolor.install -d %name-%version/%base_arch
%engines.install -d %name-%version/%base_arch
%gthemes.install -d %name-%version/%base_arch
%dmz_cursor.install -d %name-%version/%base_arch
%dmz_cursor_aa.install -d %name-%version/%base_arch
%if %option_with_indiana_branding
%neutralplus.install -d %name-%version/%base_arch
%endif
%if %option_with_blueprint
%blueprint.install -d %name-%version/%base_arch
%endif
%nimbus.install -d %name-%version/%base_arch
%gdmtheme.install -d %name-%version/%base_arch
%icontheme.install -d %name-%version/%base_arch
%backgrounds.install -d %name-%version/%base_arch
%brandedbackgrounds.install -d %name-%version/%base_arch
chmod 0755 $RPM_BUILD_ROOT%{_datadir}/icons/HighContrastLargePrint/48x48/apps/perfmeter.png
chmod 0755 $RPM_BUILD_ROOT%{_datadir}/icons/HighContrastLargePrintInverse/48x48/apps/perfmeter.png

rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

# Remove branded icons that push out the size of the panel - these need to
# be fixed in the nimbus theme. Also remove the Tango icons, since they are
# 2 feet rather than the GNOME icon
%if %option_with_indiana_branding
rm $RPM_BUILD_ROOT%{_datadir}/icons/nimbus/48x48/apps/gnome-main-menu.png
rm $RPM_BUILD_ROOT%{_datadir}/icons/nimbus/32x32/places/gnome-main-menu.png
rm $RPM_BUILD_ROOT%{_datadir}/icons/Tango/16x16/places/gnome-main-menu.png
rm $RPM_BUILD_ROOT%{_datadir}/icons/Tango/22x22/places/gnome-main-menu.png
rm $RPM_BUILD_ROOT%{_datadir}/icons/Tango/24x24/places/gnome-main-menu.png
rm $RPM_BUILD_ROOT%{_datadir}/icons/Tango/32x32/places/gnome-main-menu.png
%endif

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT%{_libdir}}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%if %option_with_blueprint
%doc -d %{base_arch} blueprint-%{blueprint.version}/README
%doc -d %{base_arch} blueprint-%{blueprint.version}/AUTHORS
%doc(bzip2) -d %{base_arch} blueprint-%{blueprint.version}/COPYING
%doc(bzip2) -d %{base_arch} blueprint-%{blueprint.version}/NEWS
%doc(bzip2) -d %{base_arch} blueprint-%{blueprint.version}/ChangeLog
%doc(bzip2) -d %{base_arch} blueprint-%{blueprint.version}/icons/ChangeLog
%doc(bzip2) -d %{base_arch} blueprint-%{blueprint.version}/po/ChangeLog
%endif
%doc -d %{base_arch} gnome-backgrounds-%{backgrounds.version}/README
%doc -d %{base_arch} gnome-backgrounds-%{backgrounds.version}/AUTHORS
%doc(bzip2) -d %{base_arch} gnome-backgrounds-%{backgrounds.version}/COPYING
%doc(bzip2) -d %{base_arch} gnome-backgrounds-%{backgrounds.version}/NEWS
%doc(bzip2) -d %{base_arch} gnome-backgrounds-%{backgrounds.version}/ChangeLog
%doc(bzip2) -d %{base_arch} gnome-backgrounds-%{backgrounds.version}/po/ChangeLog
%doc -d %{base_arch} gnome-icon-theme-%{icontheme.version}/README
%doc -d %{base_arch} gnome-icon-theme-%{icontheme.version}/AUTHORS
%doc(bzip2) -d %{base_arch} gnome-icon-theme-%{icontheme.version}/COPYING
%doc(bzip2) -d %{base_arch} gnome-icon-theme-%{icontheme.version}/NEWS
%doc(bzip2) -d %{base_arch} gnome-icon-theme-%{icontheme.version}/ChangeLog
%doc(bzip2) -d %{base_arch} gnome-icon-theme-%{icontheme.version}/po/ChangeLog
%doc -d %{base_arch} gnome-themes-%{gthemes.version}/README
%doc -d %{base_arch} gnome-themes-%{gthemes.version}/AUTHORS
%doc(bzip2) -d %{base_arch} gnome-themes-%{gthemes.version}/COPYING
%doc(bzip2) -d %{base_arch} gnome-themes-%{gthemes.version}/NEWS
%doc(bzip2) -d %{base_arch} gnome-themes-%{gthemes.version}/ChangeLog
%doc(bzip2) -d %{base_arch} gnome-themes-%{gthemes.version}/po/ChangeLog
%doc -d %{base_arch} gtk-engines-%{engines.version}/README
%doc -d %{base_arch} gtk-engines-%{engines.version}/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/clearlooks/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/crux/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/glide/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/hc/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/industrial/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/lua/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/mist/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/redmond/AUTHORS
%doc -d %{base_arch} gtk-engines-%{engines.version}/engines/thinice/AUTHORS
%doc(bzip2) -d %{base_arch} gtk-engines-%{engines.version}/COPYING
%doc(bzip2) -d %{base_arch} gtk-engines-%{engines.version}/NEWS
%doc(bzip2) -d %{base_arch} gtk-engines-%{engines.version}/ChangeLog
%doc(bzip2) -d %{base_arch} gtk-engines-%{engines.version}/po/ChangeLog
%doc -d %{base_arch} hicolor-icon-theme-%{hicolor.version}/README
%doc(bzip2) -d %{base_arch} hicolor-icon-theme-%{hicolor.version}/COPYING
%doc(bzip2) -d %{base_arch} hicolor-icon-theme-%{hicolor.version}/ChangeLog
%doc -d %{base_arch} icon-naming-utils-%{icon_naming.version}/README
%doc -d %{base_arch} icon-naming-utils-%{icon_naming.version}/AUTHORS
%doc(bzip2) -d %{base_arch} icon-naming-utils-%{icon_naming.version}/COPYING
%doc(bzip2) -d %{base_arch} icon-naming-utils-%{icon_naming.version}/NEWS
%doc(bzip2) -d %{base_arch} icon-naming-utils-%{icon_naming.version}/ChangeLog
%doc -d %{base_arch} nimbus-%{nimbus.version}/README
%doc -d %{base_arch} nimbus-%{nimbus.version}/AUTHORS
%doc(bzip2) -d %{base_arch} nimbus-%{nimbus.version}/COPYING
%doc(bzip2) -d %{base_arch} nimbus-%{nimbus.version}/NEWS
%doc(bzip2) -d %{base_arch} nimbus-%{nimbus.version}/ChangeLog
%doc(bzip2) -d %{base_arch} nimbus-%{nimbus.version}/po/ChangeLog
%if %option_with_indiana_branding
%doc -d %{base_arch} opensolaris-backgrounds-%{brandedbackgrounds.version}/README
%doc -d %{base_arch} opensolaris-backgrounds-%{brandedbackgrounds.version}/AUTHORS
%doc(bzip2) -d %{base_arch} opensolaris-backgrounds-%{brandedbackgrounds.version}/COPYING
%doc(bzip2) -d %{base_arch} opensolaris-backgrounds-%{brandedbackgrounds.version}/NEWS
%doc(bzip2) -d %{base_arch} opensolaris-backgrounds-%{brandedbackgrounds.version}/ChangeLog
%doc(bzip2) -d %{base_arch} opensolaris-backgrounds-%{brandedbackgrounds.version}/po/ChangeLog
%endif
%if %option_with_sun_branding
%doc -d %{base_arch} sun-backgrounds-%{brandedbackgrounds.version}/README
%doc -d %{base_arch} sun-backgrounds-%{brandedbackgrounds.version}/AUTHORS
%doc(bzip2) -d %{base_arch} sun-backgrounds-%{brandedbackgrounds.version}/COPYING
%doc(bzip2) -d %{base_arch} sun-backgrounds-%{brandedbackgrounds.version}/NEWS
%doc(bzip2) -d %{base_arch} sun-backgrounds-%{brandedbackgrounds.version}/ChangeLog
%doc(bzip2) -d %{base_arch} sun-backgrounds-%{brandedbackgrounds.version}/po/ChangeLog
%endif
%if %option_with_indiana_branding
%doc -d %{base_arch} opensolaris-gdm-themes-%{gdmtheme.version}/README
%doc -d %{base_arch} opensolaris-gdm-themes-%{gdmtheme.version}/AUTHORS
%doc(bzip2) -d %{base_arch} opensolaris-gdm-themes-%{gdmtheme.version}/COPYING
%doc(bzip2) -d %{base_arch} opensolaris-gdm-themes-%{gdmtheme.version}/NEWS
%doc(bzip2) -d %{base_arch} opensolaris-gdm-themes-%{gdmtheme.version}/ChangeLog
%doc(bzip2) -d %{base_arch} opensolaris-gdm-themes-%{gdmtheme.version}/po/ChangeLog
%endif
%if %option_with_sun_branding
%doc -d %{base_arch} sun-gdm-themes-%{gdmtheme.version}/README
%doc -d %{base_arch} sun-gdm-themes-%{gdmtheme.version}/AUTHORS
%doc(bzip2) -d %{base_arch} sun-gdm-themes-%{gdmtheme.version}/COPYING
%doc(bzip2) -d %{base_arch} sun-gdm-themes-%{gdmtheme.version}/NEWS
%doc(bzip2) -d %{base_arch} sun-gdm-themes-%{gdmtheme.version}/ChangeLog
%doc(bzip2) -d %{base_arch} sun-gdm-themes-%{gdmtheme.version}/po/ChangeLog
%endif
%doc -d %{base_arch} tango-icon-theme-%{tango.version}/README
%doc -d %{base_arch} tango-icon-theme-%{tango.version}/AUTHORS
%doc(bzip2) -d %{base_arch} tango-icon-theme-%{tango.version}/COPYING
%doc(bzip2) -d %{base_arch} tango-icon-theme-%{tango.version}/NEWS
%doc(bzip2) -d %{base_arch} tango-icon-theme-%{tango.version}/ChangeLog
%doc(bzip2) -d %{base_arch} tango-icon-theme-%{tango.version}/po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gtk-*/2.*/engines/*.so
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/gtk-*/2.*/engines/*.so
%endif
%dir %attr (0755, root, sys) %{_datadir}
%if %option_with_indiana_branding
%{_datadir}/gdm
%endif
%if %option_with_sun_branding
%{_datadir}/gdm
%endif
%{_datadir}/gtk-engines
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/Crux
%dir %attr (0755, root, other) %{_datadir}/icons/HighContrast
%dir %attr (0755, root, other) %{_datadir}/icons/HighContrast-SVG
%dir %attr (0755, root, other) %{_datadir}/icons/HighContrastInverse
%dir %attr (0755, root, other) %{_datadir}/icons/HighContrastLargePrint
%dir %attr (0755, root, other) %{_datadir}/icons/HighContrastLargePrintInverse
%dir %attr (0755, root, other) %{_datadir}/icons/LargePrint
%dir %attr (0755, root, other) %{_datadir}/icons/Mist
%dir %attr (0755, root, other) %{_datadir}/icons/Tango
%dir %attr (0755, root, other) %{_datadir}/icons/gnome
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%dir %attr (0755, root, other) %{_datadir}/icons/nimbus
%if %option_with_blueprint
%dir %attr (0755, root, other) %{_datadir}/icons/blueprint
%endif
# exclude index.theme from Neutral_Plus_Inv because it's listed later
%if %option_with_indiana_branding
%attr (-, root, other) %{_datadir}/icons/Neutral_Plus_Inv/[CLcs]*
%endif
%attr (-, root, other) %{_datadir}/icons/DMZ-Black
%attr (-, root, other) %{_datadir}/icons/DMZ-White
%attr (-, root, bin) %{_datadir}/icons/*/index.theme
%attr (-, root, other) %{_datadir}/icons/*/scalable
%attr (-, root, other) %{_datadir}/icons/*/8x8
%attr (-, root, other) %{_datadir}/icons/*/12x12
%attr (-, root, other) %{_datadir}/icons/*/16x16
%attr (-, root, other) %{_datadir}/icons/*/20x20
%attr (-, root, other) %{_datadir}/icons/*/22x22
%attr (-, root, other) %{_datadir}/icons/*/24x24
%attr (-, root, other) %{_datadir}/icons/*/32x32
%attr (-, root, other) %{_datadir}/icons/*/36x36
%attr (-, root, other) %{_datadir}/icons/*/48x48
%attr (-, root, other) %{_datadir}/icons/*/64x64
%attr (-, root, other) %{_datadir}/icons/*/72x72
%if %option_with_blueprint
%attr (-, root, other) %{_datadir}/icons/blueprint/stock
%endif
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%{_datadir}/themes
%{_datadir}/gnome-background-properties
%{_datadir}/dtds
%{_datadir}/icon-naming-utils

%files hires
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/icons
%dir %attr (0755, root, other) %{_datadir}/icons/nimbus
%dir %attr (0755, root, other) %{_datadir}/icons/hicolor
%attr (-, root, other) %{_datadir}/icons/*/96x96
%attr (-, root, other) %{_datadir}/icons/*/128x128
%attr (-, root, other) %{_datadir}/icons/*/192x192

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/icon-name-mapping
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/pkgconfig
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*
%endif

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%preun
find $BASEDIR/share/icons -name icon-theme.cache -exec /bin/rm -f {} \;

%post
%restart_fmri icon-cache

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 24 2009 - jeff.cai@sun.com
- Since /usr/lib/amd64/pkgconfig/gtk-engines-2.pc requires /usr/lib/amd64
  /pkgconfig/gtk+-2.0.pc, add the dependency of SUNWgnome-base-libs-devel
* Mon Mar 23 2009 - jeff.cai@sun.com
- Since /usr/share/icons/Neutral_Plus_Inv/source/make.sh (SUNWgnome-themes)
  requires /usr/bin/bash which is found in SUNWbash, add the dependency.
* Wed Feb 18 2009 - dave.lin@sun.com
- Removed %doc gtk-engines:COPYING.GPL/LGPL which were n/a in 2.17.3.
* Wed Sep 17 2008 - ghee.teo@sun.com
- Modified to add new copyright format to %files.
* Fri Aug 29 2008 - dave.lin@sun.com
- use option --with-blueprint for the line 
    %{_datadir}/icons/blueprint
- use option --with-indiana-branding for the line
    %{_datadir}/icons/Neutral_Plus_Inv/[CLcs]*
* Fri Aug 22 2008 - dave.lin@sun.com
- fix the attribute issue of dirs under share/icons
* Fri Aug 22 2008 - laca@sun.com
- fix build when blueprint is included
* Fri Aug 22 2008 - dave.lin@sun.com
- Exclude Neutral_Plus_Inv/* in %files which doesn't get installed.
* Thu Aug 21 2008 - laca@sun.com
- split the high resolution icons into SUNWgnome-themes-hires to reduce
  disk space requirements on the OpenSolaris live cd.
* Mon Jan 21 2007 - glynn.foster@sun.com
- Split out the OpenSolaris and Sun backgrounds into their
  own individual spec files - build one depending on desired
  branding.
* Fri Jan 18 2007 - glynn.foster@sun.com
- add in neutral plus cursor theme
* Sun Dec 16 2007 - laca@sun.com
- add datadir/gdm to files if either sun or indiana branding is
  requested
* Wed Oct 10 2007 - laca@sun.com
- change the inline postinstall script to an include
* Tue Oct  2 2007 - laca@sun.com
- set different PKG_CONFIG_PATHs for 32-bit and 64-bit
* Fri Sep 28 2007 - laca@sun.com
- disable building blueprint when the --without-blueprint option is used
- disable building sun-gdm-themes when --with-sun-branding is not used
* Fri May 18 2007 - laca@sun.com
- add 64-bit versions of theme engines
* Thu Apr 26 2007 - laca@sun.com
- set PERL for icon-naming-utils, part of 6454456
* Wed Mar 14 2007 - damien.carbery@sun.com
- Add %{_datadir}/gtk-engines to %files for new xml files.
* Wed Mar 07 2007 - damien.carbery@sun.com
- Use full path to icon-naming-utils build dir in PKG_CONFIG_PATH to be able to
  get full path to icon-name-mapping script.
* Tue Mar 06 2007 - damien.carbery@sun.com
- Rename ICON_NAME_MAPPING_DIR var to INU_DATA_DIR after bumping
  icon-name-mapping.
* Mon Aug 14 2006 - damien.carbery@sun.com
- Fix path to icons dir in %preun.
* Sat Aug 12 2006 - laca@sun.com
- change datadir/icons permissions back to root:other since it's a stable
  interface and wasn't supposed to be changed
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Fri Feb 17 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Jan 31 2006 - damien.carbery@sun.com
- Remove ref to LowContrastLargePrint/48x48/apps/perfmeter.png as not installed
* Fri Jan 06 2006 - damien.carbery@sun.com
- Move %files around, including adding %{_datadir}/pkgconfig. For new tarballs.
- Set PATH for %install section so icon-name-mapping is found.
* Wed Dec 20 2005 - damien.carbery@sun.com
- Update PKG_CONFIG_PATH to find icon-naming-utils dir for tango-icon-theme.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs gtk-update-icon-cache
* Tue Sep 20 2005 - glynn.foster@sun.com
- Add gnome-backgrounds
* Fri Sep 09 2005 - laca@sun.com
- remove unpackaged files
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Tue Aug 24 2004 - brian.cameron@sun.com
- No longer package blueprint docs since the AUTHORS, COPYING, ChangeLog,
  NEWS and README files aren't really useful.
* Wed Aug 18 2004 - damien.carbery@sun.com
- Change perms for some png files for Solaris integration.
* Mon Jul 12 2004 - damien.carbery@sun.com
- Unset perms for /usr/share/pixmaps.
* Sat Jul 10 2004 - damien.carbery@sun.com
- Set perms for /usr/share/pixmaps.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Fri Jun 25 2004 - hidetoshi.tajima@sun.com
- set ACLOCAL_FLAGS for gnome-themes build
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- add %{_datadir}/locale to install l10n messages
* Fri Mar 26 2004 - laca@sun.com
- update gtk engine directory for 2.4.0
* Fri Mar 12 2004 - Niall.Power@sun.com
- add missing pkgconfig files
* Thu Feb 26 2004 - Niall.Power@sun.com
- add -R%{_libdir} to LDFLAGS
- set PERL5LIB for XML:Parser
- add hicolor build stage
* Thu Feb 19 2004 - Niall.Power@sun.com
- initial Sun release.
