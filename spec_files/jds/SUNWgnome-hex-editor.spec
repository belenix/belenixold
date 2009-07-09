#
# spec file for package SUNWgnome-hex-editor
#
# includes module(s): ghex
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: yuntong.jin 
#
%include Solaris.inc
%include l10n.inc
Name:                    SUNWgnome-hex-editor
Summary:                 GNOME hex editor
Version:                 %{default_pkg_version}
%define tarball_version  2.22.0
Source:                  http://ftp.gnome.org/pub/gnome/sources/ghex/2.22/ghex-%{tarball_version}.tar.bz2
Source1:                 %{name}-manpages-0.1.tar.gz
%if %build_l10n
Source2:                 l10n-configure.sh
Source3:                 ghex-po-sun-%{po_sun_version}.tar.bz2
%endif
#date:2008-08-15 owner:jedy type:branding
Patch1:                  ghex-01-menu-entry.diff
SUNW_BaseDir:            %{_prefix}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWgnome-libs
Requires: SUNWgnome-hex-editor-root
Requires: SUNWgnome-print
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-component
Requires: SUNWgnome-config
Requires: SUNWgnome-vfs
Requires: SUNWlibms
Requires: SUNWlibpopt
Requires: SUNWdesktop-cache
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-vfs-devel
BuildRequires: SUNWlibpopt-devel
BuildRequires: SUNWgnome-print-devel
BuildRequires: SUNWgnome-libs-devel

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
Requires: SUNWgnome-hex-editor
%include default-depend.inc

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
%setup -c -n %name-%tarball_version
%if %build_l10n
cd %{_builddir}/%name-%{tarball_version}
cd ghex-%{tarball_version}
bzcat %SOURCE3 | tar xf -
cd po-sun; make; cd ..
%endif

cd %{_builddir}/%name-%{tarball_version}
gzcat %SOURCE1 | tar xf -
cd ghex-%{tarball_version}

%patch1 -p1 

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

cd ghex-%{tarball_version}
export PKG_CONFIG_PATH=%{_pkg_config_path}
export CFLAGS="%optflags"
export RPM_OPT_FLAGS="$CFLAGS"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export LDFLAGS="%_ldflags"
glib-gettextize -f
libtoolize --force
intltoolize --force --copy --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure \
    --prefix=%{_prefix} \
    --libexecdir=%{_libexecdir} \
    --sysconfdir=%{_sysconfdir}
                                
%install
rm -rf $RPM_BUILD_ROOT
cd ghex-%{tarball_version}
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make install DESTDIR=$RPM_BUILD_ROOT -j$CPUS
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
cd %{_builddir}/%name-%{tarball_version}/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%if %build_l10n
%else
# REMOVE l10n FILES*files-list*
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
rm -rf $RPM_BUILD_ROOT%{_datadir}/gnome/help/*/[a-z]*
rm -rf $RPM_BUILD_ROOT%{_datadir}/omf/*/*-[a-z]*.omf
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%post
%restart_fmri gconf-cache

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gnome-2.0
%dir %attr (0755, root, other) %{_datadir}/gnome
%{_datadir}/gnome/help/*/C
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*.desktop
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*
%dir %attr (-, root, other) %{_datadir}/icons
%dir %attr (-, root, other) %{_datadir}/icons/hicolor
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/16x16/apps
%{_datadir}/icons/hicolor/16x16/apps/ghex.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/22x22/apps
%{_datadir}/icons/hicolor/22x22/apps/ghex.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/24x24/apps
%{_datadir}/icons/hicolor/24x24/apps/ghex.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/32x32/apps
%{_datadir}/icons/hicolor/32x32/apps/ghex.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/48x48/apps
%{_datadir}/icons/hicolor/48x48/apps/ghex.png
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable
%dir %attr (-, root, other) %{_datadir}/icons/hicolor/scalable/apps
%{_datadir}/icons/hicolor/scalable/apps/ghex.svg
%doc -d ghex-%{tarball_version} AUTHORS ChangeLog NEWS README 
%doc(bzip2) -d ghex-%{tarball_version} COPYING
%doc(bzip2) -d ghex-%{tarball_version} COPYING-DOCS
%dir %attr (0755, root, other) %{_datadir}/doc

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/ghex2.schemas

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
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Mon Mar 30 2009 - yuntong.jin@sun.com
- change the owner to yuntong.jin
* Wed Oct 01 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Fri Aug 22 2008 - jedy.wang@sun.com
- rename desktop.diff to menu-entry.diff.
* Thu Aug 21 2008 - jedy.wang@sun.com
- Remove option_with_indiana_branding.
* Fri Aug 15 2008 - jedy.wang@sun.com
- Add 01-desktop.diff.
* Wed May 28 2008 - rick.ju@sun.com
- Bump to 2.22.0
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Thu Sep 20 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Sep 05 2007 - damien.carbery@sun.com
- Remove references to SUNWgnome-a11y-base-libs as its contents have been
  moved to SUNWgnome-base-libs.
* Wed Aug 15 2007 - damien.carbery@sun.com
- Bump to 2.19.90.
* Fri Aug 10 2007 - damien.carbery@sun.com
- Bump to 2.19.0. Update %files to remove omf files and add icons.
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Fri Sep 08 2006 - Matt.Keenan@sun.com
- Add man page tarball
* Fri Jul 14 2006 - laca@sun.com
- update %post/%postun/etc scripts to support diskless client setup,
  part of 6448317
* Thu Jun 29 2006 - laca@sun.com
- update postrun scripts
* Sun Jun 11 2006 - laca@sun.com
- change group from other to bin/sys
* Thu May 25 2006 - laca@sun.com
- use post/preun scripts to install schemas into the merged gconf files
* Wed May 10 2006 - laca@sun.com
- merge -share pkg(s) into the base pkg(s)
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Tue Nov 29 2005 - laca@sun.com
- remove javahelp stuff
* Thu Sep 15 2005 - laca@sun.com
- update to 2.8.1
* Fri Nov 26 2004 - laca@sun.com
- initial version of spec file
