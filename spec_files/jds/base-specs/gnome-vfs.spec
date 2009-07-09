#
# spec file for package gnome-vfs
#
# Copyright (c) 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: gheet
#
%include l10n.inc
Name:         gnome-vfs
License:      LGPL
Group:        System/Libraries/GNOME
Version:      2.24.1
Release:      4
Distribution: Java Desktop System
Vendor:       Sun Microsystems, Inc.
Summary:      Virtual File System Library for GNOME
Source:       http://ftp.gnome.org/pub/GNOME/sources/%{name}/2.24/%{name}-%{version}.tar.bz2
Source1:      %{name}-po-sun-%{po_sun_version}.tar.bz2
%if %build_l10n
Source2:                 l10n-configure.sh
%endif
# date:2006-11-23 type:branding owner:gheet 
Patch1:       gnome-vfs-01-default-url-handler.diff
# date:2005-04-26 type:branding owner:gheet 
Patch2:       gnome-vfs-02-mime-info-file-path.diff
# date:2004-10-19 type:bug bugster:5105006 bugzilla:137282 owner:stephen 
Patch3:       gnome-vfs-03-trash-only-home.diff
# date:2004-11-10 type:bug bugster:6190753 owner:stephen
Patch4:       gnome-vfs-04-mount-points-fix.diff
# date:2006-10-20 type:bug bugster:6200485 owner:stephen 
Patch5:       gnome-vfs-05-trash-files-from-different-filesystem.diff
# date:2005-01-31 type:branding bugster:4951431 owner:gheet 
Patch6:       gnome-vfs-06-socks-version.diff
# date:2006-10-20 type:bug bugster:6228176 owner:gheet 
Patch7:       gnome-vfs-07-audio-cd-show-icon.diff
# date:2005-04-13 type:bug bugster:6243507 owner:gheet 
Patch8:       gnome-vfs-08-trash-skip-copy.diff
# date:2006-05-02 type:bug owner:dcarbery bugzilla:395357
Patch9:       gnome-vfs-09-krb5-config-no-gssapi.diff
# date:2007-04-09 type:bug owner:padraig
Patch10:      gnome-vfs-10-acl-zfs.diff
# date:2007-11-08 type:bug bugster:6614146 bugzilla:495041 owner:migi
Patch11:      gnome-vfs-11-zfs-trash.diff
# date:2007-11-21 type:bug bugster:6630873 bugzilla:498806 owner:yippi
Patch12:      gnome-vfs-12-vfsinfo-crash.diff
# date:2007-11-26 type:bug bugster:6509673 bugzilla:499151 owner:padraig
Patch13:      gnome-vfs-13-hal-crash.diff
# date:2008-09-23 type:bug bugster:6752919 bugzilla:553505 owner:yippi
Patch14:      gnome-vfs-14-writable-home.diff
 
URL:          http://www.gnome.org/
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
Autoreqprov:  on
Prereq:       /sbin/ldconfig
Prereq:       GConf

%define libbonobo_version 2.6.0
%define GConf_version 2.6.1
%define gnome_mime_data_version 2.4.1
%define shared_mime_info_version 0.14
%define cdparanoia_version IIIalpha9.8-543
%define libsmbclient_version 3.0.4-1.22
%define gnome_vfs_extra_version 0.99.10

Requires:      libbonobo >= %{libbonobo_version}
Requires:      GConf >= %{GConf_version}
Requires:      gnome-mime-data >= %{gnome_mime_data_version}
Requires:      shared-mime-info >= %{shared_mime_info_version}
Requires:      cdparanoia >= %{cdparanoia_version}
Requires:      libsmbclient >= %{libsmbclient_version}
BuildRequires: libbonobo-devel >= %{libbonobo_version}
BuildRequires: GConf-devel >= %{GConf_version}
BuildRequires: gnome-mime-data >= %{gnome_mime_data_version}
BuildRequires: shared-mime-info >= %{shared_mime_info_version}
BuildRequires: libsmbclient-devel >= %{libsmbclient_version}

Obsoletes:	gnome-vfs-extras <= %{gnome_vfs_extra_version} 
Provides:      gnome-vfs-extras  = %{gnome_vfs_extra_version} 

%description
GNOME VFS is the GNOME virtual file system. It is the foundation of the
Nautilus file manager. It provides a modular architecture and ships with
several modules that implement support for file systems, http, ftp and others.
It provides a URI-based API, a backend supporting asynchronous file operations,
a MIME type manipulation library and other features.

