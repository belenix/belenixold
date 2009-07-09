#
# spec file for package SUNWgnome-img-viewer
#
# includes module(s): eog
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: bewitche
#
%include Solaris.inc

%define eog_bindir /usr/bin
%define eog_libdir /usr/lib
%define eog_libexecdir /usr/lib

%use eog = eog.spec

%define _bindir %{eog_bindir}
%define _libexecdir %{eog_libexecdir}
%define _libdir %{eog_libdir}

Name:                    SUNWgnome-img-viewer
Summary:                 GNOME image viewer
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-img-viewer-root
Requires: SUNWgnome-file-mgr
Requires: SUNWgnome-camera
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-panel
Requires: SUNWgnome-vfs
Requires: SUNWjpg
Requires: SUNWlibexif
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWdesktop-cache
Requires: SFElcms
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWjpg-devel
BuildRequires: SUNWlibexif-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-file-mgr-devel
BuildRequires: SUNWgnome-camera-devel
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-themes-devel
BuildRequires: SUNWgtk-doc
BuildRequires: SFElcms-devel

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-img-viewer-root
Requires: SUNWgnome-file-mgr
Requires: SUNWgnome-camera
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-panel
Requires: SUNWgnome-vfs
Requires: SUNWjpg
Requires: SUNWlibexif
Requires: SUNWlibms
Requires: SUNWlibpopt

%prep
rm -rf %name-%version
mkdir %name-%version
%eog.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH="%{_pkg_config_path}:/usr/sfw/lib/pkgconfig"
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -lm -L/usr/sfw/lib -R/usr/sfw/lib"

%eog.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%eog.install -d %name-%version

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

chmod 0755 $RPM_BUILD_ROOT%{_mandir}/man1/eog.1

install -d $RPM_BUILD_ROOT%{eog_libdir}/bonobo/servers

