#
# spec file for package SUNWgnome-a11y-gok
#
# includes module(s): gok
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: liyuan
#
%include Solaris.inc

%use gok = gok.spec

Name:                    SUNWgnome-a11y-gok
Summary:                 GNOME On-screen Keyboard
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-a11y-libs
Requires: SUNWgnome-a11y-gok-root
Requires: SUNWgnome-panel
Requires: SUNWgnome-libs
Requires: SUNWgnome-a11y-speech
Requires: SUNWgnome-audio
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWlibms
Requires: SUNWlxml
Requires: SUNWdesktop-cache
BuildRequires: SUNWgnome-audio-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-a11y-speech-devel
BuildRequires: SUNWgnome-panel-devel
BuildRequires: SUNWgnome-libs-devel

%package root
Summary:                 %{summary} - / filesystem
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
%gok.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar -xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export LDFLAGS="%_ldflags"
%ifarch sparc
export CFLAGS="%optflags -I%{_includedir}"
%else
export CFLAGS="%optflags -xO2 -I%{_includedir}"
%endif
%if %option_with_fox
# for <X11/extensions/XInput.h>
export CFLAGS="$CFLAGS -I/usr/X11/include"
%endif
export RPM_OPT_FLAGS="$CFLAGS"
%gok.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
%gok.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

%if %build_l10n
%else
# REMOVE l10n FILES
rm -r $RPM_BUILD_ROOT%{_datadir}/locale
rm -r $RPM_BUILD_ROOT%{_datadir}/gok/ang
rm -r $RPM_BUILD_ROOT%{_datadir}/gok/[a-z][a-z]
rm -r $RPM_BUILD_ROOT%{_datadir}/gok/[a-z][a-z]_[A-Z][A-Z]
rm -r $RPM_BUILD_ROOT%{_datadir}/gok/sr@latin
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):unsupported" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache icon-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/bonobo
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%doc -d gok-%{gok.version} README AUTHORS
%doc(bzip2) -d gok-%{gok.version} COPYING NEWS ChangeLog
%dir %attr (0755, root, other) %{_datadir}/doc
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gok/C
%{_datadir}/gok/C/*.kbd
%{_datadir}/gok/*.png
%{_datadir}/gok/*.kbd
%{_datadir}/gok/*.rc
%{_datadir}/gok/*.txt
%{_datadir}/gok/*.xam
%{_datadir}/gok/*.wav
%{_datadir}/gok/glade
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/gok.png
%{_datadir}/omf/gok/gok-C.omf
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gok.schemas

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_datadir}/gok
%{_datadir}/gok/[a-z][a-z]
%{_datadir}/gok/[a-z][a-z]_[A-Z][A-Z]
%{_datadir}/gok/ang
%{_datadir}/gok/mai
%{_datadir}/gok/sr@latin
%defattr (-, root, other)
%{_datadir}/locale/[a-z][a-z]
%{_datadir}/locale/[a-z][a-z]_[A-Z][A-Z]
%{_datadir}/locale/ang
%{_datadir}/locale/mai
%{_datadir}/locale/sr@latin
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Tue Mar 24 2009 - takao.fujiwara@sun.com
- Add %{_datadir}/gok/C/*.kbd. doo 2552.
* Tue Mar 17 2009 - dave.lin@sun.com
- Add %{_datadir}/mai, %{_datadir}/locale/mai dir in %file l10n.
* Thu Sep 18 2008 - li.yuan@sun.com
- Added %doc to %files for copyright.
* Mon Sep 01 2008 - christian.kelly@sun.com
- Change dirs sr@Latn to sr@latin.
* Mon Mar 31 2008 - li.yuan@sun.com
- Add copyright file
* Thu Jan 10 2008 - li.yuan@sun.com
- change owner to liyuan.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Mon Nov 05 2007 - li.yuan@sun.com
- Use icon-cache.script for %post. Change the inline post script
  to an include.
* Fri Oct 12 1007 - laca@sun.com
- add /usr/X11/include to CFLAGS when built with FOX
* Fri Sep 28 2007 - laca@sun.com
- delete SUNWxwrtl dep
* Mon May 28 2007 - damien.carbery@sun.com
- Add hicolor dir to %files.
* Tue Jan 30 2007 - brian.cameron@sun.com
- Remove the 'ang' locale files when not doing l10n build.
* Tue Jan 23 2007 - damien.carbery@sun.com
- Add 'ang' locale.
* Fri Sep 01 2006 - matt.keenan@sun.com
- New man page tarball
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Fri Jul 14 2006 - damien.carbery@sun.com
- Add %{_datadir}/locale to l10n package, byproduct of intltool update.
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Mon Jun 26 2006 - laca@sun.com
- move back to /usr, part of CR 6412650
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Wed May 31 2006 - damien.carbery@sun.com
- Change dirs in base and l10n packages as l10n files have been moved around
  for the 1.0.10 tarball.
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Tue May 09 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Complete update of Build/Requires after running check-deps.pl script.
* Thu Feb 16 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Mon Dec 13 2004 - damien.carbery@sun.com
- Move to /usr/sfw to implement ARC decision.
* Fri Nov 19 2004 - damien.carbery@sun.com
- Fix for 6197815: move unsupported app to /usr/demo/jds.
* Fri Nov 12 2004 - kazuhiko.maekawa@sun.com
- Added workaround fix for 6193354
* Wed Oct 06 2004 - matt.keenan@sun.com
- added l10n help files
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Thu Sep 09 2004  matt.keenan@sun.com
- Added create-branching-keyboard.1, gok.1 manpages
* Thu Aug 26 2004  damien.carbery@sun.com
- Lower optimization level on x86 to fix 5086691 - data corruption otherwise.
  -xO2 will take precedence over -xO4 because it is later in CFLAGS.
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Wed Jun 23 2004 - muktha.narayan@wipro.com
- Install schema files.
* Wed Jun  2 2004 - takao.fujiwara@sun.com
- Added %{_datadir}/locale to install l10n messages
* Tue May 18 2004 - laca@sun.com
- add gnome-speech dependency
* Tue Mar 23 2004 - laca@sun.com
- remove gtk-doc from %files
* Tue Mar 02 2004 - laca@sun.com
- add dependency on SUNWgnome-panel
* Fri Feb 27 2004 - laca@sun.com
- add %defattr for share subpkg
* Thu Feb 26 2004 - laca@sun.com
- add share %package
- define PERL5LIB for XML::Parser