%package devel
Summary:      The development package for the GNOME Virtual File System
Group:        Development/Libraries/GNOME
Requires:     %{name} = %{version}
Requires:     GConf-devel >= %{GConf_version}
Requires:     libbonobo-devel >= %{libbonobo_version}

%description devel
GNOME VFS is the GNOME virtual file system. It is the foundation of the
Nautilus file manager. It provides a modular architecture and ships with
several modules that implement support for file systems, http, ftp and others.
It provides a URI-based API, a backend supporting asynchronous file operations,
a MIME type manipulation library and other features.

%prep
%setup -q
%if %build_l10n
bzcat %SOURCE1 | tar xf -
cd po-sun; make; cd ..
%endif
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1

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
glib-gettextize --force
intltoolize -c -f --automake

%if %build_l10n
bash -x %SOURCE2 --enable-copyright
%endif

aclocal $ACLOCAL_FLAGS -I .
gtkdocize
autoheader
automake -a -c -f
autoconf
CFLAGS="$RPM_OPT_FLAGS -DDBUS_API_SUBJECT_TO_CHANGE=1"	\
./configure --prefix=%{_prefix}		\
            --sysconfdir=%{_sysconfdir} \
            --libexecdir=%{_libexecdir} \
            --enable-fam		\
            %{gtk_doc_option}
make -j $CPUS

