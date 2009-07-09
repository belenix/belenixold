#
# spec file for package libgnome
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: padraig
#
Name:         libgnome
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.26.0
Release:      5
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      GNOME Base Library
Source:       http://ftp.gnome.org/pub/GNOME/sources/libgnome/2.26/libgnome-%{version}.tar.bz2
%if %build_l10n
Source1:                 l10n-configure.sh
%endif
# owner:padraig date:2005-04-26 type:branding
Patch1:       libgnome-01-sun-default-background.diff
# owner:gman date:2008-01-18 type:branding
Patch2:       libgnome-02-indiana-default.diff
# owner:padraig date:2005-07-18 type:branding
Patch3:       libgnome-03-default-theme.diff
# owner:mattman date:2005-07-18 type:branding bugzilla:395887
Patch4:       libgnome-04-lockdown-schemas.diff
# owner:padraig date:2005-07-18 type:branding
Patch5:       libgnome-05-input-method-status-style.diff
# owner:liyuan date:2008-09-09 type:branding
Patch6:       libgnome-06-disable-accessibility.diff
URL:          http://www.gnome.org
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig

%define GConf_version 2.6.1
%define gnome_vfs_version 2.6.0
%define libbonobo_version 2.6.0
%define libxslt_version 1.1.2
%define audiofile_version 0.2.5
%define esound_version 0.2.33
%define gtk_doc_version 1.1
%define popt_version 1.7

BuildRequires: GConf-devel >= %{GConf_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: gnome-vfs-devel >= %{gnome_vfs_version}
BuildRequires: libxslt-devel >= %{libxslt_version}
BuildRequires: esound-devel >= %{esound_version}
# Audio file header files are include in base pkg in SuSE 9.1
BuildRequires: audiofile >= %{audiofile_version}
BuildRequires: gtk-doc >= %{gtk_doc_version}
BuildRequires: popt-devel >= %{popt_version}
Requires:      GConf >= %{GConf_version}
Requires:      libbonobo >= %{libbonobo_version}
Requires:      esound >= %{esound_version}
Requires:      audiofile >= %{audiofile_version}
Requires:      libxslt >= %{libxslt_version}

%description
libgnome is one of the base GNOME libraries, containing convenient API for
configuration, help, initialization and web links, all specific to the 
GNOME desktop.

%package devel
Summary:      GNOME Base Development Library
Group:        Development/Libraries/GNOME
Requires:     %name = %version-%release
Requires:     popt-devel >= %{popt_version}
Requires:     libbonobo-devel >= %{libbonobo_version}

%description devel
libgnome is one of the base GNOME libraries, containing convenient API for
configuration, help, initialization and web links, all specific to the 
GNOME desktop.

%prep
%setup -q
%if %option_with_sun_branding
%patch1 -p1
%endif
%if %option_with_indiana_branding
%patch2 -p1
%endif
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
%ifos linux
if [ -x /usr/bin/getconf ]; then
  CPUS=`getconf _NPROCESSORS_ONLN`
fi
%else
  CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
%endif
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

libtoolize --force
glib-gettextize --copy --force
intltoolize --copy --force --automake

%if %build_l10n
bash -x %SOURCE1 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
autoconf
autoheader
gtkdocize --copy
automake -a -c -f
CFLAGS="$RPM_OPT_FLAGS"		\
./configure --prefix=%{_prefix}		\
    	    --datadir=%{_datadir}       \
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir} \
            --mandir=%{_mandir}         \
            %{gtk_doc_option}
