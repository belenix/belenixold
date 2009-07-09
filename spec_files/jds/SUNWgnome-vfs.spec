#
# spec file for package SUNWgnome-vfs
#
# includes module(s): gnome-mime-data, gnome-vfs
#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include Solaris.inc

%define with_hal %(pkginfo -q SUNWhal && echo 1 || echo 0)

%use smimeinfo = shared-mime-info.spec
%use gmdata = gnome-mime-data.spec
%use gvfs = gnome-vfs.spec

Name:                    SUNWgnome-vfs
Summary:                 GNOME virtual file system framework and application/MIME type registry
Version:                 %{default_pkg_version}
Source:                  %{name}-manpages-0.1.tar.gz
SUNW_BaseDir:            %{_basedir}
SUNW_Copyright:          %{name}.copyright
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
Requires: SUNWgnome-vfs-root
Requires: SUNWgnome-base-libs
Requires: SUNWgnome-config
Requires: SUNWgnome-component
Requires: SUNWdbus
Requires: SUNWdbus-glib
Requires: SUNWperl584usr
Requires: SUNWbzip
Requires: SUNWzlib
Requires: SUNWlxml
Requires: SUNWsmbau
Requires: SUNWdesktop-cache
Requires: SUNWlibms
Requires: SUNWopenssl-libraries
Requires: SUNWgamin
Requires: SUNWless
%if %with_hal
Requires: SUNWhal
%endif
BuildRequires: SUNWgnome-base-libs-devel
BuildRequires: SUNWgnome-config-devel
BuildRequires: SUNWgnome-component-devel
BuildRequires: SUNWdbus-devel
BuildRequires: SUNWdbus-glib-devel
BuildRequires: SUNWopenssl-libraries
BuildRequires: SUNWopenssl-include
BuildRequires: SUNWgamin-devel

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
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
%smimeinfo.prep -d %name-%version
%gmdata.prep -d %name-%version
%gvfs.prep -d %name-%version
cd %{_builddir}/%name-%version
gzcat %SOURCE0 | tar xf -

%build
export PKG_CONFIG_PATH=../gnome-mime-data-%{gmdata.version}:../gnome-vfs-%{gvfs.version}:%{_pkg_config_path}
# /usr/sfw/include needed for libsmbclient.h
export CFLAGS="%optflags -I/usr/sfw/include"
export RPM_OPT_FLAGS="$CFLAGS"
export LDFLAGS="%_ldflags"

%smimeinfo.build -d %name-%version
%gmdata.build -d %name-%version

export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib"
%gvfs.build -d %name-%version

%install
rm -rf $RPM_BUILD_ROOT
export PKG_CONFIG_PATH=../gnome-mime-data-%{gmdata.version}:../gnome-vfs-%{gvfs.version}:%{_libdir}/pkgconfig:/usr/lib/pkgconfig
%smimeinfo.install -d %name-%version
%gmdata.install -d %name-%version
%gvfs.install -d %name-%version
LD_LIBRARY_PATH=$RPM_BUILD_ROOT%{_libdir} $RPM_BUILD_ROOT%{_bindir}/update-mime-database $RPM_BUILD_ROOT%{_datadir}/mime

rm -rf $RPM_BUILD_ROOT%{_mandir}
cd %{_builddir}/%name-%version/sun-manpages
make install DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_prefix}/doc

%if %build_l10n
%else
# REMOVE l10n FILES
rm -rf $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%restart_fmri mime-types-cache gconf-cache