%install
export GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL=1
make DESTDIR=$RPM_BUILD_ROOT install
unset GCONF_DISABLE_MAKEFILE_SCHEMA_INSTALL
rm $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/*.a
rm $RPM_BUILD_ROOT%{_libdir}/gnome-vfs-2.0/modules/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a
rm $RPM_BUILD_ROOT%{_libdir}/*.la

#Copy zh_HK from zh_TW
#Fixes bug 4930405
install -d $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES
install --mode=0644 $RPM_BUILD_ROOT%{_datadir}/locale/zh_TW/LC_MESSAGES/*.mo $RPM_BUILD_ROOT%{_datadir}/locale/zh_HK/LC_MESSAGES/

%post
/sbin/ldconfig
export GCONF_CONFIG_SOURCE=`gconftool-2 --get-default-source`
SCHEMAS="system_http_proxy.schemas desktop_gnome_url_handlers.schemas desktop_default_applications.schemas system_smb.schemas"
for S in $SCHEMAS; do
  gconftool-2 --makefile-install-rule %{_sysconfdir}/gconf/schemas/$S >/dev/null
done

%postun
/sbin/ldconfig

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr(-, root, root)
%{_bindir}/*
%{_datadir}/locale/*/LC_MESSAGES/gnome-vfs-2.0.mo
%{_libdir}/bonobo/servers/GNOME_VFS_Moniker_std.server
%{_libdir}/bonobo/servers/GNOME_VFS_Daemon.server
%{_sysconfdir}/gconf/schemas/*.schemas
%config %{_sysconfdir}/gnome-vfs-2.0
%{_libdir}/gnome-vfs-2.0/modules/*.so
%{_libexecdir}/*
%{_libdir}/libgnomevfs-2.so.*

%files devel
%defattr(-, root, root)
%{_libdir}/pkgconfig/gnome-vfs-2.0.pc
%{_libdir}/pkgconfig/gnome-vfs-module-2.0.pc
%{_includedir}/gnome-vfs-2.0
%{_includedir}/gnome-vfs-module-2.0
%{_libdir}/gnome-vfs-2.0/include
%{_libdir}/libgnomevfs-2.so
%{_datadir}/gtk-doc/html/gnome-vfs-2.0
%{_mandir}/man1/*
%{_mandir}/man3/*

%changelog
* Wed Mar 18 2009 - dave.lin@sun.com
- Bump to 2.24.1
* Fri Sep 26 2008 - brian.cameron@sun.com
- Bump to 2.24.0.
* Tue Sep 23 2008 - brian.cameron@sun.com
- Add patch gnome-vfs-14-writable-home.diff so that gnome-vfs works if the
  user has no writable $HOME direcory.  Fixes bugster bug #6752919.
* Thu Aug 07 2008 - damien.carbery@sun.com
- Bump to 2.23.0. Remove upstream patch, 14-acl-perms-corrupted.
* Tue Mar 11 2008 - damien.carbery@sun.com
- Bump to 2.22.0.
* Wed Jan 30 2008 - damien.carbery@sun.com
- Bump to 2.21.90.
* Tue Jan 29 2008 - takao.fujiwara@sun.com
- Add l10n tarball.
* Mon Jan 21 2008 - ghee.teo@sun.com
- Added patch gnome-vfs-14-acl-perms-corrupted.diff
* Mon Jan 07 2008 - damien.carbery.com
- Remove dos2unix code as bug 326431 is no longer an issue.
* Mon Nov 26 2007 - padraig.obriain@sun.com
- Add patch gnome-vfs-13-hal-crash.diff to fix crashing issue,
  bug #6506973.
* Wed Nov 21 2007 - brian.cameron@sun.com/
- Add patch gnome-vfs-12-vfsinfo-crash.diff to fix crashing issue,
  bug #6630873.
* Mon Nov 12 2007 - damien.carbery@sun.com
- Bump to 2.20.1.
* Thu Nov 08 2007 - michal.pryc@sun.com
- Add gnome-vfs-11-zfs-trash.diff to enable Trash on ZFS Volume.
* Wed Sep 19 2007 - damien.carbery@sun.com
- Bump to 2.20.0.
* Mon Aug 27 2007 - damien.carbery@sun.com
- Bump to 2.19.91. Remove upstream patch, 11-g11n-workgroup.
* Thu Aug 23 2007 - takao.fujiwara@sun.com
- Add gnome-vfs-11-g11n-workgroup.diff to show mutibyte workgroups.
  Fixes 6543813.
* Fri Jul 27 2007 - damien.carbery@sun.com
- Bump to 2.19.3.
* Mon May 14 2007 - damien.carbery@sun.com
- Bump to 2.19.2.
* Tue Apr 10 2007 - damien.carbery@sun.com
- Bump to 2.18.1.
* Tue Apr 10 2007 - alvaro.lopez@sun.com
- Added patch #10: Adds ZFS/NFS4 ACL support
* Tue Mar 13 2007 - damien.carbery@sun.com
- Bump to 2.18.0.1.
* Mon Mar 12 2007 - damien.carbery@sun.com
- Bump to 2.18.0.
* Tue Feb 13 2007 - damien.carbery@sun.com
- Bump to 2.17.91. Remove upstream patch, 10-hidden.
* Tue Feb 06 2007 - alvaro.lopez@sun.com
- gnome-vfs-11-acl-permissions.diff removed
* Mon Jan 22 2007 - damien.carbery@sun.com
- Bump to 2.17.90. Remove upstream patch, 09-login_tty.
* Tue Dec 19 2006 - damien.carbery@sun.com
- Bump to 2.17.2.
* Mon Dec 18 2006 - damien.carbery@sun.com
- Bump to 2.17.1.
* Thu Dec 14 2006 - ghee.teo@sun.com
- According to http://bugzilla.gnome.org/show_bug.cgi?id=168731,
  gnome-vfs-03-g11n-i18n-ui.diff seemed to have been integrated, removed.
* Mon Nov 27 2006 - damien.carbery@sun.com
- Bump to 2.16.3.
* Fri Nov 10 2006 - ghee.teo@sun.com
- removed gnome-vfs-01-uri-canonizing.diff, which is a old patch used of 
  vfolder and has consulted laszlo.kovacs.
- removed gnome-vfs-02-gopher-proxy-schema.diff, which is no longer use as 
  firefox doesnot make Solaris changes now.
* Wed Nov 08 2006 - damien.carbery@sun.com
- Bump to 2.16.2.
* Tue Nov  7 2006 - ghee.teo@sun.com
- removed gnome-vfs-02-uninstalled-pc.diff (logged as bugzilla 371610)
* Fri Nov  3 2006 - laca@sun.com
- use %gtk_doc_option in configure so that it can be disabled using
  --without-gtk-doc
* Mon Oct 23 2006 - takao.fujiwara@sun.com
- Added intlotoolize to build .po files. Fixes 6484798.
* Mon Oct 02 2006 - damien.carbery@sun.com
- Bump to 2.16.1.
* Mon Sep 04 2006 - damien.carbery@sun.com
- Bump to 2.16.0.
* Tue Sep 4 2006 - alvaro.lopez@sun.com
- gnome-vfs-16-acl-permissions: Added new patch. Fixes community
  ACL related bug. This patch will be upstream within a few days.
* Tue Aug 29 2006 - jedy.wang@sun.com
- gnome-vfs-12-ftp-show-permissions.diff removed because
  the bug it fixed has been fixed in the latest nautilus.
* Tue Aug 08 2006 - damien.carbery@sun.com
- Bump to 2.15.91.
* Thu Jul 27 2006 - damien.carbery@sun.com
- Remove upstream patch, 17-__FUNCTION__.
* Wed Jul 26 2006 - damien.carbery@sun.com
- Bump to 2.15.90.
* Sat Jul 22 2006 - laca@sun.com
- define DBUS_API_SUBJECT_TO_CHANGE
- add patch __FUNCTION__.diff
- delete bonobo monikers stuff from %files and %install
* Fri Jul 21 2006 - damien.carbery@sun.com
- Bump to 2.15.3.
* Fri Jun 23 2006 - brian.cameron@sun.com
- Bump to 2.14.2
* Mon May 29 2006 - damien.carbery@sun.com
- Add patch, 17-hidden, to remove G_GNUC_INTERNAL to build.
* Tue May 23 2006 - laca@sun.com
- remove patch all-linguas.diff, add glib-gettextize instead
* Thu May 11 2006 - alvaro.lopez@sun.com
- Added patch #17: ACL support
* Tue May 02 2006 - damien.carbery@sun.com
- Add patch, 16-krb5-config-no-gssapi, to update call to krb5-config as the
  gssapi parameter is obsolete.
* Fri Apr 21 2006 - damien.carbery@sun.com
- Add patch 15-all-linguas to replace @ALL_LINGUAS@ in po/Makefile with the
  list of languages. Bugzilla: 339276.
* Thu Apr 20 2006 - damien.carbery@sun.com
- Bump to 2.14.1.
* Thu Apr 13 2006 - dermot.mccluskey@sun.com
- replace sed with dos2unix to work around ^M problem in SVN
* Mon Mar 13 2006 - damien.carbery@sun.com
- Bump to 2.14.0.
* Wed Mar  1 2006 - laca@sun.com
- use sed instead of dos2unix for converting the po files, because dos2unix
  corrupts some UTF-8 strings
* Mon Feb 27 2006 - damien.carbery@sun.com
- Bump to 2.13.92.
* Mon Feb 21 2006 - damien.carbery@sun.com
- Add patch, 15-be_po, to workaround #332050.
* Mon Feb 13 2006 - damien.carbery@sun.com
- Bump to 2.13.91.
* Thu Jan 19 2006 - damien.carbery@sun.com
- Remove upstream patch (15-nocopy).
* Tue Jan 17 2006 - damien.carbery@sun.com
- Bump to 2.13.4
* Tue Jan 10 2006 - damien.carbery@sun.com
- dos2unix be.po to fix 326431.
* Tue Dec 21 2005 - damien.carbery@sun.com
- Remove upstream patch, 15-forte-build-fix. Add patch, 15-login_tty to skip
  call to a Linux-only function, login_tty.
* Tue Dec 20 2005 - damien.carbery@sun.com
- Bump to 2.13.3.
* Tue Nov 29 2005 - damien.carbery@sun.com
- Bump to 2.12.2.
* Tue Oct 11 2005 - damien.carbery@sun.com
- Bump to 2.12.1.1
* Wed Sep 14 2005 - brian.cameron@sun.com
- Bump to 2.12.0
* Mon Sep 05 2005 - damien.carbery@sun.com
- Bump to 2.11.92.
* Mon Aug 15 2005 - damien.carbery@sun.com
- Bump 2.11.90.
* Sun Aug 07 2005 - glynn.foster@sun.com
- Remove Computer and subfs patches to align better with community code.
  Narayana did the work to decide which bits we need to remove.
* Thu Aug 04 2005 - laca@sun.com
- add patch18 (nocopy.diff) for bugzilla bug 311591,
  fix by <archana.shah@wipro.com>
* Wed Jul 27 2005 - narayana.pattipati@wipro.com
- Removed patches gnome-vfs-04-nfs-drag-crash.diff (not required as nfs:// 
  method is removed) and gnome-vfs-12-correct-screen-for-folder.diff
  (upstream, fix present in 2.10). Renamed the other patches accordingly.
* Fri Jun 24 2005 - archana.shah@wipro.com
- Added patch gnome-vfs-19-subfs.diff 
- Removed patch gnome-vfs-X-subfs.diff
* Fri May 13 2005 - dinoop.thomas@wipro.com
- Updated the patch gnome-vfs-42-subfs.diff with fix for bug #6257289,
  crashing of nautilus when doing eject from context menu of CD icon.
* Wed May 11 2005 - brian.cameron@sun.com
- Add patch 18 to remove usage of gcc-extension that is not available
  in Forte.
* Fri May 06 2005 - narayana.pattipati@wipro.com
- Updated the patch gnome-vfs-45-smb-browse-fixes.diff with fixes for
  bug #6259956, permissions not followed in smb:///. The changes were
  backported from community CVS HEAD.
* Fri May 06 2005 - glynn.foster@sun.com
- Bump to 2.10.1
* Fri Apr 22 2005 - archana.shah@wipro.com
- Added patch gnome-vfs-53-trash-skip-copy.diff to fix a trash issue.
  Fixes bug #6243507
* Thu Apr 08 2005 - narayana.pattipati@wipro.com
- Updated the patch gnome-vfs-45-smb-browse-fixes.diff with fixes for
  bugs #6247186 (issue of authentication when username is present in URI)
  and #6243484 (server caching issues when authentication details entered
  are wrong first time). Patch for 6243484 has been committed to community
  CVS HEAD (bugzilla bug#171468). And patch for 6247186 has been submitted
  to bugzilla bug#172695.
* Thu Apr 07 2005 - vijaykumar.patwari@wipro.com
- Added gnome-vfs-52-ftp-auth.diff, which introduces the
  functionality for one time authentication for the user.
* Wed Apr 06 2005 - balamurali.viswanathan@wipro.com
- Modified patch gnome-vfs-10-this-comp-and-hotplug-names.diff 
  Fixes bug #6242108
* Tue Mar 15 2005 - archana.shah@wipro.com
- Added patch gnome-vfs-51-ftp-show-permissions.diff to show the permissions
  of file/folders in ftp method.
  Fixes bug #6232138
* Fri Mar 11 2005 - archana.shah@wipro.com
- Added patch gnome-vfs-50-audio-cd-show-icon.diff to show the icon for audio
  cd as well. Fixes bug #6228176
* Mon Mar 07 2005 - narayana.pattipati@wipro.com
- Updated the patch gnome-vfs-45-smb-browse-fixes.diff with fix for the 
  bug#6234261. Fixes the issue of domains not appearing in some networks.
  Patch was backported from community CVS HEAD.
* Fri Feb 25 2005 - takao.fujiwara@sun.com
- Updated gnome-vfs-24-g11n-i18n-ui.diff to localize desktop icons.
  Fixes #6233183
* Mon Feb 11 2005 - narayana.pattipati@wipro.com
- Updated the patch gnome-vfs-45-smb-browse-fixes.diff with community 
  smb method rewrite. Community has re-written smb method authentication
  completely. The patch backports all the changes. It fixes bugs like 
  4961385, 6203800 in an elegant way.
* Fri Feb 11 2005 - muktha.narayan@wipro.com
- Added gnome-vfs-49-socks-version.diff to add a new gconf key for
  SOCKS version. Fixes #4951431.
* Thu Feb 10 2005 - stephen.browne@sun.com
- Added patch gnome-vfs-48-trash-files-from-different-filesystem.diff
  to allow moving items to trash for a filesystem other than the one the users
  home directory resides on.  Fixes 6200485
* Tue Feb 01 2005 - alvaro.lopez@sun.com
- Obsoletes gnome-vfs-extra.
* Tue Feb 01 2005 - archana.shah@wipro.com
- Added patch gnome-vfs-47-mime-type-case-insensitive.diff to make mime type
  detection case insensitive.
  Fixes bug #5068327
* Mon Jan 17 2005 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-45-smb-browse-fixes.diff to fix smb:// browsing
  issues. Fixes the bugs: 6199915, 6203800 and 6215115.
  Part of the patch which is applicable to community smb-method is given
  to community as part of bugzilla bug#132933. And community maintainer
  committed the the changes to HEAD branch.
* Fri Dec 17 2004 - vinay.mandyakoppal@wipro.com
- Added patch gnome-vfs-44-.Z-association.diff to fix the problem of
  .Z file not associated with default application. Fixes #6205707.
* Mon Dec 06 2004 - archana.shah@wipro.com
- Added patch 43 to ignore rootfs file system.
  Fixes bug# 6192112
* Mon Nov 29 2004 - alvaro.lopez@sun.com
- Patch #42 applies only in linux. Added ifos.
* Tue Nov 23 2004 - arvind.samptur@wipro.com
- Add the rewrite of gnome-vfs-38-mount-points-fix.diff
  Fixes #6190753
* Tue Nov 23 2004 - alvaro.lopez@sun.com
- Added path 42. Fixes #6195964
* Tue Nov 17 2004 - alvaro.lopez@sun.com
- Source entry fixed
* Tue Nov 16 2004 - ciaran.mcdermott@sun.com
- Backing out gnome-vfs-41-potfiles.diff patch
* Tue Nov 16 2004 - ciaran.mcdermott@sun.com
- Added gnome-vfs-41-potfiles.diff to update POTFILES.in 
* Wed Nov 10 2004 - niall.power@sun.com
- Added gnome-vfs-40-fork-off.diff. Fixes bug 6182789. Backport of 
  bugzilla #151026. Patch approved by Stephen Browne. Reuses forked
  process when get unix devices of volumes instead of seperately
  forking for each volume.
* Wed Nov 10 2004 - niall.power@sun.com
- Commenting out Patch 38 (gnome-vfs-38-mount-points-fix.diff) because
  it needs to be rewritten to make performance acceptable.
* Wed Nov 10 2004 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-39-correct-screen-for-folder.diff to make sure
  that a folder is created on the correct screen. Fixes bug#6176070.
  Patch given by vijaykumar.patwari@wipro.com. 
* Tue Nov 09 2004 - vijaykumar.patwari@wipro.com
- Added patch gnome-vfs-38-mount-points-fix.diff 
  Fixes bug #6190753.
* Fri Nov 05 2004 - archana.shah@wipro.com
- Added patch gnome-vfs-37-sftp.diff.
  Part of the fix goes to libgnomeui.
  Fixes bug# 5088520.
* Thu Nov 04 2004 - ciaran.mcdermott@sun.com
- Added gnome-vfs-36-g11n-potfiles.diff to update POTFILES.in
* Fri Oct 29 2004 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-35-trash-only-home.diff to treat only user's home 
  directory as trash volume. Don't look at all the mount points in the 
  system for trash. Fix bugtraq bugs#5105006 and 5070031
* Thu Oct 28 2004 - matt.keenan@sun.com
- Add gnomevfs-cat.1, gnomevfs-copy.1, gnomevfs-info.1, gnomevfs-ls.1,
  gnomevfs-mkdir.1 man pages
* Thu Oct 14 2004 - narayana.pattipati@wipro.com
- Added Requires/BuildRequires of libsmbclient so that smb:/// is built
  properly.
* Wed Oct 13 2004 - arvind.samptur@wipro.com
- Forward port the panel polling patch from GNOME 2.0.2 to JDS
* Wed Sep 22 2004 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-33-volume-free-space-fix.diff to fix incorrect
  free space returned by gnome-vfs volume manager. Fixes bugtraq
  bug#5092286
* Wed Sep 22 2004 - vijaykumar.patwari@wipro.com
- Avoid installation of nfs.desktop file.
* Wed Sep 22 2004 - vijaykumar.patwari@wipro.com
- Removed NFS Module (i.e patch `gnome-vfs-03-nfs-module.diff`) 
  from Gnome-vfs. Renamed rest of the patches accordingly.
* Sat Sep 18 2004 - laca@sun.com
- Backported patch from gnome-vfs HEAD to prefer suffix to sniffing for
  xml files.
* Wed Sep 08 2004 - vinay.mandyakoppal@wipro.com
- Modified gnome-vfs-07-preference-menu-reorder.diff to remove duplicate
  menu items for "Printer Preferences".
* Mon Aug 30 2004 - vijaykumar.patwari@wipro.com
- Set default url handler for "https".
* Mon Aug 23 2004 - niall.power@sun.com
- remove JDS_CBE_PREFIX definition
* Wed Aug 18 2004 - brian.cameron@sun.com
- added --enable-gtk-doc
* Wed Aug 11 2004 - archana.shah@wipro.com
- Added patch 30 for gnome-printinfo
* Fri Jul 16 2004 - johan.steyn@sun.com
- Added patch 29 for Network Places
* Wed Jul 14 2004 - Yong.Sun@Sun.COM
- Added patch -28 to fix bugtraq #5052453
* Thu Jul 08 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-vfs-l10n-po-1.2.tar.bz2
* Wed Jul 07 2004 - niall.power@sun.com
- Ported to rpm4
* Wed Jul 07 2004 - dermot.mccluskey@sun.com
- added "-j $CPUS" to make to speed up builds
* Fri Jun 25 2004 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-27-sftp-exit-fix.diff to fix nautilus exit when
  using sftp:// method. Fixes bugtraq bug:5067878. The patch is a backport
  from community CVS HEAD.
* Fri Jun 25 2004 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-26-ftp-hostname-crash.diff to fix nautilus crash
  while using ftp:// method without specifying host name in the URL.
  Fixes bugtraq bug:5067212.
* Thu Jun 24 2004 - takao.fujiwara@sun.com
- Add gnome-vfs-25-g11n-i18n-ui.diff to translate open dialog. bugzilla #144902
* Wed Jun 09 2004 - archana.shah@wipro.com
- Add patch gnome-vfs-24-ftp-crash.diff
  Fixes bug# 5057615
* Tue Jun 08 2004 - arvind.samptur@wipro.com
- Remove  gnome-vfs-20-remove-gnome-20-menus.diff. We should
  have /usr/share/applications in path
* Wed Jun 02 2004 - niall.power@sun.com
- Added patch gnome-vfs-24-eject-solaris-rmm.diff to supress pointless
  error message when media is ejected.
* Mon May 31 2004 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-23-ftp-upload-crash.diff to fix nautilus crash
  while uploading a file to ftp server. Fixes bugtraq bug#5053735. 
  Submitted the patcht to bugzilla bug#143320 also.
* Wed May 26 2004 - vijaykumar.patwari@wipro.com
- Added patch gnome-vfs-21-unix-device-type.diff to fix bug#5040516.
* Mon May 24 2004 - narayana.pattipati@wipro.com
- Added patch gnome-vfs-21-ftp-data-loss.diff to fix data loss while
  transefering files through ftp:// method. Fixes bugtraq bug#5025035.
  The patch is backported from HEAD. This should be removed once the 
  latest tarball is picked up from community.
* Mon May 17 2004 - niall.power@sun.com
- Add patch to ignore old gnome-2.0 menu items on Solaris.
* Wed May 12 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-vfs-l10n-po-1.1.tar.bz2
* Tue May 11 2004 - laszlo.kovacs@sun.com
- jdshelp schema change
* Mon May 10 2004 - muktha.narayan@wipro.com
- Add <install_prefix>/share to XDG_DATA_DIRS path. 
  Fixes bug #5030813.
* Fri Apr 16 2004 - vijaykumar.patwari@wipro.com
- Set mozilla as the default url handler for http.
* Fri Apr 16 2004 - archana.shah@wipro.com
  Correcting the typo in schemas (system_smb.schemas).
* Wed Apr 14 2004 - archana.shah@wipro.com
- Change in spec file. Added desktop_default_applications.schemas and
  system_smb.schemas for gconftool-2.
  Fixes bug# 5014775
* Tue Apr 06 2004 - laszlo.kovacs@sun.com
- jdshelp schema patch
* Mon Mar 29 2004 - damien.donlon@sun.com
- Updated l10n content to gnome-vfs-l10n-po-1.0.tar.bz2
* Mon Mar 29 2004 - ghee.teo@sun.com
- Ported a patch for bug 136748 from HEAD. The problem is that nautilus could
  crash if staroffice mime data is found in user's own application mime.
  Since this fix goes in after the version of 2.6.0 tarball has been created,
  so create this patch, gnome-vfs-16-nautilus-crash-136748-from-head.diff for 
  cinnabar. For Vermillion, this patch can be dropped.
* Thu Mar 29 2004 - <narayana.pattipati@wipro.com>
- Updated patch gnome-vfs-03-nfs-module.diff to fix NFS method related
  problems like file removal, move, rename, replace etc. for bugs:
  5014972 and 5015739, 5009330. Also updated it with fix for nfs
  rename crash (for bug#4981011) from kaushal.kumar@wipro.com
* Thu Mar 25 2004 - niall.power@sun.com
- bumped to 2.6.0, updated dependency versions and
  added a dependency on shared-mime-info
* Thu Mar 11 2004 - yuriy.kuznetsov@sun.com
- added gnome-vfs-15-g11n-potfiles.diff
* Tue Mar 09 2004 - <niall.power@sun.com>
- Added patch to define gopher proxy schemas
* Thu Mar 04 2004 - <narayana.pattipati@wipro.com>
- Added patch gnome-vfs-13-nfs-drag-crash.diff to fix
  nautilus crash when a file/folder is dragged onto
  nfs:// location.
* Thu Feb 26 2004 - laszlo.kovacs@sun.com
- activated ported patch gnome-vfs-02-ftp-authn-keyring.diff
* Wed Feb 25 2004 - niall.power@sun.com
- add patch 12 for uninstalled .pc files
* Wed Feb 25 2004 - niall.power@sun.com
- remove unnecessary %{_datadir}/aclocal arg from aclocal line.
* Tue Feb 24 2004 - niall.power@sun.com
- build with the JDS_CBE auto tools and set ACLOCAL_FLAGS
  to pick up JDS_CBE aclocal macros (on linux) and Build
  Requirements accordingly.
* Mon Feb 23 2004 - stephen.browne@sun.com
- reactivate ported patches 05 and 11
* Mon Feb 23 2004 - stephen.browne@sun.com
- reactivate ported patch 03 
* Mon Feb 23 2004 - stephen.browne@sun.com
- uprev to 2.5.7, disable patches that need porting
* Mon Feb 16 2004 - stephen.browne@sun.com
- Add icons to This Computer view and get decent names for hotplug devices
* Mon Feb 09 2004 - laslzo.kovacs@sun.com
- include vfs daemon server file 
* Thu Feb 05 2004 - matt.keenan@sun.com
- Mismatch tag in gnome-vfs-01-menu-stripe.diff causing
  gnome-panel to fail
* Wed Feb 04 2004 - laszlo.kovacs@sun.com
- ftp authn patch ported
* Tue Jan 06 2004 - niall.power@sun.com
- Previous changelog entry had wrong year.
* Mon Jan 05 2004 - niall.power@sun.com
- Bump to 2.5.4.1. Add gtkdocize to prep stage to
  build broken tarball.
* Mon Dec 15 2003 - glynn.foster@sun.com
- Bump to 2.5.3
* Fri Oct 31 2003 - glynn.foster@sun.com
- Remove the extras menu. Remove Sun Supported 
  from vfolder description file.
* Wed Oct 08 2003 - stephen.browne@sun.com
- Updated to 2.4 for quicksilver
* Thu Aug 20 2003 - ghee.teo@sun.com
- Modified patch 15 to remove network-neighboorhood
  and replaced it with network-places instead.
  also updated nfs.desktop.in to refer to
  Categories=X-NetworkPlaces
* Wed Aug 20 2003 - niall.power@sun.com
- Added patch 21 (not the one Stephen removed :)
  Fixes broken nfs write method.
* Tue Aug 19 2003 - stephen.browne@sun.com
- Removed patch 21 its totally broken
* Thu Aug 14 2003 - <laca@sun.com>
- move lib*.so to -devel, remove *.a, *.la
* Tue Aug 05 2003 - stephen.browne@sun.com
- Remove dups from devices:///
* Fri Aug 01 2003 - glynn.foster@sun.com
- New extras:///. Woo.
* Wed Jul 30 2003 - glynn.foster@sun.com
- New tarball. Bump version, reset release.
* Fri Jul 25 2003 - niall.power@sun.com
- add missing cdparanoia dependencies
* Wed Jul 23 2003 - glynn.foster@sun.com
- Getting system-settings:/// in order.
* Wed Jul 23 2003 - glynn.foster@sun.com
- Make vfolder stuff useful by editing permissions of 
  autogenerated folders.
* Mon Jul 21 2003 - glynn.foster@sun.com
- Add quick-start:/// uri for panel items above. This is 
  mostly on crack.
* Mon Jul 21 2003 - glynn.foster@sun.com
- Changed preferences:/// for new menu setup.
* Fri Jul 18 2003 - glynn.foster@sun.com
- added gnome-vfs-20-vfolder-no-core-items.diff to remove the
  help, home and network neighborhood from the application menu
* Wed Jul 16 2003 - Laszlo.Kovacs@sun.com
- added gnome-vfs-19-vfolder-network-neighborhood.diff
* Wed Jul 09 2003 - <michael.twomey@sun.com>
- add in sun po files
* Wed Jul 9 2003 - Laszlo.Kovacs@sun.com
- gnome-vfs-17-vfolder-non-existent-file-monitor.diff added
  adds support for registering monitors for non-existent
  vfolder elements; extensive comments about some
  limitations are in patch
* Fri Jul 4 2003 - Laszlo.Kovacs@sun.com
- added gnome-vfs-16-network-all-users-support.diff
* Wed Jul 2 2003 - Laszlo.Kovacs@sun.com
- added patches gnome-vfs-15-uri-canonizing.diff
and gnome-vfs-14-network-vfolder-etc.diff
* Tue Jul 1 2003 - glynn.foster@sun.com
- Correct icon for applications:/// view
* Tue Jul 1 2003 - niall.power@sun.com
- Added rmmdevice monitor for devices:/// uri support
* Tue Jul 1 2003  - ghee.teo@sun.com
- Added .desktop file for network servers
* Fri Jun 30 2003 - glynn.foster@sun.com
- add patch to exlude star.desktop that we use in favorites:/// uri
* Fri Jun 8 2003 - Laszlo.Kovacs@sun.com
- fix access to authn cache in http module (gnome-vfs-06-http-fix-authn-cache-access.diff)
* Thu Jun 5 2003 - Laszlo.Kovacs@sun.com
- open root as default folder in the ftp module (gnome-vfs-03-ftp-open-root-as-default.diff)
- port fix for pathname containg %2F from HEAD (gnome-vfs-04-%2F-fix.diff)
- add authorization callback to ftp module (gnome-vfs-05-ftp-authn-callback.diff)
* Fri May 30 2003 - markmc@sun.com
- Make favorites:// include Mozilla and Evolution by default.
* Tue May 13 2003 - matt.keenan@sun.com
- initial Sun Package for GNOME 2.2 platform