./config.status
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1   
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL  

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/
rm $RPM_BUILD_ROOT%{_libdir}/bonobo/monikers/*.a
rm $RPM_BUILD_ROOT%{_libdir}/bonobo/monikers/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

#%check
make check

%clean 
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
SCHEMAS="desktop_gnome_accessibility_keyboard.schemas		\
	 desktop_gnome_accessibility_startup.schemas		\
	 desktop_gnome_applications_browser.schemas		\
	 desktop_gnome_applications_help_viewer.schemas		\
	 desktop_gnome_applications_terminal.schemas		\
	 desktop_gnome_applications_window_manager.schemas	\
	 desktop_gnome_background.schemas			\
	 desktop_gnome_file_views.schemas			\
	 desktop_gnome_interface.schemas			\
	 desktop_gnome_peripherals_keyboard.schemas		\
	 desktop_gnome_peripherals_mouse.schemas		\
	 desktop_gnome_sound.schemas				\
	 desktop_gnome_thumbnailers.schemas			\
	 desktop_gnome_typing_break.schemas                     \
	 desktop_gnome_lockdown.schemas"
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%files 
%defattr(-, root, root)
%{_datadir}/locale/*/LC_MESSAGES/*.mo
%{_bindir}/gnome-open
%{_sysconfdir}/sound/events/*.soundlist
%{_sysconfdir}/gconf/schemas/*
%{_libdir}/libgnome*so.*
%{_libdir}/bonobo/monikers/*so*
%{_libdir}/bonobo/servers/*.server

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/libgnome-2.0.pc
%{_includedir}/libgnome-2.0/libgnome/*.h
%{_datadir}/gtk-doc/*
%{_libdir}/libgnome*so
%{_mandir}/man1/*
%{_mandir}/man3/*
%{_mandir}/man7/*

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 2.26.0
* Fri Mar 13 2009 - dave.lin@sun.com
- Bump to 2.25.1
* Mon Sep 29 2008 - christian.kelly@sun.com
- Bump to 2.24.1.
* Sun Sep 21 2008 - christian.kelly@sun.com
- Bump to 2.23.92.
* Tue Sep 09 2008 - li.yuan@sun.com
- Add patch 06-disable-accessibility. Don't enable accessibility by
  default on development build.
* Thu Aug 21 2008 - dave.lin@sun.com
- Bump to 2.23.5
* Tue Aug 12 2008 - jedy.wang@sun.com
- merge 02-indiana-default-background and 03-indiana-default-theme into
  02-indiana-default and set /desktop/gnome/interface/toolbar_style
  to both-horiz.
* Tue Jun 17 2008 - damien.carbery@sun.com
- Bump to 2.23.4.
* Wed Jun 04 2008 - damien.carbery@sun.com
- Bump to 2.23.3.
* Wed Apr 16 2008 - damien.carbery@sun.com
- Add 'make check' call after %install.
* Mon Mar 10 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Thu Mar 06 2008 - damien.carbery@sun.com
- Bump to 2.21.91.
* Mon Feb 11 2008 - laca@sun.com
- do not apply patches 1 or 2 (branding patches) if neither Sun nor Indiana
  branding is selected
* Mon Jan 28 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Fri Jan 18 2007 - glynn.foster@sun.com
- Addition of Indiana default theme patch
* Fri Oct 19 2007 - damien.carbery@sun.com
- Bump to 2.20.1.1.
* Wed Oct  3 2007 - laca@sun.com
- add indiana default background patch
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Wed Aug 29 2007 - damien.carbery@sun.com
- Add --automake to intltoolize call for consistency with other modules.
* Mon Jul 30 2007 - damien.carbery@sun.com
- Bump to 2.19.1.
* Tue Jun 19 2007 - damien.carbery@sun.com
- Bump to 2.19.0.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Mon Mar 05 2007 - damien.carbery@sun.com
- Bump to 2.17.92.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91.
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90.
* Wed Jan 10 2007 - damien.carbery@sun.com
- Bump to 2.17.3.
* Tue Jan 09 2007 - damien.carbery@sun.com
- Bump to 2.17.2.
* Thu Dec 07 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Wed Nov 22 2006 - damien.carbery@sun.com
- Bump to 2.17.0.
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Aug 08 2006 - padraig.obriain@sun.com
- Bump to 2.15.2.
* Fri Jul 21 2006 - padraig.obriain@sun.com
- Bump to 2.15.1.
* Tue Apr 11 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Tue Feb 28 2006 - damien.carbery@sun.com
- Bump to 2.13.90.
* Thu Feb 16 2006 - brian.cameron@sun.com
- Set libexecdir or else we get /usr/libexec in the 
  libgnome.pc file.
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.5
* Wed Dec 21 2005 - brian.cameron@sun.com
- Bump to 2.13.4.
* Thu Sep 15 2005 - brian.cameron@sun.com
- Bump to 2.12.0.1.
* Fri Sep 09 2005 - laca@sun.com
- reorder autofoo: move intltoolize after glib-gettextize is the correct
  po/Makefile.in.in is used
* Tue Sep 06 2005 - damien.carbery@sun.com
- Call intltoolize, glib-gettextize and gtkdocize to add missing files.
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.3.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump to 2.11.2.
* Tue Jul 19 2005 - muktha.narayan@wipro.com
- Modify libgnome-02-default-theme.diff,
  libgnome-03-lockdown-schemas.diff and 
  libgnome-04-input-method-status-style.diff
  so that the changes are applied to the .schemas.in 
  files instead of .schemas files.
* Thu Jun 23 2005 - muktha.narayan@wipro.com
- Modified libgnome-03-lockdown-schemas.diff to
  include starsuite and starsuite-printeradmin in the 
  allowed_applications list.
  Fixes bug #6288742.
* Fri May 20 2005 - glynn.foster@sun.com
- Remove backgrounds and put them in gnome-backgrounds
  package. Sanitizes things a lot.
* Thu May 12 2005 - muktha.narayan@wipro.com
- Modified libgnome-03-lockdown-schemas.diff to
  update the entries in the allowed_applications list.
  Fixes bug #6266517.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.10.0
* Fri Dec 24 2004 - srirama.sharma@wipro.com
- Replacing /usr/bin/staroffice with /usr/bin/soffice in
  libgnome-03-lockdown-schemas.diff. Fixes Bug #6208251.
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gnome-open.1 man page
* Thu Oct 21 2004 - vinay.mandyakoppal@wipro.com
- Add patch to fix Launcher to be usable as root.
* Wed Sep 15 2004 - yuriy.kuznetsov@sun.com
- Added libgnome-07-g11n-potfiles.diff
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc.
* Mon Aug 09 2004 - vinay.mandyakoppal@wipro.com
- Added desktop_gnome_typing_break.schemas 
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to libgnome-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- Ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Tue May 25 2004 - yuriy.kuznetsov@sun.com
- Added libgnome-06-g11n-potfiles.diff
* Thu May 20 2004 - hidetoshi.tajima@sun.com
  Add libgnome-05-input-method-status-style.diff again.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to libgnome-l10n-po-1.1.tar.bz2
* Tue May 11 2004 - laszlo.kovacs@sun.com
- rename jdshelp script
* Thu May 06 2004 - laszlo.kovacs@sun.com
- replacing yelp with jds-help.sh in libgnome-03-lockdown-schemas.diff
* Mon May 3 2004 - glynn.foster@wipro.com
- Add bindir, so we get the joys of gnome-open
* Wed Apr 14 2004 - archana.shah@wipro.com
- Removed desktop_gnome_url_handlers.schemas from spec file.
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to libgnome-l10n-po-1.0.tar.bz2
* Mon Mar 22 2004 - glynn.foster@sun.com
- Bump to 2.6.0. Remove the the uninstalled pc patch since 
  it's upstream.
* Wed Mar 04 2004 - matt.keenan@sun.com
- Bump to 2.5.90, as it contains partial lockdown schema file
- re-engineer lockdown schema patch
- Remove the OrigTree.pm hack
* Mon Feb 23 2004 - stephen.browne@sun.com
- Bump to 2.5.4
* Mon Feb 02 2004 - niall.power@sun.com
- Bump to 2.5.3
- Add OrigTree.pm as source 5.
- Unpack source 1 after build into RPM_BUILD_ROOT (fixes solaris breakage).
- Add patch to add an -uninstalled.pc file for pkgconfig
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- Add patch 06 to search in /usr for intltool perl modules
* Thu Jan 29 2004 - <dermot.mccluskey@sun.com>
- Add dependency on intltool
* Mon Dec 15 2003 - glynn.foster@sun.com
- Bump to 2.5.1
* Tue Oct 21 2003 - matt.keenan@sun.com
- lockdown schema patch
* Wed Oct 08 2003 - stephen.browne@sun.com
- Updated for 2.4
* Fri Sep 05 2003 - michael.twomey@sun.com
- Add libgnome-04-schemas-chinese.diff to fix font sizes.
  Fixes bug 4915643.
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Thu Aug 07 2003 - glynn.foster@sun.com
- Update tarball, reset release, bump version.
* Thu Jul 24 2003 - Laszlo.Kovacs@sun.com
- added libgnome-04-background.diff
* Thu Jul 10 2003 - michael.twomey@sun.com
- Added .po tarball
* Thu Jul 03 2003 - glynn.foster@sun.com
- Remove the joint theme/background patch and separate them
  out
* Wed Apr 30 2003 - niall.power@sun.com
- Create new spec file for libgnome