%files
%doc -d shared-mime-info-%{smimeinfo.version} README
%doc(bzip2) -d shared-mime-info-%{smimeinfo.version} COPYING ChangeLog NEWS
%doc gnome-mime-data-%{gmdata.version}/README
%doc gnome-mime-data-%{gmdata.version}/AUTHORS
%doc(bzip2) gnome-mime-data-%{gmdata.version}/COPYING
%doc(bzip2) gnome-mime-data-%{gmdata.version}/ChangeLog
%doc(bzip2) gnome-mime-data-%{gmdata.version}/NEWS
%doc gnome-vfs-%{gvfs.version}/README
%doc gnome-vfs-%{gvfs.version}/AUTHORS
%doc(bzip2) gnome-vfs-%{gvfs.version}/COPYING
%doc(bzip2) gnome-vfs-%{gvfs.version}/COPYING.LIB
%doc(bzip2) gnome-vfs-%{gvfs.version}/ChangeLog
%doc(bzip2) gnome-vfs-%{gvfs.version}/NEWS
%dir %attr (0755, root, other) %{_datadir}/doc
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/gnome-vfs-2.0/modules/*.so
%{_libdir}/lib*.so*
%{_libdir}/gnome-vfs-daemon
%dir %attr (0755, root, sys) %{_datadir}
%ghost %attr (-, root, root) %{_datadir}/mime
%dir %attr (0755, root, other) %{_datadir}/mime-info
%{_datadir}/mime-info/*
%dir %attr (0755, root, other) %{_datadir}/application-registry
%{_datadir}/application-registry/*
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%{_datadir}/dbus-1/services/gnome-vfs-daemon.service
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gconf/schemas/desktop_default_applications.schemas
%{_sysconfdir}/gconf/schemas/desktop_gnome_url_handlers.schemas
%{_sysconfdir}/gconf/schemas/system_dns_sd.schemas
%{_sysconfdir}/gconf/schemas/system_http_proxy.schemas
%{_sysconfdir}/gconf/schemas/system_smb.schemas
%{_sysconfdir}/gnome-vfs-2.0
%ghost %attr (0644, root, sys) %{_sysconfdir}/gnome-vfs-mime-magic

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%{_libdir}/gnome-vfs-2.0/include
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%{_datadir}/pkgconfig
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man3
%dir %attr(0755, root, bin) %{_mandir}/man4
%{_mandir}/man3/*
%{_mandir}/man4/*

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Fri Apr  3 2009 - laca@sun.com
- use desktop-cache instead of postrun
* Mon Mar 23 2009 - jeff.cai@sun.com
- Add the dependency on SUNWless since /usr/bin/gvfs-less calls usr/bin/less
* Thu Mar 05 2009 - brian.cameron@sun.com
- Change SUNWdbus-bindings to SUNWdbus-glib.
* Mon Sep 15 2008 - christian.kelly@sun.com
- Remove /usr/share/doc from %files.
* Thu Jan  3 2008 - laca@sun.com
- use gconf-install.script instead of an inline script
* Thu May 17 2007 - laca@sun.com
- delete SUNWsmbaS dependency and related CFLAGS, since 6267187 was
  fixed in snv_40.
- delete some unnecessary env variables
* Tue Apr 24 2007 - laca@sun.com
- s/0755/-/ in defattr so that files are not made all executable
* Thu Mar 15 2007 - damien.carbery@sun.com
- Add %{_datadir}/pkgconfig for new shared-mime-info tarball.
* Wed Nov 29 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWdbus-bindings/-devel for the glib bindings.
* Tue Nov 28 2006 - damien.carbery@sun.com
- Change attr of gnome-vfs-mime-magic file in root package to fix 6497737.
* Fri Oct 20 2006 - damien.carbery@sun.com
- Remove SUNWhalh BuildRequires because header files are in SUNWhea in snv_51.
* Mon Sep 18 2006 - Brian.Cameron@sun.com
- Add SUNWhalh BuildRequires.
* Mon Sep 04 2006 - Matt.Keenan@sun.com
- New Manpage tarball
* Mon Aug 14 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWhal after check-deps.pl run.
* Sat Jul 29 2006 - damien.carbery@sun.com
- Add Build/Requires SUNWdbus/-devel.
* Sat Jul 22 2006 - laca@sun.com
- update %files: delete %{libdir}/_bonobo, add %{_datadir}/dbus-1
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
* Thu Apr  6 2006 - damien.carbery@sun.com
- Add SUNWopenssl-libraries/include to Build/Requires after check-deps.pl run.
* Mon Feb 20 2006 - damien.carbery@sun.com
- Update Build/Requires after running check-deps.pl script.
* Sat Dec  3 2005 - laca@sun.com
- add %post script that runs update-mime-database
* Tue Sep 06 2005 - laca@sun.com
- add to %files or remove unpackaged files
* Wed May 11 2005 - brian.cameron@sun.com
- Fixed packaging for 2.10 codebase.
* Thu Oct 14 2004 - narayana.pattipati@wipro.com
- Added SUNWsmbau, SUNWsmbaS packages as Requires/BuildRequires, so that
  smb:// is built for Solaris.
* Sat Oct 02 2004 - laca@sun.com
- added %pkgbuild_postprocess
* Fri Sep 24 2004 - laca@sun.com
- remove %{_datadir}/gnome too, it also belonged to the nfs module
* Thu Sep 23 2004 - laca@sun.com
- remove reserved-port-helper from %files as the patch that created it
  was removed from the Linux spec file
* Thu Sep 09 2004 - matt.keenan@sun.com
- Added gnomevfs-*.1, upadte-mime-database.1 manpages
* Thu Sep 02 2004 - narayana.pattipati@wipro.com
- Don't build gnome-vfs-extras for Solaris. We will build smb:/// method
  of gnome-vfs itself, as samba support is available now.
- Added /usr/sfw/bin to LDFLAGS and /usr/sfw/src/samba/sources/include to
  CFLAGS, so that smb:/// support is build for Solaris. samba team will
  change the path of libraries from /usr/sfw/bin to /usr/sfw/lib (bug#5088461)
  Once they change it, we can remove /usr/sfw/bin from LDFLAGS.
* Mon Aug 30 2004 - shirley.woo@sun.com
- Bug 5091588 : sman3/4 files should be in a separate devel package
* Mon Aug 23 2004 - laca@sun.com
- s/SUNWpl5u/SUNWperl584usr/
* Wed Aug 18 2004  daien.carbery@sun.com
- Change manpage perms for Solaris integration.
* Mon Aug 02 2004  narayana.pattipati@wipro.com
- Added /usr/sfw/lib to LDFLAGS. Fixes bugtraq bug#5080276
* Sat Jun 26 2004  shirley.woo@sun.com
- Changed install location to /usr/...
* Thu May 27 2004 - laca@sun.com
- added l10n subpkg
* Tue May 25 2004 - laca@sun.com
- run update-mime-database in %install
* Thu May 20 2004 - brian.cameron@sun.com
- Fixed man page installation.
* Sun May 02 2004 - laca@sun.com
- define PKG_CONFIG_PATH in %install too, for some relink stuff.
* Sun Apr 04 2004 - laca@sun.com
- Added a missing header file
* Wed Mar 24 2004 - brian.cameron@sun.com
- Added SGML man page integration
* Tue Mar 02 2004 - niall.power@sun.com
- add shared-mime-info component to pkg.
* Mon Mar 01 2004 - niall.power@sun.com
- add in missing gnome-vfs-daemon binary
* Sun Feb 29 2004 - laca@sun.com
- remove some gconf files that clash with SUNWgnome-libs & SUNWgnome-terminal
* Wed Feb 25 2004 - Niall.Power@sun.com
- remove sym link build hacks and add -R{_libdir}
  to LDFLAGS
* Mon Feb 23 2004 - Niall.Power@sun.com
- install gconf schemas at end of install stage.
* Mon Jan 26 2004 - Laszlo.Peter@sun.com
- initial version added to CVS
