#
# spec file for package SUNWgnome-img-organizer
#
# includes module(s): gthumb
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: jerrytan

%include Solaris.inc

%use gthumb = gthumb.spec

Name:                    SUNWgnome-img-organizer
Summary:                 GNOME image organizer (gthumb)
Version:                 %{default_pkg_version}
SUNW_Copyright:          %{name}.copyright
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-print
Requires: SUNWgnome-img-organizer-root
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

%prep
rm -rf %name-%version
mkdir %name-%version
%gthumb.prep -d %name-%version

%build
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export CPPFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -lm -L/usr/sfw/lib -R/usr/sfw/lib"

%gthumb.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gthumb.install -d %name-%version

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}(gthumb):$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT/usr}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%doc -d gthumb-%{gthumb.version} README AUTHORS
%doc(bzip2) -d gthumb-%{gthumb.version} ChangeLog NEWS doc/ChangeLog po/ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgthumb.so
%{_libdir}/bonobo/servers/GNOME_GThumb.server
%{_libdir}/gthumb/modules/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%{_datadir}/gthumb
%dir %attr(0755, root, other) %{_datadir}/icons
%dir %attr(0755, root, other) %{_datadir}/icons/hicolor
%dir %attr(0755, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr(0755, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/gthumb.png
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gthumb/[a-z][a-z]
%endif

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gthumb.schemas

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Wed May 07 2008 - damien.carbery@sun.com
- Remove PERL5LIB setting as it is not necessary.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Fri Sep 28 2007 - laca@sun.com
- delete Nevada X dep
* Tue Aug 28 2007 - damien.carbery@sun.com
- Update %files with GNOME_GThumb.server as installed by the new tarball.
* Tue Apr 24 2007 - laca@sun.com
- use $BASEDIR instead of $PKG_INSTALL_ROOT to fix diskless install
  (CR 6537817)
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Tue Mar 20 2007 - damien.carbery@sun.com
- Update %files for new tarball (remove the %{datadir}/application-registry
  dir).
* Mon Mar 14 2007 - laca@sun.com
- update postrun scripts to the latest and greatest
- delete some unnecessary env variables
* Mon Feb 19 2007 - damien.carbery@sun.com
- Minor updates for new gthumb tarball.
* Wed Oct 11 2006 - laca@sun.com
- fix icondir permissions
* Fri Jun  2 2006 - laca@sun.com
- use post/postun scripts to install schemas into the merged gconf files
* Thu May 11 2006 - laca@sun.com
- kill -share pkg, remove eog.1 man page.
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
* Tue Nov 29 2005 - laca.com
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