# Remove *.a and *.la
# .a files are no longer installed (2.23.4.1 tarball)
#rm $RPM_BUILD_ROOT%{eog_libdir}/eog/plugins/*.a
rm $RPM_BUILD_ROOT%{eog_libdir}/eog/plugins/*.la

# Never install English locales because should support full functions
# on English locales as same as Solaris.
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/eog/en_GB
rm -r $RPM_BUILD_ROOT%{_datadir}/locale/en_GB
rm $RPM_BUILD_ROOT%{_datadir}/omf/eog/eog-en_GB.omf

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gnome/help/eog/[a-z]*
rm $RPM_BUILD_ROOT%{_datadir}/omf/eog/eog-[a-z][a-z].omf
rm $RPM_BUILD_ROOT%{_datadir}/omf/eog/eog-[a-z][a-z]_[A-Z][A-Z].omf
%endif
# Remove scrollkeeper files.
#rm -r $RPM_BUILD_ROOT/var
#rm -r $RPM_BUILD_ROOT%{_prefix}/var

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}(eog):$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{eog_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{eog_libdir}/bonobo/servers
%{eog_libdir}/eog
# %{eog_libdir}/eog-collection-view
# %{eog_libdir}/eog-image-viewer
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/eog
%{_datadir}/gtk-doc
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
# %{_datadir}/idl
%{_datadir}/omf/*/*-C.omf
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/eog.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/eog.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/eog.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/eog.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/eog.svg
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%doc -d eog-%{eog.version} AUTHORS ChangeLog MAINTAINERS NEWS README THANKS
%doc(bzip2) -d eog-%{eog.version} COPYING
%dir %attr (0755, root, other) %{_datadir}/doc

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/eog/[a-z]*
%{_datadir}/omf/eog/eog-[a-z][a-z].omf
%{_datadir}/omf/eog/eog-[a-z][a-z]_[A-Z][A-Z].omf
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/eog.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Web Mar 04 2009 - chris.wang@sun.com
- Transfer the ownership to bewitche
* Tue Feb 17 2009 - dave.lin@sun.com
- Add BuildRequires: SUNWgnome-themes-devel because it requires gnome-icon-theme.
* Wed Jun 18 2008 - damien.carbery@sun.com
- *.a are no longer installed so comment out their deletion.
* Wed Jun 11 2008 - damien.carbery@sun.com
- Delete *.a/*.la during %install; add %{_datadir}/gtk-doc and
  %{eog_libdir}/eog to %files.
* Wed May 21 2008 - damien.carbery@sun.com
- Add Build/Requires: SUNWlcms after check-deps.pl run.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X dep
* Tue Aug 28 2007 - damien.carbery@sun.com
- Remove pixmaps from %files because they are not installed by new tarball.
* Sat Aug 18 2007 - damien.carbery@sun.com
- Comment out removal of /var and /usr/var dirs as they are no longer installed.
* Thu Aug 16 2007 - damien.carbery@sun.com
- Remove actions icons from %files after tarball bump.
* Wed Jul 11 2007 - damien.carbery@sun.com
- Add eog-image-collection.png and thumbnail-frame.png to %files.
* Wed May 16 2007 - damien.carbery@sun.com
- Add devel package; add icons to base package.
* Thu May 10 2007 - damien.carbery@sun.com
- Remove pixmaps dir from %files as it is no longer populated.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Wed Feb 14 2006 - damien.carbery@sun.com
- Delete en_GB files in %install.
* Thu Jan 11 2006 - damien.carbery@sun.com
- Add new icons to %files.
* Wed Dec 13 2006 - damien.carbery@sun.com
- Delete some l10n omf files in %install when not building l10n packages.
* Wed Dec 06 2006 - damien.carbery@sun.com
- Update packaging for new tarball - remove scrollkeeper files, add omf files
  to the l10n package.
* Wed Nov 29 2006 - damien.carbery@sun.com
- Fix packaging as some locales have been removed.
* Fri Oct 20 2006 - damien.carbery@sun.com
- Fix packaging for new locales.
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Fri Jul 28 2006 - damien.carbery@sun.com
- Remove scrollkeeper files before packaging. Update l10n package as some 
  files are no longer installed.
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Fri Jun  2 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Tue May 09 2006 - damien.carbery@sun.com
- Move gthumb to spec-files-extra/SUNWgnome-img-organizer as it has been EOL'd.
* Mon May 01 2006 - damien.carbery@sun.com
- Add %{_datadir}/icons to share package.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Wed Feb 15 2006 - damien.carbery@sun.com
- Set PKG_CONFIG_PATH to find libgphoto; Set LDFLAGS to link with libpng.
* Sat Jan 28 2006 - damien.carbery@sun.com
- Add BuildRequires for '-devel' equivalents of the Requires packages.
- Added BuildRequires SUNWgnome-camera-devel for gthumb.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Mon Oct 03 2005 - damien.carbery@sun.com
- Remove unpackaged files.
* Sat Dec 18 2004 - damien.carbery@sun.com
- Move gthumb to /usr/sfw per ARC decision.
* Sun Nov 14 2004 - laca@sun.com
- move gthumb to /usr/demo/jds
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Mon Jun 26 2004  shirley.woo@sun.com
- change eog.1 permissions to 0755 for Solaris integration error
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Tue May 18 2004 - laca@sun.com
- add sfw to LDFLAGS/CPPFLAGS (patch from Shirley)
* Tue May 11 2004 - brian.cameron@sun.com
- add %{_datadir}/eog to files share so glade files
  get installed.  This corrects core dumping problem
  when bringing up preferences dialog.
* Tue May 04 2004 - laca@sun.com
- add SUNWgnome-camera dependency
* Fri Mar 26 2004 - laca@sun.com
- add SUNWgnome-file-mgr dependency (for eel)
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Mon Mar 01 2004 - <laca@sun.com>
- fix dependencies
- define PERL5LIB
- file %files share
* Mon Feb 23 2004 - <niall.power@sun.com>
- install gconf schemas at the end of the install stage
