#
# spec file for package SUNWgnome-character-map
#
# includes module(s): gucharmap
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: dkenny
#
%include Solaris.inc

%use gucharmap = gucharmap.spec

Name:                    SUNWgnome-character-map
Summary:                 GNOME character map utility
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-doc-utils
Requires: SUNWdesktop-cache
Requires: %{name}-root

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: SUNWgnome-character-map
Requires: SUNWperl584usr
Requires: SUNWlibms

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
%gucharmap.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags -I%{_includedir}"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
%gucharmap.build -d %name-%version

%install
%gucharmap.install -d %name-%version
rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

# Remove scrollkeeper files.
rm -rf $RPM_BUILD_ROOT%{_localstatedir}

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z].omf
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri desktop-mime-cache gconf-cache

%postun
%restart_fmri desktop-mime-cache 

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*char*map*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libgucharmap*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/gucharmap.desktop
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/gucharmap/C
%{_datadir}/omf/gucharmap/gucharmap-C.omf
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*char*map*
%doc -d gucharmap-%{gucharmap.version} AUTHORS COPYING.UNICODE NEWS README
%doc -d gucharmap-%{gucharmap.version} ChangeLog.README
%doc(bzip2) -d gucharmap-%{gucharmap.version} COPYING ChangeLog
%doc(bzip2) -d gucharmap-%{gucharmap.version} ChangeLog.pre-2-23
%doc(bzip2) -d gucharmap-%{gucharmap.version} help/ChangeLog.pre-2-23
%doc(bzip2) -d gucharmap-%{gucharmap.version} po/ChangeLog.pre-2-23
%dir %attr (0755, root, other) %{_datadir}/doc

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/gucharmap.schemas

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/gnome
%attr (-, root, other) %{_datadir}/locale
%{_datadir}/gnome/help/*/[a-z]*
%{_datadir}/omf/*/*-[a-z][a-z].omf
%{_datadir}/omf/*/*-[a-z][a-z]_[A-Z]*.omf
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Fri Sep 12 2008 - matt.keenn@sun.com
- Update copyright
* Tue Jun 17 2008 - damien.carbery@sun.com
- Update %files as the %{_datadir}/icons dir is no longer delivered - a stock
  icon is used.
* Thu Jun 12 2008 - darren.kenny@sun.com
- Add missing root package dependency
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Wed Nov 05 2007 - damien.carbery@sun.com
- Add root package and post/preun scripts for gucharmap.schemas.
* Wed Oct 10 2007 - damien.carbery@sun.com
- Remove 'Requires: SUNWgnome-doc-utils' as it is only used during building;
  change SUNWgnome-doc-utils-devel to SUNWgnome-doc-utils to match change in
  SUNWgnome-doc-utils.spec.
* Fri Sep 01 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Fri Aug 25 2006 - brian.cameron@sun.com
- Add new charmap.1 manpage.
* Sat Aug 12 2006 - laca@sun.com
- delete some unnecessary env variables
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
* Fri Jun 02 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWgnome-doc-utils/-devel otherwise build fails.
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Feb 14 2006 - damien.carbery@sun.com
- Change %files share for new tarball (gucharmap.png now under icons).
* Mon Jan 30 2006 - damien.carbery@sun.com
- Delete scrollkeeper files before packaging.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-desktop-database
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Tue May 17 2005 - brian.cameron@sun.com
- Split out from SUNWgnome-utils.spec, since it is now a dependancy
  on gnome-applets (in SUNWgnome-panel) and SUNWgnome-utils depends
  on SUNWgnome-panel.
